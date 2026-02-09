import asyncio
import time
from types import coroutine
from abc import ABC, abstractmethod
from playwright.async_api import async_playwright
from sympy import false
from torchgen.api.types import storageT
from collections import Counter
from src.Data.Keys import MA_pass as password, MA_phone as phone
from src.Test.DeepSeek import encode_to_base64

from src.Test.Module import capture_network_images
from DeepSeek import BaseAi
import base64


def insert():
    # Ваша функция вставки данных
    pass


def encode_to_base64(image_path):
    with open(image_path, 'rb') as image:
        file = image.read()
        encode_file = base64.b64encode(file)
        result = encode_file.decode('utf-8')
        return result


async def task_detector(page) -> set:
    metro_price = page.wait_for_selector(
        selector='.form-group input[name="metro_price"]',
        state="visible"
    )
    promo_price = page.wait_for_selector(
        selector='.form-group input[name="promo_price"]',
        state="visible"
    )
    card_price = page.wait_for_selector(
        selector='.form-group input[name="card_price"]',
        state="visible"
    )
    product_description = page.wait_for_selector(
        selector='.form-group.ng-scope:has(h4:has-text("Описание товара"))',
        state="visible"
    )
    product_title = page.wait_for_selector(
        selector='.form-group.ng-scope:has(h4:has-text("Название товара"))',
        state="visible"
    )
    button_save = page.wait_for_selector(
        selector='.form-group button[ng-click="accept()"]',
        state="visible"
    )

    button_cant_do = page.wait_for_selector(
        selector='.form-group button[ng-click="sendToUnsolved()"]',
        state="visible"
    )

    button_no_price = page.wait_for_selector(
        selector='.form-group button[ng-click="sendToUnsolved()"]',
        state='visible'
    )

    article_input = page.wait_for_selector(
        selector='.btn-group input#sku_code',
        state="visible"
    )

    text_area = page.wait_for_selector(
        selector='.form-group textarea#sku_title',
        state="visible"
    )

    button_cant_end = page.wait_for_selector(
        selector='#no',
        state="visible"
    )

    level_detection = page.wait_for_selector(
        selector='h4:has-text("Укажите уровни товарной позиции:")',
        state="visible"
    )

    level1_select = page.wait_for_selector(
        selector='select[ng-model="temp.level1"]',
        state="visible"
    )

    level2_select = page.wait_for_selector(
        selector='select[ng-model="temp.level2"]',
        state="visible"
    )

    level3_select = page.wait_for_selector(
        selector='select[ng-model="temp.level3"]',
        state="visible"
    )

    level4_select = page.wait_for_selector(
        selector='select[ng-model="temp.level4"]',
        state="visible"
    )

    no_code = page.wait_for_selector(
        selector='button[ng-click="reject(true)"]',
        state="visible"
    )

    cant_scan_code = page.wait_for_selector(
        selector='button[ng-click="reject(false)"]',
        state="visible"
    )

    barcode = page.wait_for_selector(
        selector='#barcode',
        state="visible"
    )

    page_storage = PageStorage()

    metro_price_task = asyncio.create_task(check_element2(metro_price, 2000, page_storage.storage, 'metro_price'))
    promo_price_task = asyncio.create_task(check_element2(promo_price, 2000, page_storage.storage, 'promo_price'))
    button_save_task = asyncio.create_task(check_element2(button_save, 2000, page_storage.storage, 'button_save'))
    button_cant_do_task = asyncio.create_task(
        check_element2(button_cant_do, 2000, page_storage.storage, 'button_cant_do'))
    button_no_price_task = asyncio.create_task(
        check_element2(button_no_price, 2000, page_storage.storage, 'button_no_price'))
    article_input_task = asyncio.create_task(check_element2(article_input, 2000, page_storage.storage, 'article_input'))
    text_area_task = asyncio.create_task(check_element2(text_area, 2000, page_storage.storage, 'text_area'))
    card_price_task = asyncio.create_task(check_element2(card_price, 2000, page_storage.storage, 'card_price'))
    product_description_task = asyncio.create_task(
        check_element2(product_description, 2000, page_storage.storage, 'product_description'))
    product_title_task = asyncio.create_task(check_element2(product_title, 2000, page_storage.storage, 'product_title'))
    button_cant_end_task = asyncio.create_task(
        check_element2(button_cant_end, 2000, page_storage.storage, 'button_cant_end'))
    level_detection_task = asyncio.create_task(
        check_element2(level_detection, 2000, page_storage.storage, 'level_detection'))

    level1_select_task = asyncio.create_task(check_element2(level1_select, 2000, page_storage.storage, 'level1_select'))
    level2_select_task = asyncio.create_task(check_element2(level2_select, 2000, page_storage.storage, 'level2_select'))
    level3_select_task = asyncio.create_task(check_element2(level3_select, 2000, page_storage.storage, 'level3_select'))
    level4_select_task = asyncio.create_task(check_element2(level4_select, 2000, page_storage.storage, 'level4_select'))

    no_code_task = asyncio.create_task(check_element2(no_code, 2000, page_storage.storage, 'no_code'))
    cant_scan_code_task = asyncio.create_task(
        check_element2(cant_scan_code, 2000, page_storage.storage, 'cant_scan_code'))
    barcode_task = asyncio.create_task(check_element2(barcode, 2000, page_storage.storage, 'barcode'))
    tasks = [metro_price_task, promo_price_task, button_save_task, button_cant_do_task, article_input_task,
             text_area_task, card_price_task, product_description_task, product_title_task, button_cant_end_task,
             level_detection_task, level1_select_task, level2_select_task, level3_select_task, level4_select_task,
             no_code_task, cant_scan_code_task, button_no_price_task, barcode_task]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    # print(f'done: {done}\npending: {pending}')
    # for task in done:
    #     print(f'task: {task.result()}')
    #     element, found = task.result()
    #     print(f'element, found: {element},{found}')

    active_elements = set()
    for element in page_storage.storage:
        print(f'element: {element} - {page_storage.storage[element]}')
        if page_storage.storage[element]:
            active_elements.add(element)
    print(active_elements)
    return active_elements

