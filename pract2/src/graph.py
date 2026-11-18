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
    # Так как API менеджеров запрещены, угадываем URL по шаблону
    guessed_url = f"https://github.com/{pkg_name}/{pkg_name}"
    try:
        content = fetcher.fetch_cargo_toml(guessed_url, "latest", False)
        return parser.extract_dependencies(content)
    except Exception:
        # Если репозиторий не найден или нет сети, пакет - лист
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


def print_graph(graph: dict[str, list[str]]) -> None:
    """Выводит граф зависимостей в формате ключ-значение."""
    print("\n=== Граф зависимостей (BFS) ===")
    for pkg, deps in graph.items():
        deps_str = ", ".join(deps) if deps else "нет"
        print(f"{pkg} -> {deps_str}")