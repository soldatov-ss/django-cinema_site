import time

from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage
from tests.pages.locators import RegisterFormLocators


class RegisterPage(BasePage):

    def should_be_register_form(self):
        assert self.browser.find_element(*RegisterFormLocators.Form), "Register page doesn't have register form"

    def register_new_user(self):
        email, password, username = self.create_new_user()

        self.browser.find_element(By.NAME, 'email').send_keys(email)
        self.browser.find_element(By.NAME, 'username').send_keys(username)
        self.browser.find_element(*RegisterFormLocators.Form).find_element(By.NAME, 'password1').send_keys(
            password)
        self.browser.find_element(*RegisterFormLocators.Form).find_element(By.NAME, 'password2').send_keys(
            password)
        self.browser.find_element(By.CLASS_NAME, 'sign__btn').click()
        time.sleep(1)
        assert self.browser.current_url != RegisterFormLocators.Link, 'Registration was not ended'


    def check_sign_up_href(self):
        self.browser.find_element(By.CLASS_NAME, 'sign__text').find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)
        assert self.browser.current_url == RegisterFormLocators.Link, "Sign up from login page doesn't work"
