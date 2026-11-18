import os
import ssl
import urllib.error
import urllib.request

MIN_LEN = 2

def build_raw_urls(repo_url: str, version: str) -> list[str]:
    """Строит список возможных URL к raw-файлу Cargo.toml."""
    clean_url = repo_url.rstrip('/')
    if clean_url.endswith('.git'):
        clean_url = clean_url[:-4]

    parts = clean_url.split('/')
    if len(parts) < MIN_LEN:
        raise ValueError("Некорректный URL репозитория GitHub")

    owner, repo = parts[-2], parts[-1]
    base_raw = "https://raw.githubusercontent.com"
    
    urls = []
    if version == "latest":
        urls.append(f"{base_raw}/{owner}/{repo}/refs/heads/main/Cargo.toml")
        urls.append(f"{base_raw}/{owner}/{repo}/refs/heads/master/Cargo.toml")
    else:
        urls.append(
            f"{base_raw}/{owner}/{repo}/refs/tags/{version}/Cargo.toml"
        )
        urls.append(
            f"{base_raw}/{owner}/{repo}/refs/tags/v{version}/Cargo.toml"
        )
    return urls


def fetch_cargo_toml(repo_url: str, version: str, test_mode: bool) -> str:
    """Загружает содержимое Cargo.toml из локального файла или сети."""
    if test_mode:
        if not os.path.exists(repo_url):
            raise FileNotFoundError(f"Файл не найден: {repo_url}")
        with open(repo_url, 'r', encoding='utf-8') as file:
            return file.read()

    urls = build_raw_urls(repo_url, version)
    
    context = ssl._create_unverified_context()
    
    for url in urls:
        try:
            req = urllib.request.Request(
                url, headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(
                req, timeout=10, context=context
            ) as response:
                return response.read().decode('utf-8')
        except urllib.error.HTTPError:
            continue
        except urllib.error.URLError as error:
            raise ConnectionError(
                f"Ошибка сети ({error.reason}) при загрузке {url}"
            ) from error
            
    raise ConnectionError("Не удалось скачать Cargo.toml. Проверьте URL.")