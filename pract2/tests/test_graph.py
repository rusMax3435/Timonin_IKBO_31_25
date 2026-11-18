import unittest
import os
import tempfile
from src.graph import (
    build_graph_bfs, 
    load_test_graph, 
    build_reverse_graph_bfs
)


class TestGraphBFS(unittest.TestCase):
    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix=".txt"
        )
        self.test_file.write("A: B, C\n")
        self.test_file.write("B: D\n")
        self.test_file.write("C: D\n")
        self.test_file.write("D: A\n")  # Цикл
        self.test_file.close()

    def tearDown(self):
        os.remove(self.test_file.name)

    def test_load_test_graph(self):
        graph = load_test_graph(self.test_file.name)
        self.assertEqual(graph["A"], ["B", "C"])

    def test_bfs_with_cycle(self):
        result = build_graph_bfs("A", self.test_file.name, test_mode=True)
        self.assertEqual(result["A"], ["B", "C"])
        self.assertEqual(result["D"], ["A"])

    def test_reverse_bfs(self):
        # Строим прямой граф от A
        forward = build_graph_bfs("A", self.test_file.name, test_mode=True)
        
        # Ищем, кто зависит от D (должны быть B и C)
        reverse = build_reverse_graph_bfs("D", forward)
        
        # Проверяем связи: D <- B, C
        self.assertIn("D", reverse)
        self.assertEqual(sorted(reverse["D"]), ["B", "C"])
        
        # Проверяем транзитивность: кто зависит от B? (A)
        self.assertIn("B", reverse)
        self.assertEqual(reverse["B"], ["A"])


if __name__ == "__main__":
    unittest.main()