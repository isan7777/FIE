"""
Modular Instruction Loader for Frontier Intelligence Engine (FIE).
Dynamically parses markdown instructions and compiles compact, task-focused
Master System Instructions tailored to the active model profile.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import logging
from fie.config import FIEConfig
from fie.core.adaptive import AdaptiveModelEngine, ModelProfile

logger = logging.getLogger("fie.loader")

class ModularPromptLoader:
    """Loads and compiles specialized prompts on-demand to prevent context bloating."""

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        config: Optional[FIEConfig] = None
    ) -> None:
        if base_dir is None:
            self.base_dir = Path(__file__).resolve().parent.parent.parent
        else:
            self.base_dir = Path(base_dir).resolve()

        self.config = config or FIEConfig(base_dir=self.base_dir)
        custom_profiles = self.config.model_profiles.get("profiles")
        self.adaptive_engine = AdaptiveModelEngine(custom_profiles=custom_profiles)

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

    @staticmethod
    def _clean_slug(name: str) -> str:
        return name.strip().lower().replace("-agent", "").replace("fie-", "").replace(".md", "")

    def load_core_identity(self) -> str:
        return self._read_file_safe("core/identity.md")

    def load_reasoning_protocol(self) -> str:
        return self._read_file_safe("core/reasoning.md")

    def load_decision_engine(self) -> str:
        return self._read_file_safe("core/decision-engine.md")

    def load_adaptive_intelligence(self) -> str:
        return self._read_file_safe("core/adaptive-intelligence.md")

    def load_agent(self, agent_name: str) -> str:
        clean_name = self._clean_slug(agent_name)
        return self._read_file_safe(f"agents/{clean_name}.md")

    def load_intelligence_module(self, module_name: str) -> str:
        clean_name = self._clean_slug(module_name)
        return self._read_file_safe(f"intelligence/{clean_name}.md")

    def load_engineering_guide(self, guide_name: str) -> str:
        clean_name = self._clean_slug(guide_name)
        return self._read_file_safe(f"engineering/{clean_name}.md")

    def load_research_protocol(self, protocol_name: str) -> str:
        clean_name = self._clean_slug(protocol_name)
        return self._read_file_safe(f"research/{clean_name}.md")

    def load_workflow(self, workflow_name: str) -> str:
        clean_name = self._clean_slug(workflow_name)
        return self._read_file_safe(f"workflows/{clean_name}.md")

    def load_knowledge_module(self, module_name: str) -> str:
        clean_name = self._clean_slug(module_name)
        return self._read_file_safe(f"knowledge/{clean_name}.md")

    def load_tool_contract(self, tool_name: str) -> str:
        clean_name = self._clean_slug(tool_name)
        return self._read_file_safe(f"tools/{clean_name}.md")

    def load_template(self, template_name: str) -> str:
        clean_name = self._clean_slug(template_name)
        return self._read_file_safe(f"templates/{clean_name}.md")

    def list_available_modules(self) -> Dict[str, List[str]]:
        """Scans the FIE directory and returns all available markdown modules by category."""
        categories = [
            "core",
            "agents",
            "intelligence",
            "engineering",
            "research",
            "workflows",
            "knowledge",
            "tools",
            "templates",
            "evaluation"
        ]
        inventory: Dict[str, List[str]] = {}
        for cat in categories:
            cat_dir = self.base_dir / cat
            if cat_dir.exists() and cat_dir.is_dir():
                inventory[cat] = sorted([
                    p.stem for p in cat_dir.glob("*.md")
                ])
            else:
                inventory[cat] = []
        return inventory

    def resolve_engineering_guide_name(self, task_type: str, domain_hint: Optional[str] = None) -> str:
        """Selects the most relevant engineering guide based on domain hint or task type."""
        valid_guides = {
            "api-integration",
            "backend",
            "database",
            "frontend",
            "game-development",
            "performance",
            "security",
            "software-architecture",
            "ai-llm-engineering"
        }
        if domain_hint:
            cleaned = self._clean_slug(domain_hint)
            if cleaned in valid_guides:
                return cleaned

        task_to_guide = {
            "coding": "backend",
            "architecture": "software-architecture",
            "design": "frontend",
            "debugging": "performance",
            "security": "security"
        }
        return task_to_guide.get(task_type.lower(), "backend")

    def resolve_workflow_name(self, task_type: str) -> str:
        """Maps a task type to its canonical execution workflow SOP."""
        workflow_map = {
            "coding": "software-project",
            "architecture": "software-project",
            "design": "software-project",
            "debugging": "bug-fixing",
            "research": "deep-research",
            "analysis": "project-execution",
            "writing": "project-execution",
            "security": "code-review-security-audit"
        }
        return workflow_map.get(task_type.lower(), "project-execution")

    def compile_system_instruction(
        self,
        task_type: str = "general",
        model_profile_tier: str = "medium",
        active_agent: Optional[str] = None,
        context_memory: Optional[str] = None,
        domain_hint: Optional[str] = None,
        include_workflow: bool = True,
        include_template: Optional[str] = None
    ) -> str:
        """
        Dynamically packages core identity, specialized agent instructions,
        domain guidelines, workflows, standards, and memory into a single optimized system instruction.
        """
        profile: ModelProfile = self.adaptive_engine.get_profile(model_profile_tier)
        sections: List[str] = []

        # 1. Core Identity & Directives (Always included)
        core_id = self.load_core_identity()
        if core_id:
            sections.append(core_id)

        # 2. Reasoning Protocol (Included for Medium & Large, omitted for Small to save tokens)
        if profile.tier != "small":
            reasoning = self.load_reasoning_protocol()
            if reasoning:
                sections.append(reasoning)

        # 3. Dedicated Agent Role
        if not active_agent:
            agent_map = {
                "coding": "coder",
                "debugging": "debugger",
                "research": "researcher",
                "architecture": "architect",
                "analysis": "analyst",
                "design": "designer",
                "testing": "tester",
                "writing": "writer",
                "security": "debugger"
            }
            active_agent = agent_map.get(task_type.lower(), "orchestrator")

        agent_content = self.load_agent(active_agent)
        if agent_content:
            sections.append(agent_content)

        # 4. Domain-Specific Guidelines & Playbooks
        t_lower = task_type.lower()
        if profile.tier != "small":
            if t_lower in ("coding", "architecture", "design", "debugging", "security") or domain_hint:
                guide_name = self.resolve_engineering_guide_name(t_lower, domain_hint)
                eng_guide = self.load_engineering_guide(guide_name)
                if eng_guide:
                    sections.append(eng_guide)
            elif t_lower == "research":
                res_guide = self.load_research_protocol("web-research")
                if res_guide:
                    sections.append(res_guide)
                if profile.tier == "large":
                    fact_guide = self.load_research_protocol("fact-checking")
                    if fact_guide:
                        sections.append(fact_guide)

        # 5. Canonical Workflow SOP & Knowledge Standards (Medium & Large profiles)
        if include_workflow and profile.tier != "small":
            wf_name = self.resolve_workflow_name(t_lower)
            wf_doc = self.load_workflow(wf_name)
            if wf_doc:
                sections.append(wf_doc)

        if profile.tier != "small" and t_lower in ("writing", "design", "coding"):
            nat_lang_doc = self.load_knowledge_module("natural-language-style")
            if nat_lang_doc:
                sections.append(nat_lang_doc)

        if profile.tier == "large":
            if t_lower in ("coding", "debugging", "architecture", "testing"):
                std_doc = self.load_knowledge_module("programming-standards")
                if std_doc:
                    sections.append(std_doc)
            elif t_lower == "writing":
                doc_std = self.load_knowledge_module("documentation")
                if doc_std:
                    sections.append(doc_std)

        # 6. Optional Deliverable Template
        if include_template:
            tpl_doc = self.load_template(include_template)
            if tpl_doc:
                sections.append(tpl_doc)

        # 7. Self-Verification Directive
        verif_doc = self.load_intelligence_module("verification")
        if verif_doc:
            sections.append(verif_doc)

        # 8. Injected Project Memory (if provided)
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
                f"for tier '{profile.tier}'. Applying progressive trimming."
            )
            trimmed_sections = [sections[0]]
            if agent_content:
                trimmed_sections.append(agent_content)
            if verif_doc and profile.tier != "small":
                trimmed_sections.append(verif_doc)
            if context_memory:
                trimmed_sections.append(context_memory)
            compressed = self.adaptive_engine.compress_prompt("\n\n---\n\n".join(trimmed_sections), profile.tier)

        return compressed
