from enum import Enum


class REPLStatus(Enum):
    READY = "ready"
    RUNNING = "running"
    NOT_WORKING = "not_working"


class CommandExecutionStatus(Enum):
    OK = "Successfully executed"
    COMMAND_NOT_FOUND = "Got an unknown command."
    WRONG_ARGUMENT = "Wrong arguments provided."
    TERMINATE_EMULATOR = "Got a call to terminate emulator. Exiting."

    @property
    def message(self) -> str:
        return self.value


class Command(Enum):
    EXIT = ("exit", "Terminates the emulator.")
    LS = ("ls", "Stub for ls.")
    CD = ("cd", "Stub for cd.")
    CONF_DUMP = ("conf-dump", "Prints emulator configuration.")

    def __init__(self, command_name: str, help_message: str) -> None:
        self.command_name = command_name
        self.help_message = help_message