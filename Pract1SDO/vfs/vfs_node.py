from dataclasses import dataclass


@dataclass
class VfsNode:
    path: str
    type: str          # "dir" | "file"
    content: bytes = b""

    def is_directory(self) -> bool:
        return self.type == "dir"

    def is_file(self) -> bool:
        return self.type == "file"