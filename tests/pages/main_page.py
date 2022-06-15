from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class MainPage(BasePage):

    def get_current_language(self):
        self.browser.find_element(By.CLASS_NAME, 'ion-ios-more').click()
        current_language = self.current_language = self.browser.find_element(By.CLASS_NAME, 'choise_lang').text
        return current_language


    def change_language(self):
        current_language = self.get_current_language()
        if current_language == 'English':
            self.browser.find_element(By.XPATH, "//a[@href='/ru/']").click()
            assert current_language != self.get_current_language(), 'Language was not changed'
        elif current_language == 'Русский':
            self.browser.find_element(By.XPATH, "//a[@href='/en/']").click()
            assert current_language != self.get_current_language(), 'Language was not changed'


    def search_movie(self, movie):
        self.browser.find_element(By.CLASS_NAME, 'ion-ios-search').click()
        self.browser.find_element(By.NAME, 'q').send_keys(movie)
        btn = self.browser.find_element(By.NAME, "submit_button")
        self.browser.execute_script("arguments[0].click();", btn)
        movie_name = self.browser.find_element(By.CLASS_NAME, 'card__title').text.title()
        assert movie.title() in movie_name, 'Movie was not found by search'