class Element(ABC):
    def __init__(self, selector:str):
        self.selector = selector
        self.page = None

    def set_page(self, new_page):
        self.page = new_page

class MetroPrice(Element):
    def __init__(self):
        super().__init__(selector='.form-group input[name="metro_price"]')

    def check(self):
        coroutine = self.page.wait_for_selector(
            selector=self.selector,
            state = 'visible'
        )
        asyncio.wait_for(coroutine, timeout=2)


class Page(ABC):
    def __init__(self):
        self.Elements = list()

    def evaluate(self, DetectedElemets: set) -> bool:
        try:
            if (Counter(self.Elements) == Counter(DetectedElemets)):
                return True
            else:
                return False
        except Exception as e:
            print(f'Сравнение страницы {self.__class__.__name__} прошло с ошибкой: {e}')

class PagePromoPrice(Page):
    def __init__(self):
        self.Elements = ['']

async def task_detector2(page):
    titles_corutines = []
    # for i in range(1, 7):
    #     titles = await page.locator(selector='.form-group h4')
    #     titles_corutines.append()
    # a = await asyncio.wait()
    # all_title = await page.locator(selector= '.form-group h4').all()
    # for element in all_title:
    #     text = await element.text_content()
    #     print(f"Текст: {text}")


class PageStorage:
    def __init__(self):
        self.storage = {}


async def check_element2(coroutine, timeout, page_st, coroutine_name):
    try:
        element = await asyncio.wait_for(coroutine, timeout / 1000)
        page_st[coroutine_name] = True  # !
        return element, True
    except (TimeoutError, asyncio.TimeoutError):
        page_st[coroutine_name] = False
        return None, False


async def check_element(coroutine, timeout):
    try:
        element = await asyncio.wait_for(coroutine, timeout / 1000)
        return element, True
    except (TimeoutError, asyncio.TimeoutError):
        return None, False


