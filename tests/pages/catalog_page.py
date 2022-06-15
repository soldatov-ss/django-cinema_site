from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class CatalogPage(BasePage):

    def go_to_catalog_page(self):
        self.browser.find_element(By.XPATH, "//a[contains(@href, '/catalog/1/')]").click()
        assert self.browser.current_url.endswith('/catalog/1/')

    def select_genre(self, genre):
        self.browser.find_element(By.NAME, 'genre').click()
        self.browser.find_element(By.XPATH, f"//li[@data-value='{genre.lower()}']").click()
        self.browser.find_element(By.ID, 'djHideToolBarButton').click()  # убираем дебаг туллбар
        self.browser.find_element(By.CLASS_NAME, 'filter__btn').click()
        movie_genres = [i.text.split() for i in self.browser.find_elements(By.CLASS_NAME, 'card__category')]
        assert any(genre.title() in i for i in movie_genres)
