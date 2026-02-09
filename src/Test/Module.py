import os
import aiohttp
import asyncio
from urllib.parse import urlparse


# async def download_jpegs_from_playwright_page(page, save_folder="downloaded_images", max_images=50):
#     """
#     Скачивает JPEG изображения из текущей страницы Playwright
#
#     Args:
#         page: текущая страница Playwright
#         save_folder: папка для сохранения
#         max_images: максимальное количество изображений для скачивания
#     """
#
#     print("🔍 Начинаю поиск JPEG изображений на текущей странице...")
#
#     # Создаем папку для сохранения
#     os.makedirs(save_folder, exist_ok=True)
#
#     # Собираем все URL изображений со страницы
#     image_urls = []
#
#     # 1. Получаем все элементы img
#     img_elements = await page.query_selector_all('img')
#     print(f"Найдено {len(img_elements)} элементов img")
#
#     for img in img_elements:
#         try:
#             src = await img.get_attribute('src')
#             if src and src.startswith('http'):
#                 image_urls.append(src)
#         except:
#             pass
#     print(f"🔐Найдено URL 1 (Получаем все элементы img):{image_urls}")
#     # 2. Ищем изображения в стилях (background-image)
#     try:
#         elements_with_bg = await page.query_selector_all('*')
#         for element in elements_with_bg[:100]:  # Ограничиваем для производительности
#             try:
#                 style = await element.get_attribute('style')
#                 if style and 'background-image' in style:
#                     # Извлекаем URL из background-image
#                     import re
#                     urls = re.findall(r'url\(["\']?(https?://[^"\')]+)["\']?\)', style)
#                     image_urls.extend(urls)
#             except:
#                 continue
#     except:
#         pass
#
#     print(f"🔐Найдено URL 2 (Ищем изображения в стилях (background-image)):{image_urls}")
#
#     # 3. Ищем в canvas элементах (делаем скриншоты)
#     canvas_elements = await page.query_selector_all('canvas')
#     print(f"Найдено {len(canvas_elements)} элементов canvas")
#
#     for i, canvas in enumerate(canvas_elements):
#         try:
#             # Делаем скриншот canvas
#             screenshot_path = os.path.join(save_folder, f"canvas_{i}.png")
#             await canvas.screenshot(path=screenshot_path)
#             print(f"Сохранен скриншот canvas: canvas_{i}.png")
#         except:
#             pass
#
#     # 4. Получаем все ответы с изображениями (через перехват network)
#     jpeg_responses = []
#
#     def on_response(response):
#         """Обработчик сетевых ответов"""
#         try:
#             content_type = response.headers.get('content-type', '').lower()
#             url = response.url
#
#             # Проверяем JPEG
#             if ('image/jpeg' in content_type or
#                     url.lower().endswith(('.jpg', '.jpeg'))):
#                 if url not in jpeg_responses:
#                     jpeg_responses.append(url)
#                     print(f"Найден JPEG в сети: {url[:80]}...")
#
#             print(f"🔐Найдено URL 4 (Получаем все ответы с изображениями (через перехват network)):{content_type}")
#         except:
#             pass
#
#     # Включаем перехватчик ответов
#     page.on("response", on_response)
#
#
#
#     # Ждем немного для сбора запросов
#     await asyncio.sleep(2)
#
#     # 5. Выполняем JS для поиска всех изображений
#     try:
#         all_image_urls = await page.evaluate("""
#             () => {
#                 const urls = new Set();
#
#                 // 1. Все img элементы
#                 document.querySelectorAll('img').forEach(img => {
#                     if (img.src) urls.add(img.src);
#                 });
#
#                 // 2. CSS background images
#                 const allElements = document.querySelectorAll('*');
#                 allElements.forEach(el => {
#                     const bg = window.getComputedStyle(el).backgroundImage;
#                     if (bg && bg.startsWith('url')) {
#                         const match = bg.match(/url\\(["']?([^"')]+)["']?\\)/);
#                         if (match && match[1]) {
#                             const url = match[1];
#                             if (url.startsWith('http')) urls.add(url);
#                         }
#                     }
#                 });
#
#                 // 3. В data-атрибутах
#                 document.querySelectorAll('[data-src], [data-image]').forEach(el => {
#                     const src = el.getAttribute('data-src') || el.getAttribute('data-image');
#                     if (src && src.startsWith('http')) urls.add(src);
#                 });
#
#                 return Array.from(urls).filter(url =>
#                     url.toLowerCase().includes('.jpg') ||
#                     url.toLowerCase().includes('.jpeg') ||
#                     url.includes('/jpeg') ||
#                     url.includes('/jpg')
#                 );
#             }
#         """)
#         print(f"Найдено URL 5.1:{image_urls}")
#         image_urls.extend(all_image_urls)
#         print(f"Найдено URL 5.2:{image_urls}")
#     except Exception as e:
#         print(f"Ошибка при выполнении JS: {e}")
#
#     # 6. Объединяем все найденные URL
#     all_urls = list(set(image_urls + jpeg_responses))
#
#     # Фильтруем только JPEG
#     jpeg_urls = []
#     for url in all_urls:
#         url_lower = url.lower()
#         if ('.jpg' in url_lower or
#                 '.jpeg' in url_lower or
#                 '/jpg' in url_lower or
#                 '/jpeg' in url_lower):
#             jpeg_urls.append(url)
#
#     jpeg_urls = list(set(jpeg_urls))[:max_images]
#     print(f"Найдено {len(jpeg_urls)} уникальных JPEG URL")
#
#     if not jpeg_urls:
#         print("⚠️ JPEG изображения не найдены")
#         return []
#
#     # Скачиваем изображения
#     downloaded = []
#
#     async with aiohttp.ClientSession() as session:
#         for i, img_url in enumerate(jpeg_urls):
#             try:
#                 # Получаем имя файла
#                 filename = os.path.basename(urlparse(img_url).path)
#                 if not filename or '.' not in filename:
#                     filename = f"image_{i}.jpg"
#
#                 # Очищаем имя файла
#                 filename = "".join(c for c in filename if c.isalnum() or c in '._-')
#
#                 save_path = os.path.join(save_folder, filename)
#
#                 print(f"⬇️ Скачиваю ({i + 1}/{len(jpeg_urls)}): {filename[:50]}...")
#
#                 async with session.get(img_url, timeout=10) as response:
#                     if response.status == 200:
#                         content = await response.read()
#
#                         # Проверяем, что это действительно изображение
#                         if len(content) > 100:  # Минимальный размер
#                             with open(save_path, 'wb') as f:
#                                 f.write(content)
#                             downloaded.append(save_path)
#                             print(f"   ✓ Сохранено ({len(content)} байт)")
#                         else:
#                             print(f"   ⚠️ Файл слишком мал ({len(content)} байт)")
#                     else:
#                         print(f"   ✗ Ошибка HTTP: {response.status}")
#
#             except Exception as e:
#                 print(f"   ✗ Ошибка: {str(e)[:50]}...")
#
#     print(f"Скачано {len(downloaded)} JPEG изображений в папку '{save_folder}'")
#     return downloaded


