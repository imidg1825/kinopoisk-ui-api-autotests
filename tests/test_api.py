from __future__ import annotations

import allure
import pytest
import requests


@allure.title("API: Поиск фильма по названию (кириллица)")
@allure.story("Search movie by name")
@pytest.mark.api
def test_search_movie_by_name(
    api_session: requests.Session,
    base_url: str,
    api_timeout: int,
) -> None:
    with allure.step("Отправляем GET-запрос на /movie/search"):
        response = api_session.get(
            f"{base_url}/movie/search",
            params={"query": "Интерстеллар"},
            timeout=api_timeout,
        )

    with allure.step("Проверяем, что статус-код 200"):
        assert (
            response.status_code == 200
        ), f"Status={response.status_code}, body={response.text}"

    with allure.step('Проверяем, что в ответе есть "docs" и там есть элементы'):
        data = response.json()
        assert "docs" in data, f'No "docs" in response: {data}'
        assert len(data["docs"]) > 0, "docs is empty"
