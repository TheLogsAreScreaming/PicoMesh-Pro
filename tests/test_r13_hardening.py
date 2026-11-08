"""Audit R13: smaller robustness fixes (source anchors plus a date check).

Not PicoMite execution.
"""
from datetime import datetime, timezone
from pathlib import Path
import random
import re
import unittest

SOURCE = (Path(__file__).resolve().parents[1] / "meshcore.bas").read_text()


def block(signature, end):
    start = SOURCE.index(signature)
    return SOURCE[start:SOURCE.index(end, start)]


def unix_to_date(t):
    """Python port of Function UnixToDate$ (same year/month walk)."""
    seconds, t = t % 60, t // 60
    minutes, t = t % 60, t // 60
    hours, days = t % 24, t // 24
    year = 1970
    while True:
        leap = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
        length = 366 if leap else 365
        if days < length:
            break
        days -= length
        year += 1
    months = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month = 1
    while days >= months[month - 1]:
        days -= months[month - 1]
        month += 1
    return f"{year:04d}-{month:02d}-{days + 1:02d} {hours:02d}:{minutes:02d}:{seconds:02d}"


class HardeningTests(unittest.TestCase):
    def test_unix_to_date_never_assigns_its_parameter(self):
        b = block("Function UnixToDate$(t)", "End Function")
        self.assertIn("tVal = Int(t)", b)
        self.assertIsNone(re.search(r"^\s*t\s*=", b, re.M))

    def test_unix_to_date_port_matches_calendar(self):
        rng = random.Random(7)
        samples = [0, 951782400, 1709164800, 4102444799] + [rng.randrange(0, 2**32) for _ in range(500)]
        for t in samples:
            expected = datetime.fromtimestamp(t, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            self.assertEqual(unix_to_date(t), expected, t)

    def test_boot_dump_has_overall_cap(self):
        b = block("Sub ReadRawBytes(timeoutMs)", "End Sub")
        self.assertIn("Loop Until Timer - t0 > timeoutMs Or Timer - tStart > BOOT_READ_MAX_MS", b)
        self.assertIn("Const BOOT_READ_MAX_MS = 5000", SOURCE)

    def test_response_wait_uses_one_overall_deadline(self):
        b = block("Function ReadResponseSkippingAsync$(timeoutMs)", "End Function")
        self.assertIn("remainingMs = timeoutMs - (Timer - t0)", b)
        self.assertIn("If remainingMs > 0 Then frame$ = ReadFrame$(remainingMs)", b)
        self.assertNotIn("ReadFrame$(timeoutMs)", b)
        self.assertLess(b.index("t0 = Timer"), b.index("  Do\n"))
        self.assertIn("If asyncCount = 0 Then NoteNoReply", b)

    def test_channel_file_open_errors_are_handled(self):
        for sub_name, name, mode in (
            ("Sub DoRestoreLocalChannels", "CHANNELS.TXT", "Input"),
            ("Sub DoExportLocalChannels", "CHANNELS.TMP", "Output"),
        ):
            b = block(sub_name, "End Sub")
            open_line = f'Open "{name}" For {mode} As #2'
            before = b[:b.index(open_line)].rstrip().splitlines()[-1].strip()
            self.assertEqual(before, "On Error Skip 1", sub_name)
            after = b[b.index(open_line) + len(open_line):].lstrip().splitlines()[0].strip()
            self.assertEqual(after, "If MM.Errno <> 0 Then", sub_name)


if __name__ == "__main__":
    unittest.main()
