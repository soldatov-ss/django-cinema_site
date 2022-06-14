from tests.pages.locators import LoginFormLocators, MainMenuLocators
from tests.pages.login_page import LoginPage


def test_is_register_form(browser):
    link = LoginFormLocators.Link
    page = LoginPage(browser, link)
    page.open()
    page.should_be_login_form()


def test_login_user(browser):
    link = LoginFormLocators.Link
    page = LoginPage(browser, link)
    page.open()
    page.login_user()


def test_login_wrong_user(browser):
    link = LoginFormLocators.Link
    page = LoginPage(browser, link)
    page.open()
    page.login_wrong_user()


def test_go_to_login_page_from_main_menu(browser):
    link = MainMenuLocators.Link
    page = LoginPage(browser, link)
    page.open()
    page.go_to_login_page_by_button()
