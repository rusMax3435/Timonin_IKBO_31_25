import unittest
from src.visualizer import generate_dot


class TestVisualizer(unittest.TestCase):
    def test_generate_dot(self):
        graph = {
            "A": ["B", "C"],
            "B": ["D"]
        }
        dot = generate_dot(graph)
        
        self.assertIn("digraph Dependencies {", dot)
        self.assertIn('"A" -> "B";', dot)
        self.assertIn('"A" -> "C";', dot)
        self.assertIn('"B" -> "D";', dot)
        self.assertIn('"D";', dot)  


if __name__ == "__main__":
    unittest.main()