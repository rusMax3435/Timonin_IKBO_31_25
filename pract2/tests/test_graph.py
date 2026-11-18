import unittest
import os
import tempfile
from src.graph import build_graph_bfs, load_test_graph


class TestGraphBFS(unittest.TestCase):
    def setUp(self):
        # Создаем временный файл с тестовым графом (включая цикл)
        self.test_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix=".txt"
        )
        self.test_file.write("A: B, C\n")
        self.test_file.write("B: D\n")
        self.test_file.write("C: D\n")
        self.test_file.write("D: A\n")  # Цикл A -> D -> A
        self.test_file.close()

    def tearDown(self):
        os.remove(self.test_file.name)

    def test_load_test_graph(self):
        graph = load_test_graph(self.test_file.name)
        self.assertEqual(graph["A"], ["B", "C"])
        self.assertEqual(graph["D"], ["A"])

    def test_bfs_with_cycle(self):
        # Запускаем BFS с корня A
        result = build_graph_bfs("A", self.test_file.name, test_mode=True)
        
        # Проверяем, что все узлы посещены, и программа не зависла
        self.assertIn("A", result)
        self.assertIn("B", result)
        self.assertIn("C", result)
        self.assertIn("D", result)
        
        self.assertEqual(result["A"], ["B", "C"])
        self.assertEqual(result["D"], ["A"])


if __name__ == "__main__":
    unittest.main()