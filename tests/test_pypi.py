"""
Тесты модуля pypi.
"""
import pytest
import os
import sys
import json
import tempfile

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '..', 'src'
        )
    )
)

from pypi import (
    parse_package_name,
    build_pypi_url,
    parse_requires_dist,
    get_dependencies,
)


SAMPLE_DATA = {
    "info": {
        "name": "requests",
        "version": "2.31.0",
        "requires_dist": [
            "charset-normalizer (<4,>=2)",
            "idna (<4,>=2.5)",
            "urllib3 (<3,>=1.21.1)",
            "certifi (>=2017.4.17)",
            "PySocks (!=1.5.7,>=1.5.6) ; "
            "extra == 'socks'",
        ],
    }
}

EMPTY_DATA = {
    "info": {
        "name": "empty-pkg",
        "version": "1.0.0",
        "requires_dist": [],
    }
}

EXPECTED_DEPS_COUNT = 4
EXPECTED_EMPTY_COUNT = 0


def test_parse_package_name_simple():
    """Проверка разбора имени без версии."""
    name, version = parse_package_name("requests")
    assert name == "requests"
    assert version is None


def test_parse_package_name_with_version():
    """Проверка разбора имени с версией."""
    name, version = parse_package_name(
        "requests==2.31.0"
    )
    assert name == "requests"
    assert version == "2.31.0"


def test_build_pypi_url_no_version():
    """Проверка URL без версии."""
    url = build_pypi_url("requests")
    expected = "https://pypi.org/pypi/requests/json"
    assert url == expected


def test_build_pypi_url_with_version():
    """Проверка URL с версией."""
    url = build_pypi_url("requests", "2.31.0")
    expected = (
        "https://pypi.org/pypi/requests/"
        "2.31.0/json"
    )
    assert url == expected


def test_parse_requires_dist():
    """Проверка парсинга зависимостей."""
    deps = parse_requires_dist(
        SAMPLE_DATA["info"]["requires_dist"]
    )
    assert len(deps) == EXPECTED_DEPS_COUNT
    assert deps[0]["name"] == "charset-normalizer"
    assert deps[0]["version_spec"] == "(<4,>=2)"
    assert deps[3]["name"] == "certifi"


def test_parse_requires_dist_empty():
    """Проверка пустого списка зависимостей."""
    deps = parse_requires_dist([])
    assert len(deps) == EXPECTED_EMPTY_COUNT


def test_parse_requires_dist_none():
    """Проверка None вместо списка."""
    deps = parse_requires_dist(None)
    assert len(deps) == EXPECTED_EMPTY_COUNT


def test_get_dependencies_from_file():
    """Проверка чтения из JSON-файла."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False,
        encoding="utf-8"
    ) as f:
        json.dump(SAMPLE_DATA, f)
        tmp_path = f.name
    try:
        deps, version = get_dependencies(
            tmp_path, "requests", test_mode=True
        )
        assert len(deps) == EXPECTED_DEPS_COUNT
        assert version == "2.31.0"
    finally:
        os.unlink(tmp_path)


def test_get_dependencies_file_not_found():
    """Проверка ошибки при отсутствии файла."""
    with pytest.raises(ValueError):
        get_dependencies(
            "/nonexistent.json",
            "requests",
            test_mode=True
        )


def test_get_dependencies_empty():
    """Проверка пакета без зависимостей."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False,
        encoding="utf-8"
    ) as f:
        json.dump(EMPTY_DATA, f)
        tmp_path = f.name
    try:
        deps, version = get_dependencies(
            tmp_path, "empty-pkg", test_mode=True
        )
        assert len(deps) == EXPECTED_EMPTY_COUNT
        assert version == "1.0.0"
    finally:
        os.unlink(tmp_path)
