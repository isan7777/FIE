"""
Frontier Intelligence Engine (FIE)
One Framework. Universal Capabilities. Engineered for Execution.
"""

__version__ = "1.0.0"
__author__ = "Frontier Intelligence Engine Team"

from fie.config import FIEConfig
from fie.memory.sqlite_memory import SQLiteMemory
from fie.core.loader import ModularPromptLoader
from fie.core.adaptive import AdaptiveModelEngine
from fie.core.orchestrator import MasterOrchestrator
from fie.verification.engine import VerificationEngine

__all__ = [
    "FIEConfig",
    "SQLiteMemory",
    "ModularPromptLoader",
    "AdaptiveModelEngine",
    "MasterOrchestrator",
    "VerificationEngine",
]
