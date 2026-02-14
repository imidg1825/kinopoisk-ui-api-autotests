from typing import Generator

import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# ======================
# API CONFIG
# ======================

import os

API_TOKEN = os.getenv("API_TOKEN")
BASE_URL = "https://api.kinopoisk.dev/v1.4"
UI_BASE_URL = "https://www.kinopoisk.ru"


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def ui_base_url() -> str:
    return UI_BASE_URL


@pytest.fixture(scope="session")
def api_timeout() -> int:
    return 20


@pytest.fixture(scope="session")
def api_session() -> Generator[requests.Session, None, None]:
    session = requests.Session()
    session.headers.update(
        {
            "X-API-KEY": API_TOKEN,
            "accept": "application/json",
            "User-Agent": "Mozilla/5.0",
        }
    )

    retry = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)

    yield session
    session.close()


# ======================
# UI CONFIG
# ======================


def _build_chrome_options() -> Options:
    options = Options()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--lang=ru-RU")

    # важный момент — не ждём полной загрузки тяжёлых страниц
    options.page_load_strategy = "eager"

    return options


@pytest.fixture(scope="session")
def driver() -> Generator[webdriver.Chrome, None, None]:
    options = _build_chrome_options()
    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)

    drv.set_page_load_timeout(90)
    drv.set_script_timeout(90)

    yield drv

    drv.quit()
