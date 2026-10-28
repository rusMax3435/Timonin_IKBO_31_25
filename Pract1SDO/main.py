import argparse
import sys
from pathlib import Path

from command_executor import CommandExecutor
from command_parser import CommandParser
from config import Config
from prompt import Prompt
from repl import REPL
from vfs.vfs import VFS


def parse_args(argv: list[str]) -> Config:
    parser = argparse.ArgumentParser(prog="shell-emulator")
    parser.add_argument("--vfs", required=True, help="Path to VFS JSON file")
    parser.add_argument("--start-script", required=True, help="Path to start script")
    ns = parser.parse_args(argv)
    return Config(vfs_path=ns.vfs, start_script_path=ns.start_script)


def main(argv: list[str] | None = None) -> int:
    config = parse_args(sys.argv[1:] if argv is None else argv)
    print(f"[DEBUG] vfs_path={config.vfs_path}")
    print(f"[DEBUG] start_script_path={config.start_script_path}")

    vfs = VFS("unix", Path(config.vfs_path))
    try:
        vfs.load()
        print(f"[INFO] VFS loaded. Nodes: {vfs.size()}")
    except (OSError, ValueError) as e:
        print(f"[FATAL] Can't load VFS: {e}", file=sys.stderr)
        return 1

    repl = REPL(CommandParser(), CommandExecutor(vfs, config), Prompt(), config)
    return repl.start()


if __name__ == "__main__":
    sys.exit(main())