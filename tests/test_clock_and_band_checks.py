"""Source-level checks for the forward-clock prompt and LoRa band warning."""
import pathlib
import re
import unittest

SOURCE = (pathlib.Path(__file__).resolve().parent.parent / "meshcore.bas").read_text(encoding="utf-8").replace("\r\n", "\n")


def body(sig, end):
    s = SOURCE.index(sig)
    return SOURCE[s:SOURCE.index(end, s)]


def bands():
    return [(float(a), float(b)) for a, b in re.findall(r"If f >= ([\d.]+) And f <= ([\d.]+) Then", body("Function IsCommonLoraBand(f)", "End Function"))]


class BandTests(unittest.TestCase):
    def common(self, f):
        return any(a <= f <= b for a, b in bands())

    def test_usual_frequencies_are_common(self):
        for f in (433.875, 869.525, 915.0, 2450.0):
            self.assertTrue(self.common(f), f)

    def test_odd_frequencies_are_flagged(self):
        for f in (150.0, 600.0, 950.0, 2500.0):
            self.assertFalse(self.common(f), f)

    def test_warning_does_not_block(self):
        b = body("Sub DoSetRadioParams", "End Sub")
        w = b[b.index("If IsCommonLoraBand(freqMHz) = 0 Then"):]
        self.assertNotIn("Exit Sub", w[:w.index("End If")])
        self.assertLess(b.index("IsCommonLoraBand"), b.index('Line Input "Type APPLY'))


class ClockPromptTests(unittest.TestCase):
    def setUp(self):
        self.b = body("Sub DoSyncDeviceTime", "\nEnd Sub")

    def test_prompt_comes_before_the_set_command(self):
        self.assertLess(self.b.index("ReadRadioEpoch()"), self.b.index("payload$ = Chr$(6)"))
        self.assertLess(self.b.index('confirm$ <> "SYNC"'), self.b.index("payload$ = Chr$(6)"))

    def test_invalid_clock_is_rejected_before_querying_radio(self):
        self.assertLess(self.b.index("PicoClockValid() = 0"), self.b.index("ReadRadioEpoch()"))

    def test_threshold_and_no_reply_path(self):
        self.assertIn("Const CLOCK_CONFIRM_AHEAD_S = 86400", SOURCE)
        self.assertIn("If radioEpoch > 0 And epochVal - radioEpoch > CLOCK_CONFIRM_AHEAD_S Then", self.b)

    def test_read_checks_code_and_length(self):
        f = body("Function ReadRadioEpoch()", "End Function")
        self.assertIn("If Len(frame$) < 5 Then Exit Function", f)
        self.assertIn("<> 9 Then Exit Function", f)
        self.assertIn("U32LEVal(frame$, 2)", f)


if __name__ == "__main__":
    unittest.main()
