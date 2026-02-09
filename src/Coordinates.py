# import pyautogui
# import keyboard
# import time
# import pyperclip
#
#
# def get_mouse_position_with_hotkey():
#     """
#     Простая программа для получения координат мыши и ввода текста
#     с поддержкой русского языка
#     """
#     print("=== ПРОГРАММА ДЛЯ АВТОМАТИЧЕСКОГО ВВОДА ТЕКСТА ===")
#     print("Инструкция:")
#     print("1. Наведите курсор мыши на нужное место")
#     print("2. Нажмите up - сохранить координаты и ввести текст")
#     print("3. Нажмите F3 - просто кликнуть по координатам")
#     print("4. Нажмите ESC - выход из программы")
#     print("-" * 50)
#
#     saved_position = None
#     template_text = "Привет, это автоматический ввод текста!"  # Шаблонный текст
#
#     try:
#         while True:
#             # Показываем текущие координаты
#             if saved_position:
#                 print(
#                     f"\rТекущие координаты: {pyautogui.position()} | Сохраненные: {saved_position} | Ожидание клавиш...",
#                     end="", flush=True)
#             else:
#                 print(f"\rТекущие координаты: {pyautogui.position()} | Сохраненные: нет | Ожидание клавиш...", end="",
#                       flush=True)
#
#             # Обработка клавиш
#             if keyboard.is_pressed('up'):
#                 # Сохраняем текущую позицию
#                 print(f"\nВведите текст: ")
#                 template_text = str(input())
#                 time.sleep(1)
#                 saved_position = pyautogui.position()
#                 print(f"\n✓ Сохранены координаты: {saved_position}")
#
#                 # Кликаем и вводим текст через буфер обмена
#                 pyautogui.click(saved_position)
#                 time.sleep(0.3)
#
#                 # Копируем текст в буфер обмена и вставляем
#                 pyperclip.copy(template_text)
#                 pyautogui.hotkey('ctrl', 'v')  # Вставляем из буфера
#
#                 print(f"✓ Введен текст: '{template_text}'")
#                 time.sleep(0.5)
#
#             elif keyboard.is_pressed('f3'):
#                 # Просто кликаем по текущей позиции
#                 current_pos = pyautogui.position()
#                 pyautogui.click(current_pos)
#                 print(f"\n✓ Клик по координатам: {current_pos}")
#                 time.sleep(0.5)
#
#             elif keyboard.is_pressed('esc'):
#                 print("\n\n✓ Программа завершена")
#                 break
#
#             time.sleep(0.01)
#
#     except KeyboardInterrupt:
#         print("\n\n✓ Программа прервана пользователем")
#
#
# # Версия с настраиваемым текстом и поддержкой русского
# def advanced_version():
#     """
#     Версия с настройкой текста и поддержкой русского языка
#     """
#     print("=== РАСШИРЕННАЯ ВЕРСИЯ ===")
#     print("up - сохранить координаты и ввести текст")
#     print("F3 - кликнуть по текущим координатам")
#     print("F4 - изменить шаблон текста")
#     print("F5 - показать все сохраненные координаты")
#     print("ESC - выход")
#     print("-" * 40)
#
#     saved_positions = []
#     template_text = "Автоматический текст на русском"
#
#     try:
#         while True:
#             print(f"\rКоординаты: {pyautogui.position()} | Текст: '{template_text}' | Ожидание...", end="", flush=True)
#
#             if keyboard.is_pressed('up'):
#                 pos = pyautogui.position()
#                 saved_positions.append(pos)
#
#                 pyautogui.click(pos)
#                 time.sleep(0.2)
#
#                 # Используем буфер обмена для русского текста
#                 pyperclip.copy(template_text)
#                 pyautogui.hotkey('ctrl', 'v')
#
#                 print(f"\n✓ Сохранено: {pos} | Введен: '{template_text}'")
#                 time.sleep(0.3)
#
#             elif keyboard.is_pressed('f3'):
#                 pos = pyautogui.position()
#                 pyautogui.click(pos)
#                 print(f"\n✓ Клик: {pos}")
#                 time.sleep(0.3)
#
#             elif keyboard.is_pressed('f4'):
#                 print("\n")  # Новая строка
#                 new_text = input("Введите новый текст: ")
#                 if new_text.strip():
#                     template_text = new_text
#                     print(f"✓ Новый текст: '{template_text}'")
#
#             elif keyboard.is_pressed('f5'):
#                 print(f"\nСохраненные координаты ({len(saved_positions)}):")
#                 for i, pos in enumerate(saved_positions, 1):
#                     print(f"  {i}. {pos}")
#
#             elif keyboard.is_pressed('esc'):
#                 print("\n✓ Выход из программы")
#                 break
#
#             time.sleep(0.01)
#
#     except KeyboardInterrupt:
#         print("\n✓ Программа завершена")
#
#
# # Максимально простая версия с русской раскладкой
# def simple_click_type():
#     """
#     Максимально простая версия с поддержкой русского
#     """
#     print("Наведите мышь и нажмите up для ввода текста")
#     print("Нажмите ESC для выхода")
#
#     text = "Текст для ввода на русском языке"  # Русский текст
#
#     while True:
#         if keyboard.is_pressed('up'):
#             x, y = pyautogui.position()
#             pyautogui.click(x, y)
#             time.sleep(0.1)
#
#             # Используем буфер обмена для русского текста
#             pyperclip.copy(text)
#             pyautogui.hotkey('ctrl', 'v')
#
#             print(f"Введен текст в координаты ({x}, {y})")
#             time.sleep(0.5)
#
#         elif keyboard.is_pressed('esc'):
#             break
#
#         time.sleep(0.01)
#
#
# # Универсальная функция для ввода русского текста
# def type_russian_text(text):
#     """
#     Функция для ввода русского текста через буфер обмена
#     """
#     pyperclip.copy(text)
#     pyautogui.hotkey('ctrl', 'v')
#     time.sleep(0.1)
#
#
# if __name__ == "__main__":
#     # Установите библиотеки:
#     # pip install pyautogui keyboard pyperclip
#
#     try:
#         import pyperclip
#     except ImportError:
#         print("Установите pyperclip: pip install pyperclip")
#         exit()
#
#     print("Выберите режим:")
#     print("1 - Простая версия (up + F3)")
#     print("2 - Расширенная версия (up-F5)")
#     print("3 - Максимально простая")
#
#     choice = input("Ваш выбор (1-3): ").strip()
#
#     if choice == "1":
#         get_mouse_position_with_hotkey()
#     elif choice == "2":
#         advanced_version()
#     elif choice == "3":
#         simple_click_type()
#     else:
#         print("Запускаю простую версию...")
#         time.sleep(2)
#         get_mouse_position_with_hotkey()
from zoneinfo import reset_tzpath