# Альтернативная версия: перехват через request/response
async def capture_network_images(page, save_folder="network_images"):
    """
    Перехватывает и скачивает изображения из сетевых запросов
    """
    await page.reload()
    os.makedirs(save_folder, exist_ok=True)
    captured_urls = []

    def on_response(response):
        """Обработчик для перехвата изображений"""
        content_type = response.headers.get('content-type', '')
        url = response.url

        if ('image/jpeg' in content_type.lower() or
                'image/png' in content_type.lower() or
                'image/webp' in content_type.lower()):

            if url not in captured_urls:
                captured_urls.append(url)
                print(f"Перехвачено: {url[:80]}...")

    # Подписываемся на события
    page.on("response", on_response)

    # Ждем некоторое время для сбора запросов
    print("Слушаю сетевые запросы... (3 секунды)")
    await asyncio.sleep(3)

    # Скачиваем перехваченные изображения
    downloaded = []
    async with aiohttp.ClientSession() as session:
        for i, url in enumerate(captured_urls[:20]):  # Ограничиваем
            try:
                filename = f"network_img_{i}.jpg"
                if 'png' in url.lower():
                    filename = f"network_img_{i}.png"

                save_path = os.path.join(save_folder, filename)

                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        content = await response.read()
                        with open(save_path, 'wb') as f:
                            f.write(content)
                        downloaded.append(save_path)
                        print(f"Скачано: {filename}")

            except Exception as e:
                print(f"Ошибка при скачивании {url[:50]}: {e}")

    print(f"Скачано {len(downloaded)} изображений")
    return downloaded