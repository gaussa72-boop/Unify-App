import unittest
from ultima_ai.agent_network import _selected_agents


class AgentSelectionTests(unittest.TestCase):
    def setUp(self):
        self.registry = [
            {"id": "aurealis", "name": "Aurealis"},
            {"id": "ionos7", "name": "IONOS-7"},
            {"id": "neuroforge", "name": "Neuroforge"},
            {"id": "guardian", "name": "CyberShield"},
            {"id": "ionos_ki", "name": "IONOS-KI"},
            {"id": "ultra_ki_pro", "name": "Quantum KI Ultra Pro"},
        ]

    def test_only_registered_agents_are_selected(self):
        selected = _selected_agents(self.registry, ["ionos7", "unknown"])
        self.assertEqual([x["id"] for x in selected], ["ionos7"])

    def test_duplicates_are_removed_and_limit_is_four(self):
        selected = _selected_agents(self.registry, ["aurealis", "aurealis", "ionos7", "neuroforge", "guardian"])
        self.assertEqual(len(selected), 4)
        self.assertEqual(len({x["id"] for x in selected}), 4)

    def test_defaults_are_used_for_missing_selection(self):
        selected = _selected_agents(self.registry, None)
        self.assertEqual([x["id"] for x in selected], ["aurealis", "ionos7", "ionos_ki", "ultra_ki_pro"])


if __name__ == "__main__":
    unittest.main()
