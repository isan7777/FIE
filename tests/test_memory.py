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

    def test_message_recording_and_redaction(self):
        self.memory.create_or_get_session("sess_msg")
        self.memory.record_message("sess_msg", "user", "Use key AIzaSySecretKeyValue1234567890", "user")
        self.memory.record_message("sess_msg", "assistant", "Configured securely.", "coder")

        msgs = self.memory.get_messages("sess_msg")
        self.assertEqual(len(msgs), 2)
        self.assertIn("[REDACTED_CREDENTIAL]", msgs[0]["content"])
        self.assertNotIn("AIzaSySecretKeyValue1234567890", msgs[0]["content"])

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
            output_result="def hello(): return 'ok'",
            verification_status="SYNTAX_PASSED"
        )
        tasks = self.memory.get_tasks_for_session("sess_02")
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["status"], "COMPLETED")
        self.assertEqual(tasks[0]["verification_status"], "SYNTAX_PASSED")

    def test_fact_storage_relevance_and_redaction(self):
        self.memory.create_or_get_session("sess_03")
        self.memory.set_fact("sess_03", "ARCHITECTURE", "database", "PostgreSQL with connection pool")
        self.memory.set_fact("sess_03", "SECURITY", "auth", "OAuth2 with PKCE")
        self.memory.set_fact("sess_03", "SECURITY", "secret_cfg", "password=SuperSecretPassword123")

        results = self.memory.search_facts("sess_03", "Which database is used?", limit=5)
        self.assertTrue(len(results) >= 1)
        self.assertEqual(results[0]["fact_key"], "database")
        self.assertIn("PostgreSQL", results[0]["fact_value"])

        sec_facts = self.memory.get_facts_by_category("sess_03", "SECURITY")
        secret_entry = [f for f in sec_facts if f["fact_key"] == "secret_cfg"][0]
        self.assertIn("[REDACTED_CREDENTIAL]", secret_entry["fact_value"])

        summary = self.memory.get_project_context_summary("sess_03")
        self.assertIn("PROJECT MEMORY LEDGER", summary)
        self.assertIn("database", summary)

    def test_stats_and_export(self):
        self.memory.create_or_get_session("sess_exp")
        self.memory.set_fact("sess_exp", "ARCHITECTURE", "runtime", "Python 3.13")
        exported = self.memory.export_session("sess_exp")
        self.assertEqual(exported["session"]["session_id"], "sess_exp")
        self.assertEqual(len(exported["facts"]), 1)

        stats = self.memory.get_memory_stats()
        self.assertGreaterEqual(stats["fie_sessions"], 1)

    def test_session_clear(self):
        self.memory.create_or_get_session("sess_04")
        self.memory.set_fact("sess_04", "GENERAL", "k", "v")
        self.memory.record_task("t_clear", "sess_04", "type", "agent")
        self.memory.record_message("sess_04", "user", "hello")

        self.memory.clear_session("sess_04")
        self.assertIsNone(self.memory.get_session("sess_04"))
        self.assertEqual(len(self.memory.get_tasks_for_session("sess_04")), 0)
        self.assertEqual(len(self.memory.get_messages("sess_04")), 0)

if __name__ == "__main__":
    unittest.main()
