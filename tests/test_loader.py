"""
Unit tests for FIE Modular Instruction Loader & Adaptive Engine.
"""

import unittest
from fie.core.loader import ModularPromptLoader
from fie.core.adaptive import AdaptiveModelEngine

class TestModularLoader(unittest.TestCase):

    def setUp(self):
        self.loader = ModularPromptLoader()
        self.adaptive = AdaptiveModelEngine()

    def test_core_identity_loaded(self):
        identity = self.loader.load_core_identity()
        self.assertTrue(len(identity) > 50)
        self.assertIn("Identitas Sistem", identity)

    def test_agent_loading(self):
        coder = self.loader.load_agent("coder")
        self.assertIn("Lead Coder", coder)

        architect = self.loader.load_agent("architect")
        self.assertIn("System Architect", architect)

    def test_workflows_and_playbooks_loaded(self):
        wf = self.loader.load_workflow("code-review-security-audit")
        self.assertIn("Audit", wf)

        ai_guide = self.loader.load_engineering_guide("ai-llm-engineering")
        self.assertIn("Structured Outputs", ai_guide)

        std = self.loader.load_knowledge_module("programming-standards")
        self.assertIn("PEP 8", std)

        tpl = self.loader.load_template("code-template")
        self.assertIn("Deliverable Template", tpl)

    def test_list_available_modules(self):
        inventory = self.loader.list_available_modules()
        self.assertIn("agents", inventory)
        self.assertEqual(len(inventory["agents"]), 9)
        self.assertIn("ai-llm-engineering", inventory["engineering"])
        self.assertIn("code-review-security-audit", inventory["workflows"])

    def test_adaptive_compilation_small_vs_large(self):
        small_prompt = self.loader.compile_system_instruction(
            task_type="coding",
            model_profile_tier="small"
        )
        large_prompt = self.loader.compile_system_instruction(
            task_type="coding",
            model_profile_tier="large",
            domain_hint="ai-llm-engineering"
        )

        tokens_small = self.adaptive.estimate_token_count(small_prompt)
        tokens_large = self.adaptive.estimate_token_count(large_prompt)

        self.assertLess(tokens_small, tokens_large)
        self.assertLessEqual(tokens_small, 1500)
        self.assertIn("AI & LLM Systems Engineering", large_prompt)

    def test_memory_injection(self):
        memory_block = "--- PROJECT MEMORY: DB=PostgreSQL ---"
        prompt = self.loader.compile_system_instruction(
            task_type="coding",
            model_profile_tier="medium",
            context_memory=memory_block
        )
        self.assertIn(memory_block, prompt)

if __name__ == "__main__":
    unittest.main()
