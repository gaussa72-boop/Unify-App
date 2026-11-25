import os
import tempfile
import unittest

from ultima_ai import agent_store


class AgentStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        os.environ["ULTIMA_AGENT_DB"] = self.tmp.name

    def tearDown(self):
        os.unlink(self.tmp.name)
        os.environ.pop("ULTIMA_AGENT_DB", None)

    def test_task_history_round_trip(self):
        task = agent_store.create_task("Testauftrag", {"summary": "ok"})
        rows = agent_store.list_tasks()
        self.assertEqual(rows[0]["id"], task["id"])
        self.assertEqual(rows[0]["result"]["summary"], "ok")

    def test_approval_requires_pending_state(self):
        approval = agent_store.create_approval(None, "deploy", {"service": "demo"})
        self.assertTrue(agent_store.decide_approval(approval["id"], "approved", "reviewed"))
        self.assertFalse(agent_store.decide_approval(approval["id"], "rejected"))

    def test_agent_message_inbox_is_scoped(self):
        agent_store.add_message("neuroforge", "ultima", {"finding": "safe"})
        self.assertEqual(len(agent_store.list_messages("ultima")), 1)
        self.assertEqual(len(agent_store.list_messages("ionos7")), 0)


if __name__ == "__main__":
    unittest.main()
