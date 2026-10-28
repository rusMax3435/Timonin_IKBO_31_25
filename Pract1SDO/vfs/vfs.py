import base64
import json
from pathlib import Path

from vfs.vfs_node import VfsNode


class VFS:
    """In-memory virtual filesystem; source JSON is read once and not modified."""

    def __init__(self, name: str, source_path: Path) -> None:
        self.name = name
        self.source_path = source_path
        self.nodes: dict[str, VfsNode] = {}

    def load(self) -> None:
        with open(self.source_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict) or "nodes" not in data:
            raise ValueError("VFS JSON must contain a 'nodes' list")
        raw_nodes = data["nodes"]
        if not isinstance(raw_nodes, list):
            raise ValueError("'nodes' must be a list")

        loaded: dict[str, VfsNode] = {}
        for i, item in enumerate(raw_nodes, 1):
            if not isinstance(item, dict):
                raise ValueError(f"node {i}: not an object")
            path = self._normalize(item.get("path", ""))
            node_type = str(item.get("type", "")).lower()
            if node_type not in ("dir", "file"):
                raise ValueError(f"node {i}: unknown type '{node_type}'")

            b64 = item.get("content_base64", "") or ""
            if node_type == "file":
                try:
                    content = base64.b64decode(b64) if b64 else b""
                except Exception as e:
                    raise ValueError(f"node {i}: bad base64: {e}") from e
            else:
                content = b""

            if path in loaded:
                raise ValueError(f"node {i}: duplicate path '{path}'")
            loaded[path] = VfsNode(path, node_type, content)

        if "/" not in loaded:
            raise ValueError("VFS must contain root '/'")
        for node in loaded.values():
            if node.path == "/":
                continue
            parent = self._parent_of(node.path)
            if parent not in loaded:
                raise ValueError(f"missing parent '{parent}' for '{node.path}'")
            if loaded[parent].is_file():
                raise ValueError(f"parent '{parent}' is a file")

        self.nodes = loaded

    def save(self, dest: Path) -> None:
        payload = {"version": 1, "nodes": []}
        for node in self.nodes.values():
            payload["nodes"].append({
                "path": node.path,
                "type": node.type,
                "content_base64": (
                    base64.b64encode(node.content).decode("ascii")
                    if node.is_file() else ""
                ),
            })
        with open(dest, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def size(self) -> int:
        return len(self.nodes)

    @staticmethod
    def _normalize(path: str) -> str:
        if not path:
            return "/"
        s = path.strip()
        if not s.startswith("/"):
            s = "/" + s
        while len(s) > 1 and s.endswith("/"):
            s = s[:-1]
        return s

    @staticmethod
    def _parent_of(path: str) -> str:
        if path == "/":
            return ""
        i = path.rfind("/")
        return "/" if i <= 0 else path[:i]