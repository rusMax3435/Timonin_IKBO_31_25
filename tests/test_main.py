import unittest
from unittest.mock import patch
from src.main import (
    validate_version,
    validate_url_or_path,
    validate_output_filename,
    create_parser,
    validate_args,
)


class TestValidationFunctions(unittest.TestCase):
    def test_validate_version(self):
        self.assertTrue(validate_version("1.0.0"))
        self.assertTrue(validate_version("latest"))
        self.assertFalse(validate_version("1.0"))
        self.assertFalse(validate_version("v1.0.0"))

    def test_validate_output_filename(self):
        self.assertTrue(validate_output_filename("graph.png"))
        self.assertTrue(validate_output_filename("graph.SVG"))
        self.assertFalse(validate_output_filename("graph.txt"))

    @patch("os.path.exists")
    def test_validate_url_or_path_test_mode(self, mock_exists):
        mock_exists.return_value = True
        self.assertTrue(validate_url_or_path("test.txt", True))
        
        mock_exists.return_value = False
        self.assertFalse(validate_url_or_path("test.txt", True))

    def test_validate_url_or_path_normal(self):
        self.assertTrue(validate_url_or_path("https://github.com", False))
        self.assertFalse(validate_url_or_path("not_a_url", False))


class TestArgumentParsing(unittest.TestCase):
    def test_validate_args_success(self):
        parser = create_parser()
        args = parser.parse_args([
            "-p", "test-pkg", 
            "-r", "https://example.com",
            "-o", "graph.png", 
            "-v", "1.0.0"
        ])
        self.assertEqual(validate_args(args), [])

    def test_validate_args_errors(self):
        parser = create_parser()
        args = parser.parse_args([
            "-p", "test-pkg", 
            "-r", "invalid-url", 
            "-o", "graph.txt", 
            "-v", "1.0"
        ])
        errors = validate_args(args)
        self.assertEqual(len(errors), 3)


if __name__ == "__main__":
    unittest.main()