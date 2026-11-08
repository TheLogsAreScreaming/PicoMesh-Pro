"""Source-level checks for the temp-file channel export; not PicoMite execution."""
import pathlib
import unittest

SOURCE = (pathlib.Path(__file__).resolve().parent.parent / "meshcore.bas").read_text(encoding="utf-8").replace("\r\n", "\n")


def block(signature):
    start = SOURCE.index(signature)
    return SOURCE[start:SOURCE.index("End Sub", start)]


def full_export():
    start = SOURCE.index("Sub DoExportLocalChannels")
    return SOURCE[start:SOURCE.index("\nEnd Sub", start)]


class SaferExportTests(unittest.TestCase):
    def test_backup_is_never_opened_for_output(self):
        self.assertNotIn('Open "CHANNELS.TXT" For Output', SOURCE)

    def test_old_backup_is_removed_only_after_new_file_is_closed(self):
        b = full_export()
        self.assertLess(b.index("Close #2"), b.index('Kill "CHANNELS.TXT"'))
        self.assertLess(b.index('Kill "CHANNELS.TXT"'), b.index('Rename "CHANNELS.TMP" As "CHANNELS.TXT"'))

    def test_kill_and_rename_errors_are_handled(self):
        b = full_export()
        for line in ('Kill "CHANNELS.TXT"', 'Rename "CHANNELS.TMP" As "CHANNELS.TXT"'):
            head, tail = b.split(line)
            self.assertEqual(head.rstrip().splitlines()[-1].strip(), "On Error Skip 1", line)
            self.assertEqual(tail.lstrip().splitlines()[0].strip(), "If MM.Errno <> 0 Then", line)

    def test_failure_tells_user_where_the_backup_is(self):
        self.assertEqual(full_export().count("The new backup is saved as CHANNELS.TMP"), 2)

    def test_restore_points_at_interrupted_export(self):
        start = SOURCE.index("Sub DoRestoreLocalChannels")
        self.assertIn('Dir$("CHANNELS.TMP")', SOURCE[start:start + 900])

    def test_startup_hint_is_error_guarded_and_does_not_load(self):
        b = block("Sub ShowSavedChannelsHint")
        self.assertIn("On Error Skip 1", b)
        self.assertIn("MM.Errno = 0", b)
        self.assertNotIn("Open ", b)
        self.assertIn("\nShowSavedChannelsHint\n", SOURCE)


if __name__ == "__main__":
    unittest.main()
