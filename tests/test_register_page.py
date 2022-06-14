from tests.pages.locators import RegisterFormLocators, LoginFormLocators
from tests.pages.register_page import RegisterPage


def test_is_register_form(browser):
    link = RegisterFormLocators.Link
    page = RegisterPage(browser, link)
    page.open()
    page.should_be_register_form()


def test_register_new_user(browser):
    link = RegisterFormLocators.Link
    page = RegisterPage(browser, link)
    page.open()
    page.register_new_user()


def test_check_sign_up_href_from_login_page(browser):
    link = LoginFormLocators.Link
    page = RegisterPage(browser, link)
    page.open()
    page.check_sign_up_href()