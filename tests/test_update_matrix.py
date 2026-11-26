import os
import tempfile
import unittest
from pathlib import Path
from flask import Flask
import update_matrix

class UpdateMatrixTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        update_matrix.DB_PATH = Path(self.tmp.name) / "matrix.sqlite3"
        os.environ["ULTIMA_UPDATE_MATRIX_TOKEN"] = "test-token"
        os.environ.pop("UPDATE_MATRIX_LLM_API_URL", None)
        os.environ.pop("UPDATE_MATRIX_LLM_API_KEY", None)
        self.app = Flask(__name__)
        self.app.register_blueprint(update_matrix.bp)
        self.client = self.app.test_client()
        self.headers = {"Authorization": "Bearer test-token"}

    def tearDown(self):
        self.tmp.cleanup()
        os.environ.pop("ULTIMA_UPDATE_MATRIX_TOKEN", None)

    def test_auth_required(self):
        response = self.client.get("/api/update-matrix/status")
        self.assertEqual(response.status_code, 401)

    def test_status_and_scoped_agents(self):
        response = self.client.get("/api/update-matrix/status", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["mode"], "proposal_first")
        agents = self.client.get("/api/update-matrix/agents", headers=self.headers)
        self.assertEqual(agents.status_code, 200)
        self.assertEqual(len(agents.json["agents"]), 4)

    def test_generation_fails_closed_without_provider(self):
        response = self.client.post("/api/update-matrix/proposals/generate",
            headers=self.headers, json={"agent_id":"omnia_mining","task":"Review archive"})
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json["error"], "llm_provider_not_configured")

    def test_unknown_agent_rejected(self):
        response = self.client.post("/api/update-matrix/proposals/generate",
            headers=self.headers, json={"agent_id":"root","task":"Do anything"})
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
