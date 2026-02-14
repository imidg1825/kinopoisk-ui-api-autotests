import pytest
import requests


@pytest.mark.api
def test_api_pos_01_search_cyrillic(
    api_session: requests.Session,
    base_url: str,
    api_timeout: int,
) -> None:
    resp = api_session.get(
        f"{base_url}/movie/search",
        params={"query": "Интерстеллар"},
        timeout=api_timeout,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "docs" in data
    assert len(data["docs"]) > 0


@pytest.mark.api
def test_api_pos_02_search_latin(
    api_session: requests.Session,
    base_url: str,
    api_timeout: int,
) -> None:
    resp = api_session.get(
        f"{base_url}/movie/search",
        params={"query": "Interstellar"},
        timeout=api_timeout,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "docs" in data
    assert len(data["docs"]) > 0


@pytest.mark.api
def test_api_pos_03_movie_by_id(
    api_session: requests.Session,
    base_url: str,
    api_timeout: int,
) -> None:
    search = api_session.get(
        f"{base_url}/movie/search",
        params={"query": "Interstellar"},
        timeout=api_timeout,
    )
    assert search.status_code == 200

    docs = search.json().get("docs", [])
    assert docs, "Empty docs from search"

    movie_id = docs[0].get("id")
    assert movie_id is not None

    movie = api_session.get(
        f"{base_url}/movie/{movie_id}",
        timeout=api_timeout,
    )
    assert movie.status_code == 200
    assert movie.json().get("id") == movie_id


@pytest.mark.api
def test_api_neg_01_no_token(
    base_url: str,
    api_timeout: int,
) -> None:
    s = requests.Session()
    s.headers.update(
        {
            "accept": "application/json",
            "User-Agent": "Mozilla/5.0",
        }
    )

    resp = s.get(
        f"{base_url}/movie/search",
        params={"query": "Interstellar"},
        timeout=api_timeout,
    )

    assert resp.status_code in (401, 403)


@pytest.mark.api
def test_api_neg_02_wrong_method_put(
    api_session: requests.Session,
    base_url: str,
    api_timeout: int,
) -> None:
    resp = api_session.put(
        f"{base_url}/movie/search",
        params={"query": "Interstellar"},
        timeout=api_timeout,
    )

    assert resp.status_code in (400, 404, 405)