import keyboard
import pyautogui
import pyperclip
import time

print("Нажмите ESC для ввода координат и текста")
time.sleep(3)
while True:
    x,y = 949, 226
    pyautogui.click(x,y)
    time.sleep(0.5)
    if keyboard.is_pressed('esc'):
        break


# while True:
#     print(f'\r{pyautogui.position()}',end="",flush=True)
#     if keyboard.is_pressed('esc'):
#         # Небольшая задержка для стабилизации
#         time.sleep(0.3)
#
#         # Получаем координаты
#         coords_input = input("Введите координаты через пробел (x y): ")
#         coords = coords_input.split()
#
#         if len(coords) == 2:
#             try:
#                 x, y = int(coords[0]), int(coords[1])
#                 print(f"Клик по координатам: ({x}, {y})")
#                 pyautogui.click(x,y)
#
#                 # Для имитации клика можно использовать keyboard
#                 # Но лучше использовать pyautogui для клика
#                 text = "Hello"
#                 pyperclip.copy(text)
#                 pyautogui.hotkey('ctrl','v')
#                 print(f"Текст '{text}' скопирован в буфер")
#
#             except ValueError:
#                 print("Ошибка: введите числа для координат")
#         else:
#             print("Ошибка: введите две координаты через пробел")
#
#         # Задержка для предотвращения многократного срабатывания
#         time.sleep(1)
#
#     time.sleep(0.1)  # Важно: задержка для снижения нагрузки на CPU