"""
Unit tests for FIE Master Orchestrator and Autonomous Self-Correction Loop.
"""

import unittest
from typing import Any, Dict, Optional
from fie.core.orchestrator import MasterOrchestrator

class FlakyMockClient:
    """Simulates an LLM that fails verification on attempt 1 and succeeds on attempt 2."""

    def __init__(self) -> None:
        self.calls = 0

    def generate_response(self, prompt: str, system_instruction: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
        self.calls += 1
        if self.calls == 1:
            return {
                "status": "success",
                "text": "def broken_syntax(\n    return 1"
            }
        return {
            "status": "success",
            "text": "def valid_function(x: int) -> int:\n    return x * 2"
        }

class TestMasterOrchestrator(unittest.TestCase):

    def setUp(self):
        self.orchestrator = MasterOrchestrator()

    def test_task_classification_and_domain_detection(self):
        c_res = self.orchestrator.classify_task("Buatkan fungsi Python untuk query database SQLite dengan index")
        self.assertEqual(c_res["task_type"], "coding")
        self.assertEqual(c_res["engineering_domain"], "database")
        self.assertTrue(c_res["complexity"] >= 5)

        d_res = self.orchestrator.classify_task("Perbaiki bug IndexError pada script parser data")
        self.assertEqual(d_res["task_type"], "debugging")

        r_res = self.orchestrator.classify_task("Lakukan riset mendalam perbandingan paper arsitektur transformer")
        self.assertEqual(r_res["task_type"], "research")

    def test_pipeline_determination(self):
        p_small = self.orchestrator.determine_pipeline("coding", complexity=4, model_tier="small")
        self.assertEqual(p_small, ["coder"])

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
        self.orchestrator.memory.clear_session("test_orch_sess")

    def test_autonomous_self_correction_loop(self):
        flaky_client = FlakyMockClient()
        orch = MasterOrchestrator(client=flaky_client)
        result = orch.execute_workflow(
            task_prompt="Buatkan fungsi perkalian sederhana",
            session_id="test_self_correct_sess",
            model_tier="small"
        )
        step = result["steps"][0]
        self.assertEqual(step["attempts"], 2)
        self.assertEqual(step["verification"]["status"], "SYNTAX_PASSED")
        orch.memory.clear_session("test_self_correct_sess")

if __name__ == "__main__":
    unittest.main()
