"""
Master Orchestrator for Frontier Intelligence Engine (FIE).
Classifies requests, determines complexity and engineering domains, schedules sequential
agent pipelines, coordinates memory and verification, and triggers autonomous self-correction.
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
        self.loader = loader or ModularPromptLoader(config=self.config)
        self.adaptive = self.loader.adaptive_engine
        self.verifier = verifier or VerificationEngine()
        self.client = client or GeminiClient(self.config)

    def detect_engineering_domain(self, prompt: str, task_type: str) -> Optional[str]:
        """Detects the specific engineering playbook domain from prompt cues."""
        p_lower = prompt.lower()
        playbook_keywords = {
            "database": ["sql", "sqlite", "postgres", "ddl", "schema", "tabel", "query", "index", "migration", "database"],
            "frontend": ["react", "nextjs", "tailwind", "css", "html", "dom", "komponen ui", "frontend", "responsive", "wcag"],
            "game-development": ["game", "unity", "ecs", "frame rate", "physics", "shader", "object pool", "state machine"],
            "security": ["jwt", "oauth", "auth", "enkripsi", "owasp", "xss", "csrf", "injection", "keamanan", "security", "argon2"],
            "performance": ["latency", "optimasi", "cache", "lru", "memory leak", "profiling", "throughput", "concurrency", "performa"],
            "api-integration": ["rest api", "webhook", "graphql", "grpc", "endpoint", "http client", "circuit breaker"],
            "ai-llm-engineering": ["llm", "gemini", "prompt", "rag", "agent", "embedding", "token", "function calling", "ai"],
            "software-architecture": ["clean architecture", "hexagonal", "microservice", "monolith", "solid", "arsitektur"],
            "backend": ["fastapi", "flask", "django", "service", "backend", "worker", "queue"]
        }
        best_domain: Optional[str] = None
        best_score = 0
        for domain, kws in playbook_keywords.items():
            score = sum(1 for kw in kws if kw in p_lower)
            if score > best_score:
                best_score = score
                best_domain = domain

        if best_domain:
            return best_domain

        fallback = {
            "coding": "backend",
            "architecture": "software-architecture",
            "design": "frontend",
            "debugging": "performance"
        }
        return fallback.get(task_type)

    def classify_task(self, prompt: str) -> Dict[str, Any]:
        """
        Classifies task type, sub-domain, and computes complexity score (1 to 10) using weighted domain scores.
        """
        p_lower = prompt.lower()

        domain_keywords = {
            "debugging": ["bug", "error", "trace", "crash", "fix", "exception", "regresi", "memperbaiki", "recursionerror", "indexerror", "keyerror"],
            "research": ["riset", "paper", "investigasi", "analisis literatur", "grounding", "fakta", "penelitian", "studi pustaka", "literature review"],
            "architecture": ["arsitektur", "rancang sistem", "arsitektur software", "schema", "database design", "high-level design", "rancang skema"],
            "coding": ["code", "script", "fungsi", "endpoint", "api", "buatkan program", "buatkan fungsi", "class", "implementasi", "coding", "refactoring"],
            "design": ["ui", "ux", "tampilan", "desain", "css", "layout", "komponen", "antarmuka", "wireframe"],
            "analysis": ["hitung", "matematika", "analisis data", "metrik", "statistik", "kuantitatif", "perhitungan", "benchmark"],
            "writing": ["tulis", "artikel", "dokumentasi", "readme", "panduan", "naskah", "laporan", "changelog"]
        }

        scores: Dict[str, int] = {domain: 0 for domain in domain_keywords}
        for domain, kws in domain_keywords.items():
            for kw in kws:
                if kw in p_lower:
                    weight = 2 if p_lower.startswith(kw) or f" {kw} " in f" {p_lower} " else 1
                    scores[domain] += weight

        sorted_domains = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_domain, top_score = sorted_domains[0]
        task_type = top_domain if top_score > 0 else "general"

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

        if any(w in p_lower for w in ["end-to-end", "skala besar", "produksi", "komprehensif", "lengkap", "distributed", "multi-agent"]):
            complexity = min(10, complexity + 3)
        if len(prompt) > 500:
            complexity = min(10, complexity + 1)

        engineering_domain = self.detect_engineering_domain(prompt, task_type)

        return {
            "task_type": task_type,
            "complexity": complexity,
            "engineering_domain": engineering_domain
        }

    def determine_pipeline(self, task_type: str, complexity: int, model_tier: str) -> List[str]:
        """
        Selects the sequential chain of agents based on task and model profile.
        """
        if model_tier == "small" or complexity <= 3:
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

    def _run_step_with_self_correction(
        self,
        agent_name: str,
        current_context: str,
        system_inst: str,
        max_attempts: int = 2
    ) -> Dict[str, Any]:
        """
        Executes an agent generation step and performs autonomous self-correction
        (up to max_attempts retries) if verification detects issues or style violations.
        """
        attempts = 0
        correction_history: List[Dict[str, Any]] = []
        prompt_payload = f"Task for Agent [{agent_name.upper()}]:\n{current_context}"
        step_output = ""
        verif: Dict[str, Any] = {}

        while attempts <= max_attempts:
            attempts += 1
            step_resp = self.client.generate_response(
                prompt=prompt_payload,
                system_instruction=system_inst
            )
            step_output = step_resp.get("text", "")

            # Auto-sanitize emoji policy violations if configured
            if self.config.get_setting("verification.reject_emojis_in_deliverables", True):
                if self.verifier.EMOJI_PATTERN.search(step_output):
                    step_output = self.verifier.sanitize_emojis(step_output)

            verif = self.verifier.verify_deliverable(step_output)
            verif_status = verif.get("status", "UNTESTED")
            issues = verif.get("issues", [])
            warnings = verif.get("warnings", [])

            if verif_status in ("VERIFIED", "SYNTAX_PASSED") and not issues:
                break

            correction_history.append({
                "attempt": attempts,
                "status": verif_status,
                "issues": issues,
                "warnings": warnings
            })

            if attempts > max_attempts:
                logger.warning(
                    f"Agent [{agent_name}] reached max self-correction attempts ({max_attempts}). "
                    f"Proceeding with status '{verif_status}'."
                )
                break

            feedback_items = issues + warnings
            feedback_str = "\n".join(f"- {item}" for item in feedback_items)
            prompt_payload = (
                f"Task for Agent [{agent_name.upper()}] (SELF-CORRECTION ATTEMPT {attempts}/{max_attempts}):\n"
                f"Your previous output failed verification with the following findings:\n"
                f"{feedback_str}\n\n"
                f"Fix all issues above and provide a complete, verified deliverable for:\n"
                f"{current_context}"
            )

        return {
            "output": step_output,
            "verification": verif,
            "attempts": attempts,
            "correction_history": correction_history
        }

    def execute_workflow(
        self,
        task_prompt: str,
        session_id: Optional[str] = None,
        model_tier: str = "medium"
    ) -> Dict[str, Any]:
        """
        Orchestrates an end-to-end task through the specialist agent pipeline
        with persistent memory tracking and autonomous self-correction.
        """
        session_id = session_id or f"session_{uuid.uuid4().hex[:8]}"
        self.memory.create_or_get_session(session_id, project_name=task_prompt[:40], model_profile=model_tier)
        self.memory.record_message(session_id, role="user", content=task_prompt, agent_name="user")

        classification = self.classify_task(task_prompt)
        task_type = classification["task_type"]
        complexity = classification["complexity"]
        engineering_domain = classification.get("engineering_domain")
        pipeline = self.determine_pipeline(task_type, complexity, model_tier)

        max_corrections = int(self.config.get_setting("orchestration.max_self_correction_attempts", 2))

        logger.info(
            f"Session {session_id}: Task '{task_type}' (Domain: {engineering_domain}, "
            f"Complexity: {complexity}), Pipeline: {pipeline}"
        )

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

            system_inst = self.loader.compile_system_instruction(
                task_type=task_type,
                model_profile_tier=model_tier,
                active_agent=agent_name,
                context_memory=context_memory,
                domain_hint=engineering_domain
            )

            step_exec = self._run_step_with_self_correction(
                agent_name=agent_name,
                current_context=current_context,
                system_inst=system_inst,
                max_attempts=max_corrections
            )

            step_output = step_exec["output"]
            verif = step_exec["verification"]
            verif_status = verif["status"]

            if verif_status in ("FAILED", "NEEDS_REVIEW") and overall_status == "VERIFIED":
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
            self.memory.record_message(
                session_id=session_id,
                role="assistant",
                content=step_output,
                agent_name=agent_name
            )

            pipeline_results.append({
                "step": step_idx,
                "agent": agent_name,
                "attempts": step_exec["attempts"],
                "verification": verif,
                "output": step_output
            })

            current_context = (
                f"Previous Step Output from [{agent_name.upper()}]:\n"
                f"{step_output[:1500]}\n\n"
                f"Original User Goal:\n{task_prompt}"
            )

        self.memory.set_fact(
            session_id=session_id,
            category="TASK_RECORD",
            fact_key=f"completed_{task_type}",
            fact_value=f"Pipeline {pipeline} executed with final status {overall_status}."
        )

        return {
            "session_id": session_id,
            "task_type": task_type,
            "engineering_domain": engineering_domain,
            "complexity": complexity,
            "model_tier": model_tier,
            "pipeline": pipeline,
            "final_status": overall_status,
            "steps": pipeline_results
        }
