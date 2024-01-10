import chromedriver_autoinstaller
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC

chromedriver_autoinstaller.install()


@pytest.fixture(autouse=True)
def web_driver():
    web_driver = webdriver.Chrome()

    # Переходим на страницу авторизации
    web_driver.get('https://petfriends.skillfactory.ru/login')

    web_driver.maximize_window()
    yield web_driver

    web_driver.quit()

"""явное ожидание"""


def test_show_my_pets(web_driver):
    """Проверяем, что присутствуют все питомцы:
        -находим кол-во питомцев по статистике и провер что кол-во соотв числу в таблице"""
    wdw(web_driver, 5).until(EC.presence_of_element_located((By.ID, 'email')))
    web_driver.find_element(By.ID, 'email').send_keys('Vera.Mitchenko@geropharm.com')
    # Вводим пароль
    web_driver.find_element(By.ID, 'pass').send_keys('vera2205')
    # Нажимаем на кнопку входа в аккаунт
    web_driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    # assert web_driver.find_element(By.TAG_NAME, 'h1').text == 'PetFriends'
    assert web_driver.current_url == 'https://petfriends.skillfactory.ru/all_pets'


    web_driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()
    # Нажимаем на кнопку Мои питомцы
    # web_driver.find_element(By.CSS_SELECTOR, '#navbarNav > ul > li:nth-child(1) > a').click()

    # assert web_driver.find_element(By.TAG_NAME, 'h2').text == "JetiMax"
    pets_number = web_driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    pets_count = web_driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    assert int(pets_number) == len(pets_count)