from selenium.webdriver.common.by import By


class RegisterFormLocators:
    Form = (By.CLASS_NAME, 'sign__form')
    Link = 'http://127.0.0.1:8000/en/register/'


class LoginFormLocators:
    Link = 'http://127.0.0.1:8000/en/login/'
    Form = (By.CLASS_NAME, 'sign__form')
    Button = (By.CLASS_NAME, 'header__sign-in')
    Username = (By.NAME, 'username')
    Password = (By.NAME, 'password')
    SignBtn = (By.CLASS_NAME, 'sign__btn')


class MainMenuLocators:
    Link = 'http://127.0.0.1:8000/'


class CatalogLocators:
    Link = 'http://127.0.0.1:8000/catalog/1/'