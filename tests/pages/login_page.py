from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage
from tests.pages.locators import RegisterFormLocators, LoginFormLocators


class LoginPage(BasePage):

    def login_user(self):
        self.browser.find_element(*LoginFormLocators.Username).send_keys('admin')
        self.browser.find_element(*LoginFormLocators.Password).send_keys('admin')
        self.browser.find_element(*LoginFormLocators.SignBtn).click()
        assert self.browser.current_url != LoginFormLocators.Link, 'Logging user is not successful'

    def login_wrong_user(self):
        self.browser.find_element(*LoginFormLocators.Username).send_keys('WRONG')
        self.browser.find_element(*LoginFormLocators.Password).send_keys('WRONG')
        self.browser.find_element(*LoginFormLocators.SignBtn).click()
        warn_message = self.browser.find_element(By.TAG_NAME, 'strong').text

        assert warn_message.startswith('Please') or warn_message.startswith('Пожалуйста'), \
            'There is not any message about failed login'

    def should_be_login_form(self):
        assert self.browser.find_element(*RegisterFormLocators.Form), "Login page doesn't have login form"

    def go_to_login_page_by_button(self):
        self.browser.find_element(By.ID, 'djHideToolBarButton').click()  # убираем дебаг туллбар
        self.browser.find_element(*LoginFormLocators.Button).click()
        assert self.browser.current_url == LoginFormLocators.Link, 'Redirect to login page from main page was not successful'
