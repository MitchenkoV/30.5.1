import time
import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()


@pytest.fixture(autouse=True)
def web_driver():
    web_driver = webdriver.Chrome()
    web_driver.implicitly_wait(10)
    web_driver.get('https://petfriends.skillfactory.ru/login')
    web_driver.maximize_window()
    yield web_driver
    web_driver.quit()


def test_cards_pets(web_driver):
    """Проверяем карточки питомцев"""
    # Вводим email, заменить на свой email для того чтобы получить свой список питомцев
    web_driver.find_element(By.ID, 'email').send_keys('Vera.Mitchenko@geropharm.com')
    # Вводим пароль
    web_driver.find_element(By.ID, 'pass').send_keys('vera2205')
    # Нажимаем на кнопку входа в аккаунт
    web_driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    assert web_driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    time.sleep(1)

    # Нажимаем на кнопку Мои питомцы
    web_driver.find_element(By.CSS_SELECTOR, 'div#navbarNav > ul > li > a').click()

    assert web_driver.find_element(By.TAG_NAME, 'div#navbarNav').text == "Мои питомцы"


    images = web_driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = web_driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = web_driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    for i in range(len(names)):
       image_source= images[i].get_attribute('src')
       name_text= names[i].text
       print(f"image source:{image_source}")
       print(f'image source:{name_text}')
       assert image_source != ''
       assert name_text != ''
       assert descriptions[i].text != ''
       assert ', ' in descriptions[i]
       parts = descriptions[i].text.split(", ")
       assert len(parts[0]) > 0
       assert len(parts[1]) > 0