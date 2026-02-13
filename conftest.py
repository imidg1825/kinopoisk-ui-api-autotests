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
    url = os.getenv("BASE_URL", "").strip()
    if not url:
        raise RuntimeError("BASE_URL is not set. Put it into .env")
    return url.rstrip("/")


@pytest.fixture(scope="session")
def api_token() -> str:
    token = os.getenv("API_TOKEN", "").strip()
    if not token:
        raise RuntimeError("API_TOKEN is not set. Put it into .env")
    return token


@pytest.fixture(scope="session")
def api_timeout() -> int:
    raw = os.getenv("API_TIMEOUT", "10").strip()
    return int(raw)


@pytest.fixture(scope="session")
def movie_id() -> int:
    raw = os.getenv("MOVIE_ID", "258687").strip()
    return int(raw)


@pytest.fixture(scope="session")
def api_session(api_token: str) -> Generator[requests.Session, None, None]:
    """
    Requests.Session configured like Postman:
    - accept: application/json
    - X-API-KEY: <token>
    """
    with allure.step("Create API session"):
        session = requests.Session()
        session.headers.update(
            {
                "accept": "application/json",
                "X-API-KEY": api_token,
            }
        )

    yield session

    with allure.step("Close API session"):
        session.close()
