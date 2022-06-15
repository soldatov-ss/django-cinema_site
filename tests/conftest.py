import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import fake_useragent

def pytest_addoption(parser):
    parser.addoption('--browser_name', action='store', default='chrome',
                     help="Choose browser: chrome or firefox")

    parser.addoption('--language', action='store', default='ru',
                     help="Choose language, bro")


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    language = request.config.getoption("language")
    user_agent = fake_useragent.UserAgent().chrome
    browser = None

    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('window-size=1400,900')
    options.add_experimental_option('prefs', {'intl.accept_languages': language})
    options.add_argument(f'user-agent={user_agent}')

    if browser_name == "chrome":
        browser = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        fp = webdriver.FirefoxProfile()
        fp.set_preference("intl.accept_languages", language)
        browser = webdriver.Firefox(firefox_profile=fp)
    else:
        raise pytest.UsageError("--browser_name should be chrome or firefox")
    yield browser

    browser.quit()
