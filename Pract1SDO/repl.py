import os
import sys

from command_executor import CommandExecutor
from command_parser import CommandParser
from config import Config
from enums import CommandExecutionStatus, REPLStatus
from prompt import Prompt


class REPL:
    def __init__(
        self,
        parser: CommandParser,
        executor: CommandExecutor,
        prompt: Prompt,
        config: Config,
    ) -> None:
        self.parser = parser
        self.executor = executor
        self.prompt = prompt
        self.config = config
        self.status = REPLStatus.READY

    def _run_line(self, line: str) -> CommandExecutionStatus:
        if not line.strip():
            return CommandExecutionStatus.OK
        tokens = self.parser.parse_input(line)
        status = self.executor.execute(tokens)
        if status not in (CommandExecutionStatus.OK, CommandExecutionStatus.TERMINATE_EMULATOR):
            print(status.message, file=sys.stderr)
        return status

    def _run_start_script(self) -> None:
        path = self.config.start_script_path
        if not os.path.isfile(path):
            print(f"[ERROR] Start script not found: {path}", file=sys.stderr)
            return

        print(f"[INFO] Executing start script: {path}")
        with open(path, "r", encoding="utf-8") as f:
            for line_no, raw in enumerate(f, 1):
                line = raw.rstrip("\n")
                print(f"{self.prompt.render()}{line}")
                status = self._run_line(line)

                if status == CommandExecutionStatus.TERMINATE_EMULATOR:
                    self.status = REPLStatus.NOT_WORKING
                    return

                if status != CommandExecutionStatus.OK:
                    print(
                        f"[SCRIPT] Stopped at line {line_no}: {status.message}",
                        file=sys.stderr,
                    )
                    return

        print("[INFO] Start script finished successfully.")

    def start(self) -> int:
        print("(i) REPL is ready.")
        self.status = REPLStatus.RUNNING

        if not os.path.isfile(self.config.vfs_path):
            print(f"[FATAL] VFS file not found: {self.config.vfs_path}", file=sys.stderr)
            print("(i) REPL isn't working.")
            return 1
        print(f"[INFO] VFS is ready: {self.config.vfs_path}")

        self._run_start_script()

        while self.status != REPLStatus.NOT_WORKING:
            try:
                raw = input(self.prompt.render())
            except (EOFError, KeyboardInterrupt):
                print()
                break

            status = self._run_line(raw)
            if status == CommandExecutionStatus.TERMINATE_EMULATOR:
                self.status = REPLStatus.NOT_WORKING

        print("(i) REPL isn't working.")
        return 0