import pytest

from tests.pages.catalog_page import CatalogPage
from tests.pages.locators import MainMenuLocators, RegisterFormLocators, LoginFormLocators, CatalogLocators


@pytest.mark.parametrize('link', [MainMenuLocators.Link, RegisterFormLocators.Link, LoginFormLocators.Link])
def test_go_to_catalog_page_by_button(browser, link):
    page = CatalogPage(browser, link)
    page.open()
    page.go_to_catalog_page()


@pytest.mark.parametrize('genre', ['боевик', 'триллер', 'драма', 'приключения'])
def test_select_genre(browser, genre):
    link = CatalogLocators.Link
    page = CatalogPage(browser, link)
    page.open()
    page.select_genre(genre)