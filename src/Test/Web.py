from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from collections import defaultdict
import json

from src.Data.Keys import MA_pass as password, MA_phone as phone


def get_classes_and_ids_selenium(url):
    # Словари для хранения результатов
    print('start')
    classes = defaultdict(list)
    ids = {}
    all_elements = []

    try:
        print('step 1')
        # Находим все элементы
        elements = driver.find_elements(By.XPATH, "//*")

        for element in elements:
            try:
                tag_name = element.tag_name
                class_list = element.get_attribute("class").split() if element.get_attribute("class") else []
                element_id = element.get_attribute("id")
                text_content = element.text[:100] if element.text else ""

                element_info = {
                    'tag': tag_name,
                    'classes': class_list,
                    'id': element_id,
                    'text': text_content
                }
                all_elements.append(element_info)

                # Собираем классы
                for class_name in class_list:
                    classes[class_name].append({
                        'tag': tag_name,
                        'id': element_id
                    })

                # Собираем ID
                if element_id:
                    ids[element_id] = {
                        'tag': tag_name,
                        'classes': class_list
                    }

            except Exception as e:
                print(f"Ошибка при обработке элемента: {e}")
                continue

    finally:
        return {
            'all_elements': all_elements,
            'classes': dict(classes),
            'ids': ids
        }

# Настройка драйвера
driver = webdriver.Chrome()  # Укажите путь к драйверу, если необходимо
driver.get("https://m54.millionagents.com/conveyor_new/jobs")

# Ожидание появления полей ввода
# import asyncio

print('STOP')

wait = WebDriverWait(driver, 10)

# Ввод номера телефона
phone_field = wait.until(EC.presence_of_element_located((By.ID, "phone")))  # Замените "phone" на актуальное имя поля
phone_field.send_keys(phone)

time.sleep(2)

password_filed = wait.until(EC.presence_of_element_located((By.ID, "password")))
password_filed.send_keys(password)

time.sleep(2)

login_button = driver.find_element(By.CLASS_NAME, "btn")
login_button.click()
try:
    wait = WebDriverWait(driver, 10)
    canvas = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas.upper-canvas")))
except:
    print('no canvas')
time.sleep(2)

Input_ID = ['sku_title', 'sku_code']
Input_name = ['metro_price', 'promo_price']
Classes = ['form-control']
time.sleep(2)
try:
    url = driver.current_url
    print(url)
    print(f'{get_classes_and_ids_selenium(url)['ids']}\n')
    print(f'\n{print(get_classes_and_ids_selenium(url)['classes'])}')
    input_filed = wait.until(EC.presence_of_element_located((By.ID, "sku_title")))
    input_filed.send_keys("100")
except:
    print("No id")


time.sleep(180)
driver.quit()