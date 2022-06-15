import pytest

from tests.pages.locators import MainMenuLocators
from tests.pages.main_page import MainPage


def test_change_language_from_main_page(browser):
    link = MainMenuLocators.Link
    page = MainPage(browser, link)
    page.open()
    page.change_language()


@pytest.mark.parametrize('movie', ['Матрица: Воскрешение', 'воСкРешение', 'Матриц', 'король', 'КОРОЛЬ'])
def test_search_movie(browser, movie):
    link = MainMenuLocators.Link
    page = MainPage(browser, link)
    page.open()
    page.search_movie(movie)


