import io
import json
import os
import unittest
from unittest.mock import patch

from ultima_ai.agent_network import _agent_call


class RemoteAgentTests(unittest.TestCase):
    @patch("ultima_ai.agent_network.urlopen")
    def test_remote_agent_uses_shared_token_and_returns_analysis(self, mocked):
        mocked.return_value.__enter__.return_value = io.BytesIO(
            json.dumps({"answer": "Bitcoin-Netzwerkanalyse"}).encode("utf-8")
        )
        with patch.dict(os.environ, {"ULTIMA_AGENT_SHARED_TOKEN": "test-token"}):
            answer = _agent_call({"id": "aurealis", "name": "AUREALIS OMNIA"},
                                 "Analysiere den Block", "unused", "unused", "unused")
        self.assertEqual(answer, "Bitcoin-Netzwerkanalyse")
        request = mocked.call_args.args[0]
        self.assertEqual(request.full_url, "https://aurealis-omnia.onrender.com/api/agent/analyze")
        self.assertEqual(request.get_header("X-ultima-agent-token"), "test-token")

    def test_remote_agent_requires_shared_token(self):
        with patch.dict(os.environ, {"ULTIMA_AGENT_SHARED_TOKEN": ""}):
            with self.assertRaises(ValueError):
                _agent_call({"id": "ionos7", "name": "IONOS-7"},
                            "Analysiere", "unused", "unused", "unused")


if __name__ == "__main__":
    unittest.main()
