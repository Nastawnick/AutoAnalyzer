import cv2
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
from pathlib import Path

# Настройка Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_image(image_path):
    # Загружаем изображение
    image = cv2.imread(image_path)

    # Конвертируем в оттенки серого (улучшает распознавание)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применяем пороговую обработку (бинаризация)
    _, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Сохраняем временное изображение (опционально)
    cv2.imwrite("temp_threshold.png", threshold)

    # Используем Tesseract для распознавания текста
    text = pytesseract.image_to_string(threshold, lang='rus+eng')  # 'rus' для русского
    data = pytesseract.image_to_data(threshold, lang='rus+eng')

    return text.strip()


def input_text_to_browser(text, url="https://example.com", field_selector=("id", "input-field-id")):
    try:
        print("Инициализация браузера Chrome...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        print(f"Открываю URL: {url}")
        driver.get(url)
        time.sleep(2)  # Ожидание загрузки страницы

        # Стратегии поиска поля ввода
        locator_types = {
            "id": By.ID,
            "name": By.NAME,
            "xpath": By.XPATH,
            "css": By.CSS_SELECTOR,
            "class": By.CLASS_NAME
        }

        locator_type, locator_value = field_selector
        by_method = locator_types.get(locator_type.lower(), By.ID)

        print(f"Ищу поле ввода по {locator_type}: {locator_value}")
        try:
            input_field = driver.find_element(by_method, locator_value)
            input_field.clear()
            input_field.send_keys(text)
            print(f"Текст успешно введён в поле: {text}")

            # Дополнительные действия (например, нажатие Enter)
            # input_field.send_keys(Keys.RETURN)

            time.sleep(5)  # Пауза для визуальной проверки
        except NoSuchElementException:
            print(f"Не удалось найти поле ввода по {locator_type}: {locator_value}")
            print("Попробуйте изменить селектор или проверить структуру страницы")

    except Exception as e:
        print(f"Ошибка в работе браузера: {e}")
    finally:
        driver.quit()
        print("Браузер закрыт")


if __name__ == "__main__":
    # Путь к изображению относительно корня проекта
    image_name = "Screen.png"
    image_path = Path(__file__).parent.parent / "data" / "input" / image_name

    print(f"Обработка изображения: {image_path}")
    extracted_text = extract_text_from_image(image_path)

    if extracted_text:
        print(f"Финальный распознанный текст: {extracted_text}")

        # Настройки для целевой страницы (измените под ваши нужды)
        target_url = "https://google.com"  # Замените на ваш URL
        field_locator = ("id", "APjFqb")  # Замените на ваш селектор

        input_text_to_browser(
            extracted_text,
            url=target_url,
            field_selector=field_locator
        )
    else:
        print("Не удалось распознать текст. Проверьте качество изображения.")