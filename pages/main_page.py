from __future__ import annotations

from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class MainPage:
    SEARCH_INPUT = (By.NAME, "kp_query")
    FILM_LINKS = (By.CSS_SELECTOR, "a[href*='/film/']")
    HEADER = (By.TAG_NAME, "header")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def open(self, url: str) -> None:
        self.driver.get(url)

    def wait_loaded(self, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.HEADER)
        )

    def search(self, text: str, timeout: int = 10) -> None:
        search_input = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(text)
        search_input.send_keys(Keys.ENTER)

    def wait_results(self, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.FILM_LINKS)
        )

    def results(self) -> List[WebElement]:
        return self.driver.find_elements(*self.FILM_LINKS)
