"""
Unit tests for FIE Benchmark & Evaluation Runner.
"""

import unittest
from fie.evaluation.runner import BenchmarkRunner

class TestBenchmarkRunner(unittest.TestCase):

    def setUp(self):
        self.runner = BenchmarkRunner()

    def test_coding_suite(self):
        res = self.runner.run_coding_suite()
        self.assertEqual(res["category"], "Coding")
        self.assertEqual(res["correctness_score"], 100.0)

    def test_reasoning_suite(self):
        res = self.runner.run_reasoning_suite()
        self.assertEqual(res["category"], "Reasoning & Logic")
        self.assertEqual(res["correctness_score"], 100.0)
        self.assertEqual(res["passed_cases"], 3)

    def test_full_benchmark(self):
        res = self.runner.run_full_benchmark()
        self.assertGreaterEqual(res["final_score"], 95.0)
        self.assertTrue(res["grade"].startswith("S"))
        self.assertEqual(len(res["suites"]), 4)

if __name__ == "__main__":
    unittest.main()
