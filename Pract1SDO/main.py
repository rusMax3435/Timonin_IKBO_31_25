import argparse
import sys

from command_executor import CommandExecutor
from command_parser import CommandParser
from config import Config
from prompt import Prompt
from repl import REPL


def parse_args(argv: list[str]) -> Config:
    parser = argparse.ArgumentParser(prog="shell-emulator")
    parser.add_argument("--vfs", required=True, help="Path to VFS source file")
    parser.add_argument("--start-script", required=True, help="Path to start script")
    ns = parser.parse_args(argv)
    return Config(vfs_path=ns.vfs, start_script_path=ns.start_script)


def main(argv: list[str] | None = None) -> int:
    config = parse_args(sys.argv[1:] if argv is None else argv)
    print(f"[DEBUG] vfs_path={config.vfs_path}")
    print(f"[DEBUG] start_script_path={config.start_script_path}")

    repl = REPL(CommandParser(), CommandExecutor(config), Prompt(), config)
    return repl.start()


if __name__ == "__main__":
    sys.exit(main())