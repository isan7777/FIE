"""
Configuration Loader for Frontier Intelligence Engine (FIE).
Loads YAML configuration files with resilient defaults and environment variable overrides.
"""

from pathlib import Path
from typing import Any, Dict, Optional
import os
import yaml
import logging

logger = logging.getLogger("fie.config")

class FIEConfig:
    """Manages system settings, model profiles, and tool permissions."""

    def __init__(self, base_dir: Optional[Path] = None) -> None:
        if base_dir is None:
            # Default to root of FRONTIER-INTELLIGENCE-ENGINE
            self.base_dir = Path(__file__).resolve().parent.parent
        else:
            self.base_dir = Path(base_dir).resolve()

        self.config_dir = self.base_dir / "config"
        self.settings: Dict[str, Any] = self._load_yaml("settings.yaml")
        self.model_profiles: Dict[str, Any] = self._load_yaml("model-profiles.yaml")
        self.tool_permissions: Dict[str, Any] = self._load_yaml("tool-permissions.yaml")

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        file_path = self.config_dir / filename
        if not file_path.exists():
            logger.warning(f"Config file not found: {file_path}. Using empty default.")
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f)
                return content or {}
        except Exception as e:
            logger.error(f"Failed to load {filename}: {e}. Falling back to empty dict.")
            return {}

    def get_setting(self, path: str, default: Any = None) -> Any:
        """Retrieves a nested setting using dot notation (e.g. 'memory.backend')."""
        keys = path.split(".")
        current: Any = self.settings
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return default
        return current

    def get_model_profile(self, tier: str = "medium") -> Dict[str, Any]:
        """Returns the configuration profile for 'small', 'medium', or 'large'."""
        profiles = self.model_profiles.get("profiles", {})
        tier_key = tier.lower()
        if tier_key in profiles:
            return profiles[tier_key]
        logger.warning(f"Profile '{tier}' not found. Defaulting to 'medium'.")
        return profiles.get("medium", {})

    def get_tool_permission(self, tool_name: str) -> Dict[str, Any]:
        """Returns permission config for a tool category."""
        return self.tool_permissions.get("permissions", {}).get(tool_name, {})

    @property
    def gemini_api_key(self) -> Optional[str]:
        """Safely gets Gemini API Key from environment."""
        return os.environ.get("GEMINI_API_KEY")
