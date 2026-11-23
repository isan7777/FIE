"""
Unit tests for FIE SQLite Memory Subsystem.
"""

import unittest
import tempfile
import os
from fie.memory.sqlite_memory import SQLiteMemory

class TestSQLiteMemory(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.memory = SQLiteMemory(db_path=self.temp_db.name)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_session_lifecycle(self):
        session = self.memory.create_or_get_session("sess_01", "Project Alpha", "small")
        self.assertEqual(session["session_id"], "sess_01")
        self.assertEqual(session["project_name"], "Project Alpha")
        self.assertEqual(session["model_profile"], "small")

        retrieved = self.memory.get_session("sess_01")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["session_id"], "sess_01")

    def test_task_recording(self):
        self.memory.create_or_get_session("sess_02")
        self.memory.record_task(
            task_id="t1",
            session_id="sess_02",
            task_type="coding",
            assigned_agent="coder",
            status="IN_PROGRESS"
        )
        self.memory.record_task(
            task_id="t1",
            session_id="sess_02",
            task_type="coding",
            assigned_agent="coder",
            status="COMPLETED",
            output_result="def hello(): pass",
            verification_status="SYNTAX_PASSED"
        )
        tasks = self.memory.get_tasks_for_session("sess_02")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["status"], "COMPLETED")
        self.assertEqual(tasks[0]["verification_status"], "SYNTAX_PASSED")

    def test_fact_storage_and_relevance_search(self):
        self.memory.create_or_get_session("sess_03")
        self.memory.set_fact("sess_03", "ARCHITECTURE", "database", "PostgreSQL with connection pool")
        self.memory.set_fact("sess_03", "SECURITY", "auth", "OAuth2 with PKCE")

        # Search by relevance
        results = self.memory.search_facts("sess_03", "Which database is used?", limit=5)
        self.assertTrue(len(results) >= 1)
        self.assertEqual(results[0]["fact_key"], "database")
        self.assertIn("PostgreSQL", results[0]["fact_value"])

        # Summary check
        summary = self.memory.get_project_context_summary("sess_03")
        self.assertIn("PROJECT MEMORY LEDGER", summary)
        self.assertIn("database", summary)

    def test_session_clear(self):
        self.memory.create_or_get_session("sess_04")
        self.memory.set_fact("sess_04", "GENERAL", "k", "v")
        self.memory.record_task("t_clear", "sess_04", "type", "agent")
        
        self.memory.clear_session("sess_04")
        self.assertIsNone(self.memory.get_session("sess_04"))
        self.assertEqual(len(self.memory.get_tasks_for_session("sess_04")), 0)

if __name__ == "__main__":
    unittest.main()
