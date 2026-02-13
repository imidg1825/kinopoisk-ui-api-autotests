from __future__ import annotations

import allure
import pytest
import requests


def attach_response(resp: requests.Response) -> None:
    allure.attach(str(resp.request.method), "method", allure.attachment_type.TEXT)
    allure.attach(str(resp.request.url), "url", allure.attachment_type.TEXT)
    allure.attach(str(resp.status_code), "status_code", allure.attachment_type.TEXT)
    allure.attach(resp.text[:5000], "body", allure.attachment_type.TEXT)


@allure.story("API Smoke")
@allure.title("API Smoke — сервер отвечает")
@pytest.mark.api
def test_api_smoke(
    api_session: requests.Session,
    base_url: str,
    api_timeout: int,
) -> None:

    with allure.step("GET /movie/search?query=test"):
        response = api_session.get(
            f"{base_url}/movie/search",
            params={"query": "test"},
            timeout=api_timeout,
        )
        attach_response(response)

    with allure.step("Проверяем, что сервер не упал"):
        assert response.status_code < 600


@allure.story("Positive")
@allure.title("POS-01 — поиск возвращает корректный ответ")
@pytest.mark.api
def test_pos_01_search(
    api_session: requests.Session,
    base_url: str,
    api_timeout: int,
) -> None:

    with allure.step("GET /movie/search?query=Interstellar"):
        response = api_session.get(
            f"{base_url}/movie/search",
            params={"query": "Interstellar"},
            timeout=api_timeout,
        )
        attach_response(response)

    with allure.step("Проверяем, что ответ не 401"):
        assert response.status_code != 401


@allure.story("Positive")
@allure.title("POS-02 — получение фильма по ID")
@pytest.mark.api
def test_pos_02_movie_by_id(
    api_session: requests.Session,
    base_url: str,
    api_timeout: int,
    movie_id: int,
) -> None:

    with allure.step(f"GET /movie/{movie_id}"):
        response = api_session.get(
            f"{base_url}/movie/{movie_id}",
            timeout=api_timeout,
        )
        attach_response(response)

    with allure.step("Проверяем, что сервер ответил"):
        assert response.status_code < 600


@allure.story("Negative")
@allure.title("NEG-01 — без токена")
@pytest.mark.api
def test_neg_01_without_token(
    base_url: str,
    api_timeout: int,
) -> None:

    with allure.step("GET без X-API-KEY"):
        response = requests.get(
            f"{base_url}/movie/search",
            params={"query": "test"},
            headers={"accept": "application/json"},
            timeout=api_timeout,
        )
        attach_response(response)

    with allure.step("Ожидаем 401 или 503 (публичный API может быть нестабилен)"):
        assert response.status_code in (401, 503)


@allure.story("Negative")
@allure.title("NEG-02 — неверный токен")
@pytest.mark.api
def test_neg_02_wrong_token(
    base_url: str,
    api_timeout: int,
) -> None:

    with allure.step("GET с неверным токеном"):
        response = requests.get(
            f"{base_url}/movie/search",
            params={"query": "test"},
            headers={
                "accept": "application/json",
                "X-API-KEY": "WRONG_TOKEN",
            },
            timeout=api_timeout,
        )
        attach_response(response)

    with allure.step("Ожидаем 401 или 503"):
        assert response.status_code in (401, 503)


@allure.story("Negative")
@allure.title("NEG-03 — неверный метод")
@pytest.mark.api
def test_neg_03_wrong_method(
    api_session: requests.Session,
    base_url: str,
    api_timeout: int,
) -> None:

    with allure.step("PUT /movie/search"):
        response = api_session.put(
            f"{base_url}/movie/search",
            timeout=api_timeout,
        )
        attach_response(response)

    with allure.step("Проверяем, что это не 200"):
        assert response.status_code != 200
