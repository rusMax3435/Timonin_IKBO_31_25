import getpass
import os
import socket


class Prompt:
    """user@host:cwd$ — built from real OS data."""

    def __init__(self) -> None:
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.home = os.path.expanduser("~")

    def render(self) -> str:
        cwd = os.getcwd()
        if cwd == self.home:
            display = "~"
        elif cwd.startswith(self.home + os.sep):
            display = "~" + cwd[len(self.home):]
        else:
            display = cwd
        return f"{self.username}@{self.hostname}:{display}$ "