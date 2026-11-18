import subprocess


def generate_dot(graph: dict[str, list[str]]) -> str:
    """Генерирует текстовое представление графа на языке Graphviz."""
    lines = ["digraph Dependencies {"]
    lines.append("    rankdir=LR;")
    lines.append("    node [shape=box, style=filled, color=lightblue];")
    
    for pkg, deps in graph.items():
        # Добавляем узел, даже если у него нет зависимостей
        lines.append(f'    "{pkg}";')
        for dep in deps:
            lines.append(f'    "{pkg}" -> "{dep}";')
            
    lines.append("}")
    return "\n".join(lines)


def save_png(dot_code: str, output_path: str) -> None:
    """Сохраняет граф в PNG, вызывая системную утилиту Graphviz."""
    try:
        process = subprocess.run(
            ["dot", "-Tpng", "-o", output_path],
            input=dot_code.encode('utf-8'),
            capture_output=True,
            check=True
        )
    except FileNotFoundError as error:
        raise RuntimeError(
            "Утилита 'dot' не найдена. Установите Graphviz в систему."
        ) from error
    except subprocess.CalledProcessError as error:
        stderr = error.stderr.decode('utf-8')
        raise RuntimeError(f"Ошибка Graphviz:\n{stderr}") from error