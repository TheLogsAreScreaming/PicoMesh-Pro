"""Keep the hardware tester issue form in step with the RC evidence log."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
FORM = (ROOT / ".github" / "ISSUE_TEMPLATE" / "hardware-test.yml").read_text()
LOG = (ROOT / "docs" / "RC_EVIDENCE_LOG.md").read_text()


class HardwareIssueTemplateTests(unittest.TestCase):
    def test_every_evidence_scenario_has_a_result_field(self):
        rows = re.findall(r"^\| (.+?) \| NOT TESTED \|", LOG, re.M)
        self.assertEqual(len(rows), 15)
        labels = re.findall(r'^      label: "(.+)"$', FORM, re.M)
        self.assertEqual(labels, rows)

    def test_results_default_to_not_tested(self):
        blocks = FORM.split("  - type: dropdown")[1:]
        results = [b for b in blocks if "id: result_" in b]
        self.assertEqual(len(results), 15)
        for b in results:
            self.assertIn("        - NOT TESTED\n", b)
            self.assertIn("default: 0", b)

    def test_privacy_acknowledgement_is_required(self):
        privacy = FORM.split("id: privacy", 1)[1].split("  - type:", 1)[0]
        self.assertEqual(privacy.count("required: true"), 2)
        self.assertIn("channel secrets", privacy)

    def test_required_identity_fields(self):
        for field in ("commit", "app_version", "board", "companion", "wiring"):
            section = FORM.split(f"id: {field}\n", 1)[1].split("  - type:", 1)[0]
            self.assertIn("required: true", section, field)

    def test_title_matches_tester_program(self):
        program = (ROOT / "docs" / "HARDWARE_TESTER_PROGRAM.md").read_text()
        self.assertIn("Hardware test: <board> / <companion> / <short outcome>", program)
        self.assertIn('title: "Hardware test: <board> / <companion> / <short outcome>"', FORM)


if __name__ == "__main__":
    unittest.main()
