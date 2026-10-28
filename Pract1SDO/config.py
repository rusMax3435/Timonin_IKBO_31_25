from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    vfs_path: str
    start_script_path: str