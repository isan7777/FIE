"""
Unit tests for FIE Built-in Tools and Sandbox Registry.
"""

import unittest
from fie.tools.builtin import ToolRegistry

class TestBuiltinTools(unittest.TestCase):

    def setUp(self):
        self.registry = ToolRegistry()

    def test_list_declarations(self):
        decls = self.registry.list_declarations()
        names = [d["name"] for d in decls]
        self.assertIn("execute_python_code", names)
        self.assertIn("read_file", names)
        self.assertIn("write_file", names)

    def test_execute_python_code(self):
        res = self.registry.execute("execute_python_code", code="print(2 ** 10)")
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["result"]["exit_code"], 0)
        self.assertIn("1024", res["result"]["stdout"])

    def test_path_traversal_containment(self):
        # Attempt to read something outside base dir
        res = self.registry.execute("read_file", path="../../../windows/system32/cmd.exe")
        self.assertEqual(res["status"], "error")
        self.assertIn("escapes workspace boundary", res["message"])

if __name__ == "__main__":
    unittest.main()
