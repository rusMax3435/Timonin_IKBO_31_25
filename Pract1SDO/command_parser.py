import os


class CommandParser:
    """Splits input into command + args; expands real env vars ($VAR, ${VAR})."""

    def parse_input(self, raw_input: str) -> list[str]:
        expanded = os.path.expandvars(raw_input)
        return expanded.strip().split()