async def event_driven_automation():
    """Действительно event-driven подход как в JavaScript"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        print(1)
        context = await browser.new_context()
        print(2)
        page = await context.new_page()
        print(3)
        await page.goto("https://m54.millionagents.com/conveyor_new/jobs", wait_until="domcontentloaded", timeout=60000)
        print(4)
        try:
            waiting_phone = await page.wait_for_selector(
                "#phone",
                state="visible",
                timeout=1000
            )
            print('phone detected!')
            waiting_password = await page.wait_for_selector(
                "#password",
                state="visible",
                timeout=1000
            )
            print('password detected!')
            waiting_button = await page.wait_for_selector(
                'button.btn-primary[type="submit"]',
                state="visible",
                timeout=1000
            )
            print('waiting_button detected!')

            await waiting_phone.fill(phone)
            await waiting_password.fill(password)
            await waiting_button.click()

        except Exception as e:
            print(f'Элемент не найден: {e}')

        time.sleep(3)
        print("1. Ожидание загрузки страницы...")

        attempt = 0
        while True:
            attempt += 1
            print(f"\nПопытка #{attempt}")
            try:
                button, found = await check_element((page.wait_for_selector(
                    selector="button:has-text('Попробовать взять работу еще раз')",
                    state="visible")), 2000)
                if found:
                    print("Это все еще страница ожидания - кликаем по кнопке...")
                    await button.click()
                    await asyncio.sleep(1)
                else:
                    print(f"Страница с заданием загружена!")
                    break
            except Exception as e:
                print(f"Произошла ошибка при попытке найти кнопку на странице: {e}")
                return False

        try:
            # Ждем поле ввода
            input_field = page.wait_for_selector(
                'input[name="metro_price"]',
                state='visible',
            )

            input_field, input_found = await check_element(input_field, 2000)
            print(f"Input_field: {input_field}")
            if input_found:
                print("Поле ввода найдено!")
                await input_field.click()
                await asyncio.sleep(1)
            else:
                print("Поле ввода НЕ найдено")
            metro_price = page.wait_for_selector(
                selector='.form-group input[name="metro_price"]',
                state="visible"
            )
            promo_price = page.wait_for_selector(
                selector='.form-group input[name="promo_price"]',
                state="visible"
            )
            button_save = page.wait_for_selector(
                selector='.form-group button[ng-click="accept()"]',
                state="visible"
            )

            button_cant_do = page.wait_for_selector(
                selector='.form-group button[ng-click="sendToUnsolved()"]'
            )

        except Exception as e:
            print(f"Ошибка при заполнении формы: {e}")
        try:
            print(f"task_detector:")
            await task_detector(page)
            print(f"task_detector is ended")
            task1 = asyncio.create_task(check_element(metro_price, 2000))
            task2 = asyncio.create_task(check_element(promo_price, 2000))
            task3 = asyncio.create_task(check_element(button_save, 2000))
            task4 = asyncio.create_task(check_element(button_cant_do, 2000))

            done, pending = await asyncio.wait([task1, task2], return_when=asyncio.ALL_COMPLETED)
            print(f'done: {done}\npending: {pending}')
            for task in done:
                print(f'task: {task.result()}')
                element, found = task.result()
                print(f'element, found: {element},{found}')

            if input_found:
                print("Поле ввода найдено!")
                await input_field.click()
                await asyncio.sleep(1)
            else:
                print("Поле ввода НЕ найдено")
        except Exception as e:
            print(f"Ошибка при поиске текста: {e}")

        print("Загрузка изображений...")
        # Вариант 1/2: Перехват сетевых запросов
        await capture_network_images(page)
        print("Скачивание завершено\nНачинаем отправку изображения...")
        image = encode_to_base64("network_images/network_img_1.jpg")
        # ai = BaseAi()
        # ai.set_image(image)
        # Теперь заполняем форму
        print("\nНачинаем заполнение формы...")

        # Пауза для проверки
        print("\n⏸️ Пауза 10 секунд для проверки...")
        await asyncio.sleep(10)
        time.sleep(1000)
        return False  # Завершаем цикл


# Запуск
if __name__ == "__main__":
    asyncio.run(event_driven_automation())
