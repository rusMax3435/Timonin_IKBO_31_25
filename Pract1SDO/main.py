from command_executor import CommandExecutor
from command_parser import CommandParser
from prompt import Prompt
from repl import REPL


def main() -> None:
    repl = REPL(CommandParser(), CommandExecutor(), Prompt())
    repl.start()


if __name__ == "__main__":
    main()