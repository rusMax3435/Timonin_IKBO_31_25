import unittest
from src.fetcher import build_raw_url


class TestFetcher(unittest.TestCase):
    def test_build_raw_url_latest(self):
        url = build_raw_url("https://github.com/rust-lang/cargo", "latest")
        expected = (
            "https://raw.githubusercontent.com/rust-lang/cargo/main/Cargo.toml"
        )
        self.assertEqual(url, expected)

    def test_build_raw_url_version(self):
        url = build_raw_url("https://github.com/rust-lang/cargo.git", "0.1.0")
        expected = (
            "https://raw.githubusercontent.com/rust-lang/cargo/0.1.0/Cargo.toml"
        )
        self.assertEqual(url, expected)