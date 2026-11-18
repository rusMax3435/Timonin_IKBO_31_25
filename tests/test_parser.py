import unittest
from src.parser import extract_dependencies


class TestParser(unittest.TestCase):
    def test_extract_dependencies(self):
        toml = """
        [package]
        name = "test"
        version = "1.0.0"

        [dependencies]
        serde = "1.0"
        tokio = { version = "1.0", features = ["full"] }

        [dev-dependencies]
        criterion = "0.3"
        """
        result = extract_dependencies(toml)
        expected = ["criterion", "serde", "tokio"]
        self.assertEqual(result, expected)

    def test_empty_dependencies(self):
        toml = "[package]\nname = \"test\"\n"
        result = extract_dependencies(toml)
        self.assertEqual(result, [])