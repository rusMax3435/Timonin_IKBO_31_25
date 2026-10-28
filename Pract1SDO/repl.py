import sys

from command_executor import CommandExecutor
from command_parser import CommandParser
from enums import CommandExecutionStatus, REPLStatus
from prompt import Prompt


class REPL:
    def __init__(
        self,
        parser: CommandParser,
        executor: CommandExecutor,
        prompt: Prompt,
    ) -> None:
        self.parser = parser
        self.executor = executor
        self.prompt = prompt
        self.status = REPLStatus.READY

    def start(self) -> None:
        print("(i) REPL is ready.")
        self.status = REPLStatus.RUNNING

        while self.status != REPLStatus.NOT_WORKING:
            try:
                raw = input(self.prompt.render())
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not raw.strip():
                continue

            tokens = self.parser.parse_input(raw)
            status = self.executor.execute(tokens)

            if status == CommandExecutionStatus.TERMINATE_EMULATOR:
                self.status = REPLStatus.NOT_WORKING
            elif status != CommandExecutionStatus.OK:
                print(status.message, file=sys.stderr)

        print("(i) REPL isn't working.")