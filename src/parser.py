import tomllib


def extract_dependencies(toml_content: str) -> list[str]:
    """Извлекает прямые зависимости из содержимого Cargo.toml."""
    try:
        data = tomllib.loads(toml_content)
    except tomllib.TOMLDecodeError as error:
        raise ValueError("Ошибка парсинга Cargo.toml") from error

    dependencies: set[str] = set()
    dep_types = ["dependencies", "dev-dependencies", "build-dependencies"]
    
    for dep_type in dep_types:
        if dep_type in data:
            dependencies.update(data[dep_type].keys())
            
    return sorted(list(dependencies))