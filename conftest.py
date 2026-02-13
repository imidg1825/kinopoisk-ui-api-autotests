from __future__ import annotations

import os
from typing import Generator

import allure
import pytest
import requests
from dotenv import load_dotenv

# Загружаем переменные из .env (файл лежит в корне проекта)
load_dotenv()


@pytest.fixture(scope="session")
def base_url() -> str:
    """Базовый URL API (берем из .env)."""
    value = os.getenv("BASE_URL", "").strip().rstrip("/")
    if not value:
        raise RuntimeError("BASE_URL is not set in .env")
    return value


@pytest.fixture(scope="session")
def api_timeout() -> int:
    """Таймаут для API запросов (секунды)."""
    raw = os.getenv("API_TIMEOUT", "10").strip()
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError(f"API_TIMEOUT must be int, got: {raw!r}") from exc


@pytest.fixture(scope="session")
def api_token() -> str:
    """Токен для API (из .env)."""
    token = os.getenv("API_TOKEN", "").strip()
    if not token:
        raise RuntimeError("API_TOKEN is not set in .env")
    return token


@pytest.fixture(scope="session")
def api_session(api_token: str) -> Generator[requests.Session, None, None]:
    """HTTP-сессия для API тестов (общие headers как в Postman)."""
    with allure.step("Создаем requests.Session для API"):
        session = requests.Session()
        session.headers.update(
            {
                "accept": "application/json",
                "X-API-KEY": api_token,  # важно: как в Postman
            }
        )

    yield session

    with allure.step("Закрываем requests.Session"):
        session.close()
