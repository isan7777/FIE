"""
Modular Instruction Loader for Frontier Intelligence Engine (FIE).
Dynamically parses markdown instructions and compiles compact, task-focused
Master System Instructions tailored to the active model profile.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import logging
from fie.core.adaptive import AdaptiveModelEngine, ModelProfile

logger = logging.getLogger("fie.loader")

class ModularPromptLoader:
    """Loads and compiles specialized prompts on-demand to prevent context bloating."""

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent.parent.parent
        else:
            self.base_dir = Path(base_dir).resolve()

        self.adaptive_engine = AdaptiveModelEngine()

    def _read_file_safe(self, relative_path: str) -> str:
        target = self.base_dir / relative_path
        if not target.exists():
            logger.warning(f"Prompt module file missing: {target}")
            return ""
        try:
            with open(target, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            logger.error(f"Error reading {target}: {e}")
            return ""

    def load_core_identity(self) -> str:
        return self._read_file_safe("core/identity.md")

    def load_reasoning_protocol(self) -> str:
        return self._read_file_safe("core/reasoning.md")

    def load_agent(self, agent_name: str) -> str:
        clean_name = agent_name.lower().replace("-agent", "").replace(".md", "")
        return self._read_file_safe(f"agents/{clean_name}.md")

    def load_intelligence_module(self, module_name: str) -> str:
        clean_name = module_name.lower().replace(".md", "")
        return self._read_file_safe(f"intelligence/{clean_name}.md")

    def load_engineering_guide(self, guide_name: str) -> str:
        clean_name = guide_name.lower().replace(".md", "")
        return self._read_file_safe(f"engineering/{clean_name}.md")

    def load_research_protocol(self, protocol_name: str) -> str:
        clean_name = protocol_name.lower().replace(".md", "")
        return self._read_file_safe(f"research/{clean_name}.md")

    def compile_system_instruction(
        self,
        task_type: str = "general",
        model_profile_tier: str = "medium",
        active_agent: Optional[str] = None,
        context_memory: Optional[str] = None
    ) -> str:
        """
        Dynamically packages core identity, specialized agent instructions,
        domain guidelines, and memory into a single optimized system instruction.
        """
        profile: ModelProfile = self.adaptive_engine.get_profile(model_profile_tier)
        sections: List[str] = []

        # 1. Core Identity & Directives (Always included)
        core_id = self.load_core_identity()
        if core_id:
            sections.append(core_id)

        # 2. Reasoning Protocol (Included for Medium & Large, simplified for Small)
        if profile.tier != "small":
            reasoning = self.load_reasoning_protocol()
            if reasoning:
                sections.append(reasoning)

        # 3. Dedicated Agent Role
        if not active_agent:
            # Map task_type to default agent
            agent_map = {
                "coding": "coder",
                "debugging": "debugger",
                "research": "researcher",
                "architecture": "architect",
                "analysis": "analyst",
                "design": "designer",
                "testing": "tester",
                "writing": "writer"
            }
            active_agent = agent_map.get(task_type.lower(), "orchestrator")

        agent_content = self.load_agent(active_agent)
        if agent_content:
            sections.append(agent_content)

        # 4. Domain-Specific Guidelines
        if task_type.lower() == "coding":
            eng_guide = self.load_engineering_guide("backend")
            if eng_guide and profile.tier != "small":
                sections.append(eng_guide)
        elif task_type.lower() == "research":
            res_guide = self.load_research_protocol("web-research")
            if res_guide and profile.tier != "small":
                sections.append(res_guide)

        # 5. Self-Verification Directive
        verif_doc = self.load_intelligence_module("verification")
        if verif_doc:
            sections.append(verif_doc)

        # 6. Injected Project Memory (if provided)
        if context_memory:
            sections.append(context_memory)

        # Combine and apply model-adaptive compression
        full_text = "\n\n---\n\n".join(sections)
        compressed = self.adaptive_engine.compress_prompt(full_text, profile.tier)

        # Token Budget Check
        estimated_tokens = self.adaptive_engine.estimate_token_count(compressed)
        if estimated_tokens > profile.max_instruction_tokens:
            logger.info(
                f"Instruction tokens ({estimated_tokens}) exceeds budget ({profile.max_instruction_tokens}) "
                f"for tier '{profile.tier}'. Applying aggressive trimming."
            )
            # Retain Core Identity + Active Agent + Memory
            trimmed_sections = [sections[0]]
            if agent_content:
                trimmed_sections.append(agent_content)
            if context_memory:
                trimmed_sections.append(context_memory)
            compressed = self.adaptive_engine.compress_prompt("\n\n---\n\n".join(trimmed_sections), profile.tier)

        return compressed
