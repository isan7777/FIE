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

    def test_adaptive_compilation_small_vs_large(self):
        small_prompt = self.loader.compile_system_instruction(
            task_type="coding",
            model_profile_tier="small"
        )
        large_prompt = self.loader.compile_system_instruction(
            task_type="coding",
            model_profile_tier="large"
        )

        tokens_small = self.adaptive.estimate_token_count(small_prompt)
        tokens_large = self.adaptive.estimate_token_count(large_prompt)

        # Small model prompt must be more compact than large model prompt
        self.assertLess(tokens_small, tokens_large)
        self.assertLessEqual(tokens_small, 1500)

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
