from __future__ import annotations

import allure
import pytest
import requests


@allure.title("API: проверка, что тестовая инфраструктура работает")
@allure.story("Smoke: запуск pytest + api маркера + requests.Session")
@pytest.mark.api
def test_api_smoke(
    api_session: requests.Session,
    base_url: str,
    api_timeout: int,
) -> None:
    with allure.step("Отправляем GET-запрос на /status/200"):
        response = api_session.get(
            f"{base_url}/status/200",
            timeout=api_timeout,
        )

    with allure.step("Проверяем, что статус-код 200"):
        assert response.status_code == 200
