"""
Модуль для работы с репозиторием PyPI.
Вариант 11, Этап 2.
"""
import os
import re
import json
import urllib.request
import urllib.error


PYPI_BASE_URL = "https://pypi.org/pypi"
UNKNOWN_VERSION = "?"


def parse_package_name(name):
    """
    Разбирает имя пакета на имя и версию.
    :param name: Строка вида 'package' или 'package==1.0'.
    :return: Кортеж (package_name, version).
    """
    if "==" in name:
        parts = name.split("==", 1)
        return parts[0].strip(), parts[1].strip()
    return name.strip(), None


def build_pypi_url(package, version=None):
    """
    Строит URL к JSON API PyPI.
    :param package: Имя пакета.
    :param version: Версия или None.
    :return: Полный URL.
    """
    base = PYPI_BASE_URL.rstrip("/")
    if version:
        return f"{base}/{package}/{version}/json"
    return f"{base}/{package}/json"


def fetch_json(url):
    """
    Скачивает JSON по URL.
    :param url: Адрес для загрузки.
    :return: Словарь с данными.
    """
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
    except urllib.error.HTTPError as e:
        raise ValueError(
            f"Ошибка HTTP {e.code} при запросе {url}"
        ) from e
    except urllib.error.URLError as e:
        raise ValueError(
            f"Ошибка сети при запросе {url}: {e.reason}"
        ) from e


def _parse_requirement(req_str):
    """
    Парсит одну строку зависимости.
    :param req_str: Строка вида 'package (>=1.0)'.
    :return: Словарь {name, version_spec} или None.
    """
    if not req_str:
        return None
    req_str = req_str.strip()
    if "extra ==" in req_str:
        return None
    match = re.match(
        r"^([a-zA-Z0-9_.-]+)\s*(\(.*?\))?",
        req_str
    )
    if not match:
        return None
    name = match.group(1)
    version_spec = match.group(2) or ""
    return {
        "name": name,
        "version_spec": version_spec.strip(),
    }


def parse_requires_dist(requires_dist):
    """
    Парсит список зависимостей из PyPI.
    :param requires_dist: Список строк.
    :return: Список словарей с зависимостями.
    """
    if not requires_dist:
        return []
    deps = []
    for req in requires_dist:
        parsed = _parse_requirement(req)
        if parsed is not None:
            deps.append(parsed)
    return deps


def get_dependencies(source, package, test_mode=False):
    """
    Получает прямые зависимости пакета Python.
    :param source: URL PyPI или путь к JSON-файлу.
    :param package: Имя пакета (возможно с версией).
    :param test_mode: Флаг тестового режима.
    :return: Кортеж (список зависимостей, версия).
    """
    if test_mode:
        return _get_deps_from_file(source, package)
    return _get_deps_from_pypi(source, package)


def _get_deps_from_file(file_path, package):
    """
    Читает зависимости из локального JSON-файла.
    :param file_path: Путь к JSON-файлу.
    :param package: Имя пакета.
    :return: Кортеж (зависимости, версия).
    """
    if not os.path.isfile(file_path):
        raise ValueError(
            f"Файл не найден: {file_path}"
        )
    with open(
        file_path, "r", encoding="utf-8"
    ) as f:
        data = json.load(f)
    info = data.get("info", {})
    version = info.get("version", UNKNOWN_VERSION)
    requires_dist = info.get("requires_dist", [])
    deps = parse_requires_dist(requires_dist)
    return deps, version


def _get_deps_from_pypi(source, package):
    """
    Скачивает зависимости из PyPI.
    :param source: URL PyPI.
    :param package: Имя пакета.
    :return: Кортеж (зависимости, версия).
    """
    pkg_name, version = parse_package_name(package)
    url = build_pypi_url(pkg_name, version)
    data = fetch_json(url)
    info = data.get("info", {})
    actual_version = info.get("version", UNKNOWN_VERSION)
    requires_dist = info.get("requires_dist", [])
    deps = parse_requires_dist(requires_dist)
    return deps, actual_version
