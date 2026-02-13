from __future__ import annotations

import os
from typing import Generator

import allure
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def base_url() -> str:
    """Базовый URL для API (берем из .env)."""
    value = os.getenv("BASE_URL", "https://httpbin.org").rstrip("/")
    return value


@pytest.fixture(scope="session")
def api_timeout() -> int:
    """Таймаут для API запросов (секунды)."""
    raw = os.getenv("API_TIMEOUT", "10")
    return int(raw)


@pytest.fixture(scope="session")
def api_session() -> Generator[requests.Session, None, None]:
    """HTTP-сессия для API тестов (переиспользует соединения)."""
    with allure.step("Создаем requests.Session для API тестов"):
        session = requests.Session()
    yield session
    with allure.step("Закрываем requests.Session"):
        session.close()
