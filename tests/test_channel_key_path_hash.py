"""Source-level checks for channel-key and path-hash commands (firmware main 81dbae5)."""
import pathlib
import re
import unittest

SOURCE = (pathlib.Path(__file__).resolve().parent.parent / "meshcore.bas").read_text(encoding="utf-8").replace("\r\n", "\n")


def body(sig, end="\nEnd Sub"):
    s = SOURCE.index(sig)
    return SOURCE[s:SOURCE.index(end, s)]


class ChannelKeyTests(unittest.TestCase):
    def setUp(self):
        self.b = body("Sub DoSetChannelKey")

    def test_frame_layout_matches_firmware(self):
        self.assertIn('SendFrame Chr$(32) + Chr$(idxVal) + name$ + String$(32 - Len(name$), Chr$(0)) + HexToBin$(keyHex$)', self.b)
        name = b"ops"
        frame = bytes([32, 1]) + name + bytes(32 - len(name)) + bytes(16)
        self.assertEqual(len(frame), 2 + 32 + 16)  # 2+32+32 is refused by the firmware

    def test_public_slot_is_refused(self):
        self.assertIn('InStr("1234567", idxStr$) = 0', self.b)

    def test_key_is_never_printed(self):
        for line in self.b.splitlines():
            if line.strip().startswith("Print") or "DumpHex" in line:
                self.assertNotIn("keyHex$", line)

    def test_key_cleared_on_every_path_after_entry(self):
        after = self.b[self.b.index('Line Input "Key'):]
        self.assertEqual(after.count('keyHex$ = ""'), 3)
        self.assertLess(after.index("SendFrame"), after.rindex('keyHex$ = ""'))

    def test_apply_required_before_send(self):
        self.assertLess(self.b.index('confirm$ <> "APPLY"'), self.b.index("SendFrame"))

    def test_key_format_check(self):
        f = body("Function IsChannelKeyHex(s$)", "End Function")
        self.assertIn("If Len(s$) <> 32 Then Exit Function", f)
        self.assertIn("IsChannelKeyHex = nonZero", f)


class PathHashTests(unittest.TestCase):
    def setUp(self):
        self.b = body("Sub DoSetPathHashSize")

    def test_frame_and_range_match_firmware(self):
        self.assertIn("SendFrame Chr$(61) + Chr$(0) + Chr$(sizeVal - 1)", self.b)
        self.assertIn('InStr("123", sizeStr$) = 0', self.b)  # firmware refuses mode >= 3

    def test_needs_reported_mode(self):
        self.assertLess(self.b.index("If gPathHashMode < 0 Then"), self.b.index("SendFrame"))

    def test_device_info_offset(self):
        # code, ver, contacts, channels, pin(4), build(12), maker(40), version(20), repeat, mode
        self.assertEqual(1 + 1 + 1 + 1 + 4 + 12 + 40 + 20 + 1 + 1, 82)
        self.assertIn("Len(a$) >= 82 Then gPathHashMode = Asc(Mid$(a$, 82, 1))", SOURCE)

    def test_state_changes_only_on_ok(self):
        tail = self.b[self.b.index("SendFrame"):]
        self.assertLess(tail.index("= 0 Then"), tail.index("gPathHashMode = sizeVal - 1"))


if __name__ == "__main__":
    unittest.main()
