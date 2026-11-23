"""
Adaptive Model Engine for Frontier Intelligence Engine (FIE).
Dynamically adjusts instruction length, task decomposition granularity,
token budgets, and verification intensity across Small, Medium, and Large models.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional
import re
import logging

logger = logging.getLogger("fie.adaptive")

@dataclass
class ModelProfile:
    tier: str
    name: str
    max_context_window: int
    max_instruction_tokens: int
    decomposition_granularity: str
    chaining_mode: str
    max_tools_per_turn: int
    reasoning_verbosity: str
    verification_intensity: str
    prompt_compression_level: str
    use_few_shot_examples: bool

class AdaptiveModelEngine:
    """Manages model profiles and adapts prompts and execution strategies accordingly."""

    DEFAULTS = {
        "small": ModelProfile(
            tier="small",
            name="Small Model (Flash-Lite / Sub-8B)",
            max_context_window=8192,
            max_instruction_tokens=1200,
            decomposition_granularity="fine-grained",
            chaining_mode="serial_single_agent",
            max_tools_per_turn=1,
            reasoning_verbosity="minimal",
            verification_intensity="syntax_and_null_checks",
            prompt_compression_level="high",
            use_few_shot_examples=True
        ),
        "medium": ModelProfile(
            tier="medium",
            name="Medium Model (Flash / 12B-30B)",
            max_context_window=32768,
            max_instruction_tokens=3500,
            decomposition_granularity="medium_staged",
            chaining_mode="sequential_pipeline",
            max_tools_per_turn=3,
            reasoning_verbosity="structured",
            verification_intensity="contract_and_unit_tests",
            prompt_compression_level="balanced",
            use_few_shot_examples=True
        ),
        "large": ModelProfile(
            tier="large",
            name="Large Model (Pro / Ultra / 70B+)",
            max_context_window=128000,
            max_instruction_tokens=16000,
            decomposition_granularity="holistic_strategic",
            chaining_mode="full_agent_mesh",
            max_tools_per_turn=10,
            reasoning_verbosity="deep_analytical",
            verification_intensity="comprehensive_audit_and_fuzzing",
            prompt_compression_level="none",
            use_few_shot_examples=False
        )
    }

    def __init__(self, custom_profiles: Optional[Dict[str, Any]] = None) -> None:
        self.profiles: Dict[str, ModelProfile] = dict(self.DEFAULTS)
        if custom_profiles:
            self._load_custom(custom_profiles)

    def _load_custom(self, data: Dict[str, Any]) -> None:
        for tier, conf in data.items():
            if isinstance(conf, dict):
                self.profiles[tier] = ModelProfile(
                    tier=tier,
                    name=conf.get("name", f"{tier.capitalize()} Model"),
                    max_context_window=conf.get("max_context_window", 16384),
                    max_instruction_tokens=conf.get("max_instruction_tokens", 2500),
                    decomposition_granularity=conf.get("decomposition_granularity", "medium_staged"),
                    chaining_mode=conf.get("chaining_mode", "sequential_pipeline"),
                    max_tools_per_turn=conf.get("max_tools_per_turn", 2),
                    reasoning_verbosity=conf.get("reasoning_verbosity", "structured"),
                    verification_intensity=conf.get("verification_intensity", "contract_and_unit_tests"),
                    prompt_compression_level=conf.get("prompt_compression_level", "balanced"),
                    use_few_shot_examples=conf.get("use_few_shot_examples", True)
                )

    def get_profile(self, tier: str = "medium") -> ModelProfile:
        tier_normalized = tier.strip().lower()
        if tier_normalized not in self.profiles:
            logger.warning(f"Unknown tier '{tier}'. Falling back to 'medium'.")
            return self.profiles["medium"]
        return self.profiles[tier_normalized]

    def compress_prompt(self, text: str, tier: str) -> str:
        """
        Compresses prompt text based on profile tier to respect token limits.
        Removes markdown comments, excessive empty lines, and redundant filler words.
        """
        profile = self.get_profile(tier)
        if profile.prompt_compression_level == "none":
            return text

        # Strip markdown comments <!-- ... -->
        cleaned = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        
        # Collapse multiple blank lines to a single blank line
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

        if profile.prompt_compression_level == "high":
            # For small models: Strip verbose explanations and keep action items
            lines = []
            for line in cleaned.splitlines():
                stripped = line.strip()
                # Skip decorative banners or lines that add no imperative value
                if stripped.startswith("---") and len(stripped) > 5:
                    continue
                lines.append(line)
            cleaned = "\n".join(lines)

        return cleaned.strip()

    def estimate_token_count(self, text: str) -> int:
        """
        Rough heuristic token estimator (~4 characters per token for English/Code,
        ~3 characters per token for Indonesian / multilingual text).
        """
        if not text:
            return 0
        return max(1, int(len(text) / 3.5))
