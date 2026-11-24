"""
SQLite External Memory Engine for Frontier Intelligence Engine (FIE).
Provides structured, persistent storage for sessions, conversation messages,
task execution ledgers, and key-value project facts with relevance retrieval
and automatic secret redaction.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Iterator
import sqlite3
import json
import re
import logging
from contextlib import contextmanager

logger = logging.getLogger("fie.memory")

class SQLiteMemory:
    """Manages persistent external memory with SQLite backend."""

    SENSITIVE_VALUE_PATTERNS = [
        re.compile(r"AIza[0-9A-Za-z\-_]{20,}"),
        re.compile(r"sk-[0-9A-Za-z]{20,}"),
        re.compile(r"ghp_[0-9A-Za-z]{20,}"),
        re.compile(r"(?i)(?:bearer\s+)[0-9A-Za-z\-_\.]{20,}"),
        re.compile(r"(?i)(?:password|passwd|secret|api_key)\s*[:=]\s*['\"]?[^\s'\"]{6,}['\"]?")
    ]

    def __init__(self, db_path: Optional[str] = None) -> None:
        if db_path is None:
            # Default to local database in root project directory
            base_dir = Path(__file__).resolve().parent.parent.parent
            self.db_path = str(base_dir / "fie_memory.db")
        else:
            self.db_path = str(db_path)

        self._init_db()

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        """Initializes tables and indexes idempotently."""
        with self._connection() as conn:
            cursor = conn.cursor()

            # Sessions Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS fie_sessions (
                session_id TEXT PRIMARY KEY,
                project_name TEXT NOT NULL,
                model_profile TEXT NOT NULL DEFAULT 'medium',
                user_preferences TEXT DEFAULT '{}',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # Conversation Messages Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS fie_messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                agent_name TEXT DEFAULT 'system',
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(session_id) REFERENCES fie_sessions(session_id)
            );
            """)

            # Task History Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS fie_tasks (
                task_id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                task_type TEXT NOT NULL,
                assigned_agent TEXT NOT NULL,
                status TEXT NOT NULL,
                input_payload TEXT,
                output_result TEXT,
                verification_status TEXT DEFAULT 'UNTESTED',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(session_id) REFERENCES fie_sessions(session_id)
            );
            """)

            # Project Facts & Knowledge Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS fie_project_facts (
                fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                category TEXT NOT NULL,
                fact_key TEXT NOT NULL,
                fact_value TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(session_id) REFERENCES fie_sessions(session_id),
                UNIQUE(session_id, fact_key)
            );
            """)

            # Indexes for high-speed queries
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_session ON fie_messages(session_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_session ON fie_tasks(session_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_facts_session ON fie_project_facts(session_id, category);")
            conn.commit()

    @classmethod
    def redact_sensitive_text(cls, value: str) -> str:
        """Redacts raw API keys, tokens, or password assignments before persistence."""
        redacted = value
        for pattern in cls.SENSITIVE_VALUE_PATTERNS:
            redacted = pattern.sub("[REDACTED_CREDENTIAL]", redacted)
        return redacted

    # ---------------- Session Operations ---------------- #

    def create_or_get_session(
        self,
        session_id: str,
        project_name: str = "Default Project",
        model_profile: str = "medium",
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Creates a session if it does not exist, or updates its profile."""
        prefs_json = json.dumps(user_preferences or {})
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO fie_sessions (session_id, project_name, model_profile, user_preferences)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    project_name = excluded.project_name,
                    model_profile = excluded.model_profile,
                    updated_at = CURRENT_TIMESTAMP;
                """,
                (session_id, project_name, model_profile, prefs_json)
            )
            conn.commit()
            cursor.execute("SELECT * FROM fie_sessions WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            return dict(row) if row else {}

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fie_sessions WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def list_sessions(self) -> List[Dict[str, Any]]:
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fie_sessions ORDER BY updated_at DESC")
            return [dict(r) for r in cursor.fetchall()]

    def clear_session(self, session_id: str) -> bool:
        """Cleans all messages, tasks, and facts belonging to a session."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM fie_messages WHERE session_id = ?", (session_id,))
            cursor.execute("DELETE FROM fie_tasks WHERE session_id = ?", (session_id,))
            cursor.execute("DELETE FROM fie_project_facts WHERE session_id = ?", (session_id,))
            cursor.execute("DELETE FROM fie_sessions WHERE session_id = ?", (session_id,))
            conn.commit()
            return True

    # ---------------- Message & Rolling Window Operations ---------------- #

    def record_message(
        self,
        session_id: str,
        role: str,
        content: str,
        agent_name: str = "system"
    ) -> int:
        """Records a conversation or agent interaction turn with credential redaction."""
        safe_content = self.redact_sensitive_text(content)
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO fie_messages (session_id, role, agent_name, content)
                VALUES (?, ?, ?, ?)
                """,
                (session_id, role.lower(), agent_name.lower(), safe_content)
            )
            conn.commit()
            return int(cursor.lastrowid or 0)

    def get_messages(self, session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Returns the most recent messages for a session in chronological order."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM (
                    SELECT * FROM fie_messages
                    WHERE session_id = ?
                    ORDER BY message_id DESC
                    LIMIT ?
                ) ORDER BY message_id ASC
                """,
                (session_id, limit)
            )
            return [dict(r) for r in cursor.fetchall()]

    # ---------------- Task Operations ---------------- #

    def record_task(
        self,
        task_id: str,
        session_id: str,
        task_type: str,
        assigned_agent: str,
        status: str = "PENDING",
        input_payload: Optional[str] = None,
        output_result: Optional[str] = None,
        verification_status: str = "UNTESTED"
    ) -> None:
        """Records or updates a task in the execution ledger."""
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO fie_tasks 
                (task_id, session_id, task_type, assigned_agent, status, input_payload, output_result, verification_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(task_id) DO UPDATE SET
                    status = excluded.status,
                    output_result = excluded.output_result,
                    verification_status = excluded.verification_status;
                """,
                (task_id, session_id, task_type, assigned_agent, status, input_payload, output_result, verification_status)
            )
            conn.commit()

    def get_tasks_for_session(self, session_id: str) -> List[Dict[str, Any]]:
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fie_tasks WHERE session_id = ? ORDER BY created_at ASC", (session_id,))
            return [dict(r) for r in cursor.fetchall()]

    # ---------------- Project Facts & Relevance Retrieval ---------------- #

    def set_fact(
        self,
        session_id: str,
        category: str,
        fact_key: str,
        fact_value: str,
        confidence: float = 1.0
    ) -> None:
        """Stores a key fact about the project with automatic credential redaction."""
        safe_value = self.redact_sensitive_text(fact_value)
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO fie_project_facts (session_id, category, fact_key, fact_value, confidence)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(session_id, fact_key) DO UPDATE SET
                    category = excluded.category,
                    fact_value = excluded.fact_value,
                    confidence = excluded.confidence,
                    created_at = CURRENT_TIMESTAMP;
                """,
                (session_id, category.upper(), fact_key, safe_value, confidence)
            )
            conn.commit()

    def get_all_facts(self, session_id: str) -> List[Dict[str, Any]]:
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM fie_project_facts WHERE session_id = ? ORDER BY category ASC, fact_key ASC",
                (session_id,)
            )
            return [dict(r) for r in cursor.fetchall()]

    def get_facts_by_category(self, session_id: str, category: str) -> List[Dict[str, Any]]:
        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM fie_project_facts WHERE session_id = ? AND category = ? ORDER BY fact_key ASC",
                (session_id, category.upper())
            )
            return [dict(r) for r in cursor.fetchall()]

    def search_facts(self, session_id: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves facts based on token overlap / relevance search against fact_key and fact_value.
        """
        tokens = [t.strip().lower() for t in re.split(r"\W+", query) if len(t.strip()) > 2]
        if not tokens:
            with self._connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM fie_project_facts WHERE session_id = ? LIMIT ?",
                    (session_id, limit)
                )
                return [dict(r) for r in cursor.fetchall()]

        with self._connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM fie_project_facts WHERE session_id = ?", (session_id,))
            all_facts = [dict(r) for r in cursor.fetchall()]

        # Score by token occurrence in key and value
        scored: List[Tuple[float, Dict[str, Any]]] = []
        for fact in all_facts:
            score = 0.0
            text_target = f"{fact['fact_key']} {fact['fact_value']} {fact['category']}".lower()
            for token in tokens:
                if token in text_target:
                    score += 1.0
                    if token in fact["fact_key"].lower():
                        score += 1.5
            if score > 0:
                scored.append((score, fact))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:limit]]

    def get_project_context_summary(self, session_id: str, query: Optional[str] = None) -> str:
        """
        Builds a compact summary block (< 400 tokens) of key facts for prompt injection.
        """
        if query:
            facts = self.search_facts(session_id, query, limit=6)
            if not facts:
                facts = self.get_all_facts(session_id)[:6]
        else:
            facts = self.get_all_facts(session_id)[:6]

        if not facts:
            return "No prior project memory recorded."

        lines = ["--- PROJECT MEMORY LEDGER ---"]
        for f in facts:
            lines.append(f"- [{f['category']}] {f['fact_key']}: {f['fact_value']}")
        lines.append("-----------------------------")
        return "\n".join(lines)

    def export_session(self, session_id: str) -> Dict[str, Any]:
        """Exports complete session metadata, facts, tasks, and recent messages."""
        return {
            "session": self.get_session(session_id),
            "facts": self.get_all_facts(session_id),
            "tasks": self.get_tasks_for_session(session_id),
            "messages": self.get_messages(session_id, limit=50)
        }

    def get_memory_stats(self) -> Dict[str, int]:
        """Returns aggregate record counts across all SQLite memory tables."""
        with self._connection() as conn:
            cursor = conn.cursor()
            stats = {}
            for table in ("fie_sessions", "fie_messages", "fie_tasks", "fie_project_facts"):
                cursor.execute(f"SELECT COUNT(*) AS cnt FROM {table}")
                row = cursor.fetchone()
                stats[table] = int(row["cnt"]) if row else 0
            return stats
