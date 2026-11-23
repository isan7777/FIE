"""
Unit tests for FIE Master Orchestrator.
"""

import unittest
from fie.core.orchestrator import MasterOrchestrator

class TestMasterOrchestrator(unittest.TestCase):

    def setUp(self):
        self.orchestrator = MasterOrchestrator()

    def test_task_classification_and_complexity(self):
        # Coding task
        c_res = self.orchestrator.classify_task("Buatkan fungsi Python untuk memfilter array")
        self.assertEqual(c_res["task_type"], "coding")
        self.assertTrue(c_res["complexity"] >= 5)

        # Debugging task
        d_res = self.orchestrator.classify_task("Perbaiki bug IndexError pada script parser data")
        self.assertEqual(d_res["task_type"], "debugging")

        # Research task
        r_res = self.orchestrator.classify_task("Lakukan riset mendalam perbandingan paper arsitektur transformer")
        self.assertEqual(r_res["task_type"], "research")

    def test_pipeline_determination(self):
        # Small model -> single agent
        p_small = self.orchestrator.determine_pipeline("coding", complexity=4, model_tier="small")
        self.assertEqual(p_small, ["coder"])

        # Medium model -> multi-stage pipeline
        p_medium = self.orchestrator.determine_pipeline("coding", complexity=6, model_tier="medium")
        self.assertEqual(p_medium, ["architect", "coder", "tester"])

    def test_workflow_execution_offline(self):
        result = self.orchestrator.execute_workflow(
            task_prompt="Buatkan fungsi hitung faktorial dengan Python",
            session_id="test_orch_sess",
            model_tier="small"
        )
        self.assertIn("session_id", result)
        self.assertEqual(result["task_type"], "coding")
        self.assertTrue(len(result["steps"]) > 0)
        self.assertIn("final_status", result)

if __name__ == "__main__":
    unittest.main()
