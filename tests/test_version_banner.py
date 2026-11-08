"""The program identifies itself so hardware reports name the build tested."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "meshcore.bas").read_text()


class VersionBannerTests(unittest.TestCase):
    def test_version_is_set_before_use_and_printed_at_startup(self):
        m = re.search(r'^gAppVersion\$ = "(\d+\.\d+\.\d+(?:-[0-9A-Za-z.]+)?)"$', SOURCE, re.M)
        self.assertIsNotNone(m)
        self.assertLess(SOURCE.index("Dim gAppVersion$"), m.start())
        banner = 'Print "PicoMesh Pro "; gAppVersion$'
        self.assertLess(m.start(), SOURCE.index(banner))
        self.assertLess(SOURCE.index(banner), SOURCE.index("DoInitialize\n"))
        self.assertNotIn('Print "MeshCore Pico Client"', SOURCE)

    def test_status_shows_version(self):
        start = SOURCE.index("Sub ShowStatus")
        self.assertIn('Print "PicoMesh Pro: "; gAppVersion$', SOURCE[start:SOURCE.index("End Sub", start)])

    def test_banner_keeps_upstream_attribution(self):
        self.assertIn("Based on PicoMeshCore by Vigoleis912 (GPL-3.0)", SOURCE)


if __name__ == "__main__":
    unittest.main()
