"""
Master Orchestrator for Frontier Intelligence Engine (FIE).
Classifies requests, determines complexity, schedules sequential agent pipelines,
coordinates memory and verification, and triggers autonomous self-correction.
"""

from typing import Any, Dict, List, Optional
import uuid
import logging
from fie.config import FIEConfig
from fie.memory.sqlite_memory import SQLiteMemory
from fie.core.loader import ModularPromptLoader
from fie.core.adaptive import AdaptiveModelEngine
from fie.verification.engine import VerificationEngine
from fie.api.gemini_client import GeminiClient

logger = logging.getLogger("fie.orchestrator")

class MasterOrchestrator:
    """Central executive agent coordinating multi-agent workflows."""

    def __init__(
        self,
        config: Optional[FIEConfig] = None,
        memory: Optional[SQLiteMemory] = None,
        loader: Optional[ModularPromptLoader] = None,
        verifier: Optional[VerificationEngine] = None,
        client: Optional[GeminiClient] = None
    ) -> None:
        self.config = config or FIEConfig()
        self.memory = memory or SQLiteMemory()
        self.loader = loader or ModularPromptLoader()
        self.adaptive = AdaptiveModelEngine()
        self.verifier = verifier or VerificationEngine()
        self.client = client or GeminiClient(self.config)

    def classify_task(self, prompt: str) -> Dict[str, Any]:
        """
        Classifies task type and computes complexity score (1 to 10) using weighted domain scores.
        """
        p_lower = prompt.lower()

        domain_keywords = {
            "debugging": ["bug", "error", "trace", "crash", "fix", "exception", "regresi", "memperbaiki bug", "recursionserror"],
            "research": ["riset", "paper", "investigasi", "analisis literatur", "grounding", "fakta", "penelitian", "studi pustaka", "literature review"],
            "architecture": ["arsitektur", "rancang sistem", "arsitektur software", "schema", "database design", "high-level design"],
            "coding": ["code", "script", "fungsi", "endpoint", "api", "buatkan program", "class", "implementasi", "coding", "refactoring"],
            "design": ["ui", "ux", "tampilan", "desain", "css", "layout", "komponen", "antarmuka"],
            "analysis": ["hitung", "matematika", "analisis data", "metrik", "statistik", "kuantitatif", "perhitungan"],
            "writing": ["tulis", "artikel", "dokumentasi", "readme", "panduan", "naskah", "laporan"]
        }

        # Calculate score per domain
        scores: Dict[str, int] = {domain: 0 for domain in domain_keywords}
        for domain, kws in domain_keywords.items():
            for kw in kws:
                if kw in p_lower:
                    # Give higher weight to explicit intent verbs
                    weight = 2 if p_lower.startswith(kw) or f" {kw} " in f" {p_lower} " else 1
                    scores[domain] += weight

        # Pick highest scoring domain (if tied or 0, default to general or highest non-zero)
        sorted_domains = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_domain, top_score = sorted_domains[0]
        task_type = top_domain if top_score > 0 else "general"

        # Complexity baseline
        base_complexity = {
            "general": 3,
            "writing": 4,
            "design": 5,
            "debugging": 6,
            "coding": 6,
            "analysis": 6,
            "research": 7,
            "architecture": 8
        }
        complexity = base_complexity.get(task_type, 5)

        # Complexity adjustments
        if any(w in p_lower for w in ["end-to-end", "skala besar", "produksi", "komprehensif", "lengkap"]):
            complexity = min(10, complexity + 3)
        if len(prompt) > 500:
            complexity = min(10, complexity + 1)

        return {
            "task_type": task_type,
            "complexity": complexity
        }

    def determine_pipeline(self, task_type: str, complexity: int, model_tier: str) -> List[str]:
        """
        Selects the sequential chain of agents based on task and model profile.
        """
        if model_tier == "small" or complexity <= 3:
            # Serial single-agent for small models or low complexity
            single_map = {
                "coding": ["coder"],
                "debugging": ["debugger"],
                "research": ["researcher"],
                "architecture": ["architect"],
                "design": ["designer"],
                "analysis": ["analyst"],
                "writing": ["writer"]
            }
            return single_map.get(task_type, ["coder"])

        # Medium / Large pipelines
        pipelines = {
            "coding": ["architect", "coder", "tester"],
            "debugging": ["debugger", "coder", "tester"],
            "architecture": ["architect", "analyst", "writer"],
            "research": ["researcher", "analyst", "writer"],
            "design": ["designer", "coder", "tester"],
            "analysis": ["analyst", "writer"],
            "writing": ["researcher", "writer"]
        }
        return pipelines.get(task_type, ["architect", "coder", "tester"])

    def execute_workflow(
        self,
        task_prompt: str,
        session_id: Optional[str] = None,
        model_tier: str = "medium"
    ) -> Dict[str, Any]:
        """
        Orchestrates an end-to-end task through the specialist agent pipeline.
        """
        session_id = session_id or f"session_{uuid.uuid4().hex[:8]}"
        self.memory.create_or_get_session(session_id, project_name=task_prompt[:30], model_profile=model_tier)

        classification = self.classify_task(task_prompt)
        task_type = classification["task_type"]
        complexity = classification["complexity"]
        pipeline = self.determine_pipeline(task_type, complexity, model_tier)

        logger.info(f"Session {session_id}: Task '{task_type}' (Complexity: {complexity}), Pipeline: {pipeline}")

        # Retrieve relevant project memory
        context_memory = self.memory.get_project_context_summary(session_id, query=task_prompt)

        pipeline_results: List[Dict[str, Any]] = []
        current_context = task_prompt
        overall_status = "VERIFIED"

        for step_idx, agent_name in enumerate(pipeline, start=1):
            task_id = f"{session_id}_step_{step_idx}_{agent_name}"
            self.memory.record_task(
                task_id=task_id,
                session_id=session_id,
                task_type=task_type,
                assigned_agent=agent_name,
                status="IN_PROGRESS",
                input_payload=current_context
            )

            # Compile prompt for the specific agent
            system_inst = self.loader.compile_system_instruction(
                task_type=task_type,
                model_profile_tier=model_tier,
                active_agent=agent_name,
                context_memory=context_memory
            )

            # Generate response through client
            step_resp = self.client.generate_response(
                prompt=f"Task for Agent [{agent_name.upper()}]:\n{current_context}",
                system_instruction=system_inst
            )
            step_output = step_resp.get("text", "")

            # Perform verification
            if "def " in step_output or "class " in step_output:
                verif = self.verifier.verify_python_code(step_output)
            else:
                verif = self.verifier.verify_text_deliverable(step_output)

            verif_status = verif["status"]
            if verif_status in ["FAILED", "NEEDS_REVIEW"] and overall_status == "VERIFIED":
                overall_status = verif_status

            self.memory.record_task(
                task_id=task_id,
                session_id=session_id,
                task_type=task_type,
                assigned_agent=agent_name,
                status="COMPLETED",
                output_result=step_output,
                verification_status=verif_status
            )

            pipeline_results.append({
                "step": step_idx,
                "agent": agent_name,
                "verification": verif,
                "output": step_output
            })

            # Feed forward to next agent
            current_context = (
                f"Previous Step Output from [{agent_name.upper()}]:\n"
                f"{step_output[:1200]}\n\n"
                f"Original User Goal:\n{task_prompt}"
            )

        # Store key architectural fact if relevant
        self.memory.set_fact(
            session_id=session_id,
            category="TASK_RECORD",
            fact_key=f"completed_{task_type}",
            fact_value=f"Pipeline {pipeline} executed with final status {overall_status}."
        )

        return {
            "session_id": session_id,
            "task_type": task_type,
            "complexity": complexity,
            "model_tier": model_tier,
            "pipeline": pipeline,
            "final_status": overall_status,
            "steps": pipeline_results
        }
