import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def open_main(driver: WebDriver, base_url: str) -> None:
    driver.get(base_url)


def search_movie(driver: WebDriver, query: str) -> None:
    search_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "kp_query"))
    )
    search_input.clear()
    search_input.send_keys(query)
    search_input.submit()


def wait_results_page(driver: WebDriver) -> None:
    WebDriverWait(driver, 30).until(lambda d: "kp_query=" in d.current_url)


def open_first_film_link(driver: WebDriver) -> None:
    first_link = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/film/']"))
    )
    first_link.click()


@allure.story("UI")
@allure.title("UI-01: Поиск фильма — URL содержит kp_query")
@pytest.mark.ui
def test_ui_01_search_movie(driver: WebDriver, ui_base_url: str) -> None:
    with allure.step("Открываем главную"):
        open_main(driver, ui_base_url)

    with allure.step("Ищем Interstellar"):
        search_movie(driver, "Interstellar")

    with allure.step("Ждём результаты"):
        wait_results_page(driver)

    with allure.step("Проверяем kp_query в URL"):
        assert "kp_query=" in driver.current_url


@allure.story("UI")
@allure.title("UI-02: На главной есть поле поиска kp_query")
@pytest.mark.ui
def test_ui_02_search_field_present(driver: WebDriver, ui_base_url: str) -> None:
    with allure.step("Открываем главную"):
        open_main(driver, ui_base_url)

    with allure.step("Ждём поле поиска"):
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "kp_query"))
        )

    with allure.step("Проверяем что поле найдено"):
        assert element is not None


@allure.story("UI")
@allure.title("UI-03: Заголовок страницы не пустой")
@pytest.mark.ui
def test_ui_03_title_not_empty(driver: WebDriver, ui_base_url: str) -> None:
    with allure.step("Открываем главную"):
        open_main(driver, ui_base_url)

    with allure.step("Проверяем title"):
        assert driver.title.strip() != ""


@allure.story("UI")
@allure.title("UI-04: Открываем карточку фильма из результатов поиска")
@pytest.mark.ui
def test_ui_04_open_movie_from_results(driver: WebDriver, ui_base_url: str) -> None:
    with allure.step("Открываем главную"):
        open_main(driver, ui_base_url)

    with allure.step("Ищем Interstellar"):
        search_movie(driver, "Interstellar")

    with allure.step("Ждём результаты"):
        wait_results_page(driver)

    with allure.step("Открываем первый результат (film link)"):
        open_first_film_link(driver)

    with allure.step("Проверяем URL содержит /film/"):
        assert "/film/" in driver.current_url


@allure.story("UI")
@allure.title("UI-05: Page source не пустой")
@pytest.mark.ui
def test_ui_05_page_source_not_empty(driver: WebDriver, ui_base_url: str) -> None:
    with allure.step("Открываем главную"):
        open_main(driver, ui_base_url)

    with allure.step("Проверяем, что HTML не пустой"):
        assert len(driver.page_source) > 1000
