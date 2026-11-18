import collections
import os
import fetcher
import parser


def load_test_graph(filepath: str) -> dict[str, list[str]]:
    """Загружает тестовый граф из файла формата 'A: B, C'."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")

    graph = {}
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or ":" not in line:
                continue
            pkg, deps_str = line.split(":", 1)
            pkg = pkg.strip()
            deps = [
                d.strip() for d in deps_str.split(",") if d.strip()
            ]
            graph[pkg] = deps
    return graph


def get_real_dependencies(pkg_name: str) -> list[str]:
    """Пытается получить зависимости из GitHub по имени пакета."""
    guessed_url = f"https://github.com/{pkg_name}/{pkg_name}"
    try:
        content = fetcher.fetch_cargo_toml(guessed_url, "latest", False)
        return parser.extract_dependencies(content)
    except Exception:
        return []


def build_graph_bfs(root_pkg: str, source: str, test_mode: bool):
    """Строит граф зависимостей с помощью BFS без рекурсии."""
    visited = set()
    queue = collections.deque([root_pkg])
    graph = {}

    test_graph = {}
    if test_mode:
        test_graph = load_test_graph(source)

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        if test_mode:
            deps = test_graph.get(current, [])
        else:
            if current == root_pkg:
                content = fetcher.fetch_cargo_toml(
                    source, "latest", False
                )
                deps = parser.extract_dependencies(content)
            else:
                deps = get_real_dependencies(current)

        graph[current] = deps
        
        for dep in deps:
            if dep not in visited:
                queue.append(dep)

    return graph


def build_reverse_graph_bfs(target_pkg: str, forward_graph: dict):
    """Строит граф обратных зависимостей с помощью BFS."""
    reverse_adj = {}
    for pkg, deps in forward_graph.items():
        for dep in deps:
            if dep not in reverse_adj:
                reverse_adj[dep] = []
            reverse_adj[dep].append(pkg)

    visited = set()
    queue = collections.deque([target_pkg])
    result_graph = {}

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)

        parents = reverse_adj.get(current, [])
        result_graph[current] = parents

        for parent in parents:
            if parent not in visited:
                queue.append(parent)

    return result_graph


def print_graph(graph: dict[str, list[str]]) -> None:
    """Выводит граф прямых зависимостей."""
    print("\n=== Прямые зависимости (BFS) ===")
    for pkg, deps in graph.items():
        deps_str = ", ".join(deps) if deps else "нет"
        print(f"{pkg} -> {deps_str}")


def print_reverse_graph(graph: dict[str, list[str]]) -> None:
    """Выводит граф обратных зависимостей."""
    print("\n=== Обратные зависимости (BFS) ===")
    for pkg, parents in graph.items():
        parents_str = ", ".join(parents) if parents else "нет"
        print(f"{pkg} <- {parents_str}")