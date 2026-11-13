import argparse
import os
import re
import sys
from urllib.parse import urlparse


def validate_version(version_str: str) -> bool:
    """Проверяет версию пакета на соответствие SemVer (например, 1.0.0)."""
    if version_str == "latest":
        return True
    pattern = r'^\d+\.\d+\.\d+$'
    return bool(re.match(pattern, version_str))


def validate_url_or_path(repo_str: str, is_test_mode: bool) -> bool:
    """Проверяет URL репозитория или путь к файлу (в режиме теста)."""
    if is_test_mode:
        return os.path.exists(repo_str)
    parsed_url = urlparse(repo_str)
    return bool(parsed_url.scheme and parsed_url.netloc)


def validate_output_filename(filename: str) -> bool:
    """Проверяет расширение файла для сохранения графа."""
    allowed_extensions = ('.png', '.svg', '.jpg', '.jpeg')
    return filename.lower().endswith(allowed_extensions)


def create_parser() -> argparse.ArgumentParser:
    """Создает и настраивает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей (Этап 1)"
    )
    parser.add_argument(
        "-p", "--package", required=True,
        help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "-r", "--repo", required=True,
        help="URL-адрес репозитория или путь к файлу тестового репозитория"
    )
    parser.add_argument(
        "-t", "--test-mode", action="store_true",
        help="Режим работы с тестовым репозиторием (файлом)"
    )
    parser.add_argument(
        "-v", "--version", default="latest",
        help="Версия пакета (например, 1.0.0). По умолчанию: latest"
    )
    parser.add_argument(
        "-o", "--output", required=True,
        help="Имя сгенерированного файла с изображением графа"
    )
    return parser


def validate_args(args: argparse.Namespace) -> list:
    """Валидирует переданные аргументы и возвращает список ошибок."""
    errors = []
    
    if not validate_version(args.version):
        errors.append(f"Неверный формат версии: '{args.version}'")
        
    if not validate_url_or_path(args.repo, args.test_mode):
        if args.test_mode:
            errors.append(f"Файл тестового репозитория не найден: {args.repo}")
        else:
            errors.append(f"Неверный URL репозитория: {args.repo}")
            
    if not validate_output_filename(args.output):
        errors.append(
            f"Неверное имя файла графа: '{args.output}'. "
            f"Допустимые расширения: .png, .svg, .jpg, .jpeg"
        )
        
    return errors


def print_config(args: argparse.Namespace) -> None:
    """Выводит настраиваемые параметры в формате ключ-значение."""
    print("=== Параметры конфигурации ===")
    print(f"package_name: {args.package}")
    print(f"repository_url_or_path: {args.repo}")
    print(f"test_mode: {args.test_mode}")
    print(f"package_version: {args.version}")
    print(f"output_filename: {args.output}")


def main() -> None:
    """Точка входа в приложение."""
    parser = create_parser()
    args = parser.parse_args()
    
    errors = validate_args(args)
    if errors:
        print("Обнаружены ошибки при вводе параметров:", file=sys.stderr)
        for err in errors:
            print(f" - {err}", file=sys.stderr)
        sys.exit(1)

    print_config(args)


if __name__ == "__main__":
    main()