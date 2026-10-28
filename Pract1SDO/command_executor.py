from enums import Command, CommandExecutionStatus


class CommandExecutor:
    def execute(self, tokens: list[str]) -> CommandExecutionStatus:
        if not tokens:
            return CommandExecutionStatus.COMMAND_NOT_FOUND

        command = next((c for c in Command if c.command_name == tokens[0]), None)
        if command is None:
            return CommandExecutionStatus.COMMAND_NOT_FOUND

        if command is Command.EXIT:
            if len(tokens) != 1:
                return CommandExecutionStatus.WRONG_ARGUMENT
            return CommandExecutionStatus.TERMINATE_EMULATOR

        # Stubs — print the command name and its arguments
        if command is Command.LS:
            if len(tokens) > 2:
                return CommandExecutionStatus.WRONG_ARGUMENT
            print(f"ls called, args={tokens[1:]}")
            return CommandExecutionStatus.OK

        if command is Command.CD:
            if len(tokens) != 2:
                return CommandExecutionStatus.WRONG_ARGUMENT
            print(f"cd called, args={tokens[1:]}")
            return CommandExecutionStatus.OK

        return CommandExecutionStatus.COMMAND_NOT_FOUND