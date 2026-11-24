"""
Unit tests for FIE Verification Engine.
"""

import unittest
from fie.verification.engine import VerificationEngine

class TestVerificationEngine(unittest.TestCase):

    def setUp(self):
        self.verifier = VerificationEngine()

    def test_valid_python_syntax(self):
        code = "def add(a: int, b: int) -> int:\n    return a + b"
        result = self.verifier.verify_python_code(code)
        self.assertEqual(result["status"], "SYNTAX_PASSED")
        self.assertTrue(result["syntax_valid"])
        self.assertEqual(result["grade"], "A")

    def test_invalid_python_syntax(self):
        code = "def broken(a, b\n    return a +"
        result = self.verifier.verify_python_code(code)
        self.assertEqual(result["status"], "FAILED")
        self.assertFalse(result["syntax_valid"])
        self.assertEqual(result["grade"], "F")
        self.assertTrue(len(result["issues"]) > 0)

    def test_security_violation_detection(self):
        code = "import os\ndef dangerous(cmd):\n    return eval(cmd)"
        result = self.verifier.verify_python_code(code)
        self.assertEqual(result["grade"], "F")
        has_security_issue = any("[SECURITY]" in iss for iss in result["issues"])
        self.assertTrue(has_security_issue)

    def test_stub_warning_detection(self):
        code = "def calculate_total():\n    # TODO: implement formula\n    pass"
        result = self.verifier.verify_python_code(code)
        self.assertTrue(len(result["warnings"]) > 0)

    def test_dynamic_test_execution(self):
        code = "def multiply(x, y): return x * y"
        test = "assert multiply(3, 4) == 12"
        result = self.verifier.verify_python_code(code, run_test=True, test_code=test)
        self.assertEqual(result["status"], "VERIFIED")
        self.assertTrue(result["test_passed"])
        self.assertEqual(result["grade"], "S")

    def test_markdown_with_fenced_python_deliverable(self):
        markdown_doc = (
            "# Implementation Report\n"
            "Below is the production module for computing squares safely with full type annotations:\n\n"
            "```python\n"
            "def compute_square(n: int) -> int:\n"
            "    return n * n\n"
            "```\n"
        )
        res = self.verifier.verify_deliverable(markdown_doc)
        self.assertEqual(res["deliverable_type"], "markdown_with_python")
        self.assertEqual(res["code_blocks_count"], 1)
        self.assertTrue(res["syntax_valid"])
        self.assertEqual(res["status"], "SYNTAX_PASSED")

    def test_text_deliverable_verification(self):
        good_text = (
            "# Executive Architectural Report\n"
            "This report outlines the distributed caching layer and system resilience specifications. "
            "All components comply with high-availability guidelines and zero-downtime rollover protocols."
        )
        res = self.verifier.verify_text_deliverable(good_text, required_keywords=["Executive", "caching"])
        self.assertEqual(res["status"], "VERIFIED")

        bad_text = "Short text {UNRESOLVED_PLACEHOLDER}"
        res_bad = self.verifier.verify_text_deliverable(bad_text)
        self.assertTrue(len(res_bad["warnings"]) > 0 or len(res_bad["issues"]) > 0)

    def test_emoji_sticker_detection_and_sanitization(self):
        emoji_char = chr(0x1F680)
        thumbs_char = chr(0x1F44D)

        code_with_emoji = f"def greet():\n    # Launch {emoji_char}\n    return 'ok'"
        res = self.verifier.verify_python_code(code_with_emoji)
        has_emoji_warning = any("[STYLE_POLICY]" in w for w in res["warnings"])
        self.assertTrue(has_emoji_warning)

        text_with_emoji = f"Laporan Performa Sistem: Semua modul berjalan dengan baik {thumbs_char}"
        res_text = self.verifier.verify_text_deliverable(text_with_emoji)
        has_text_emoji = any("[STYLE_POLICY]" in w for w in res_text["warnings"])
        self.assertTrue(has_text_emoji)

        sanitized = self.verifier.sanitize_emojis(text_with_emoji)
        self.assertNotIn(thumbs_char, sanitized)

    def test_poetic_cliche_detection(self):
        poetic_text = (
            "Koleksi destinasi alam, situs warisan peradaban, dan pusat tradisi yang dipilih secara saksama "
            "dengan informasi perjalanan lengkap dan etika berkunjung. Ubud di Gianyar adalah episentrum "
            "seni rupa, tari, dan ketenangan jiwa di perbukitan Bali tengah. Di lereng Gunung Batukaru "
            "terbentang Terasering Sawah Jatiluwih seluas ribuan hektar."
        )
        res_poetic = self.verifier.verify_text_deliverable(poetic_text)
        self.assertEqual(res_poetic["status"], "NEEDS_REVIEW")
        style_warnings = [w for w in res_poetic["warnings"] if "[STYLE_POLICY]" in w]
        self.assertGreaterEqual(len(style_warnings), 4)

        natural_text = (
            "Daftar tempat wisata alam, budaya, dan sejarah di Bali, lengkap dengan info rute, tiket masuk, "
            "serta aturan berkunjung. Ubud di Gianyar dikenal sebagai pusat kesenian, pertunjukan tari "
            "tradisional, dan suasana pedesaan yang tenang."
        )
        res_natural = self.verifier.verify_text_deliverable(natural_text)
        self.assertEqual(res_natural["status"], "VERIFIED")
        self.assertEqual(len(res_natural["warnings"]), 0)

if __name__ == "__main__":
    unittest.main()
