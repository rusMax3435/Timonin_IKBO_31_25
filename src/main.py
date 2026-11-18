import argparse
import os
import re
import sys
from urllib.parse import urlparse
import graph
import visualizer


def validate_version(version_str: str) -> bool:
    """Проверяет версию пакета на соответствие SemVer."""
    if version_str == "latest":
        return True
    pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(pattern, version_str))


def validate_url_or_path(repo_str: str, is_test_mode: bool) -> bool:
    """Проверяет URL репозитория или путь к файлу."""
    if is_test_mode:
        return os.path.exists(repo_str)
    parsed_url = urlparse(repo_str)
    return bool(parsed_url.scheme and parsed_url.netloc)


def validate_output_filename(filename: str) -> bool:
    """Проверяет расширение файла."""
    allowed_extensions = ('.png', '.svg', '.jpg', '.jpeg')
    return filename.lower().endswith(allowed_extensions)


def create_parser() -> argparse.ArgumentParser:
    """Создает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей"
    )
    parser.add_argument(
        "-p", "--package", required=True, help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "-r", "--repo", required=True, help="URL репозитория или путь к файлу"
    )
    parser.add_argument(
        "-t", "--test-mode", action="store_true", help="Режим тестирования"
    )
    parser.add_argument(
        "-v", "--version", default="latest", help="Версия пакета"
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Имя файла изображения графа"
    )
    parser.add_argument(
        "-rev", "--reverse", action="store_true", 
        help="Вывод обратных зависимостей"
    )
    return parser


def validate_args(args: argparse.Namespace) -> list:
    """Валидирует аргументы."""
    errors = []
    if not validate_version(args.version):
        errors.append(f"Неверный формат версии: '{args.version}'")
    if not validate_url_or_path(args.repo, args.test_mode):
        if args.test_mode:
            errors.append(f"Файл тестового репозитория не найден: {args.repo}")
        else:
            errors.append(f"Неверный URL репозитория: {args.repo}")
    if not validate_output_filename(args.output):
        errors.append(f"Неверное имя файла графа: '{args.output}'")
    return errors


def main() -> None:
    """Точка входа в приложение."""
    arg_parser = create_parser()
    args = arg_parser.parse_args()
    
    errors = validate_args(args)
    if errors:
        print("Обнаружены ошибки при вводе параметров:", file=sys.stderr)
        for err in errors:
            print(f" - {err}", file=sys.stderr)
        sys.exit(1)

    try:
        dep_graph = graph.build_graph_bfs(
            args.package, args.repo, args.test_mode
        )
        
        if args.reverse:
            rev_graph = graph.build_reverse_graph_bfs(
                args.package, dep_graph
            )
            graph.print_reverse_graph(rev_graph)
            final_graph = rev_graph
        else:
            graph.print_graph(dep_graph)
            final_graph = dep_graph

        dot_code = visualizer.generate_dot(final_graph)
        
        print("\n=== Код Graphviz (DOT) ===")
        print(dot_code)
        
        print(f"\nСохранение PNG в {args.output}...")
        visualizer.save_png(dot_code, args.output)
        print("Успешно сохранено!")
            
    except Exception as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()