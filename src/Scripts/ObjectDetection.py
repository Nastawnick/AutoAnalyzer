from ultralytics import YOLO
from pathlib import Path

# model = YOLO('yolov8m.pt')
#
# current_file = Path(__file__)
# # path = current_file.parent.parent.parent /'data'/'input'/'Animal_1.jpg'
# #
# # results = model.predict(path)
# # result = results[0]
# #
# # print(result.boxes)
#
#
# data_path = current_file.parent.parent.parent /'data'/'input'/'price-tag-audit.v2-complete-dataset.yolov8'/'data.yaml'
# model.train(data = data_path, epochs = 20)

# from ultralytics import YOLO
# from pathlib import Path
# import cv2
#
# # Загружаем вашу обученную модель (автоматически загружается лучшая веса)
# model = YOLO(r'C:\Users\Lev\PycharmProjects\AutoAnalyzer\runs\detect\train4\weights\best.pt')  # путь к обученной модели
#
# # Альтернативно, если вы знаете точный путь:
# # model = YOLO('path/to/your/trained/model/weights/best.pt')
#
# # Путь к тестовому изображению
# current_file = Path(__file__)
# test_image_path = current_file.parent.parent.parent / 'data' / 'input' / 'tag7.png'
#
# # Распознавание на изображении
# results = model.predict(test_image_path, save=True, conf=0.25)  # conf - порог уверенности
# if results and hasattr(results[0], 'names'):
#     class_names = results[0].names
#     print("Список доступных классов:")
#     for class_id, class_name in class_names.items():
#         print(f"  {class_id}: {class_name}")
# else:
#     # Альтернативный способ, если первый не сработал
#     model = YOLO(r'C:\Users\Lev\PycharmProjects\AutoAnalyzer\runs\detect\train4\weights\best.pt')
#     if hasattr(model, 'names'):
#         print("Список доступных классов:")
#         for class_id, class_name in model.names.items():
#             print(f"  {class_id}: {class_name}")
#     else:
#         print("Не удалось получить список классов.")
#
# print(results)

#
# print()
#
# from ultralytics import YOLO
# from pathlib import Path
# import cv2
#
# # Загружаем вашу обученную модель
# model = YOLO(r'C:\Users\Lev\PycharmProjects\AutoAnalyzer\runs\detect\train4\weights\best.pt')
#
# # Путь к тестовому изображению
# current_file = Path(__file__)
# test_image_path = current_file.parent.parent.parent / 'data' / 'input' / 'tag7.png'
#
# # Загружаем исходное изображение
# original_image = cv2.imread(str(test_image_path))
#
# # Распознавание на изображении
# results = model.predict(test_image_path, conf=0.25)
#
# print(results[0].names)
# # Класс, который нас интересует (замените на нужный ID класса)
# target_class_id = 3  # Например, класс с ID 0
#
# # Обрабатываем результаты для первого изображения (results[0])
# for result in results:
#     # Проверяем, есть ли обнаруженные объекты
#     if result.boxes is not None and len(result.boxes) > 0:
#         for i, box in enumerate(result.boxes):
#             # Получаем ID класса и уверенность
#             class_id = int(box.cls.item())
#             confidence = box.conf.item()
#
#             # Если это нужный нам класс
#             if class_id == target_class_id:
#                 # Получаем координаты bounding box в формате xyxy
#                 x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
#
#                 # Обрезаем изображение
#                 cropped_image = original_image[y1:y2, x1:x2]
#
#                 # Выводим информацию
#                 class_name = result.names[class_id]
#                 print(f"Обнаружен {class_name} с уверенностью {confidence:.2f}")
#
#                 # Показываем обрезанное изображение
#                 cv2.imshow(f'Cropped {class_name} {i}', cropped_image)
#
#         # Ждем нажатия клавиши для закрытия окон
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
#     else:
#         print("На изображении не обнаружено объектов")



# # Простой пример с использованием Pillow (PIL)
# current_file = Path(__file__)
#
# import cv2
# import pytesseract
#
#
# def preprocess_image(image_path):
#     """Функция для предварительной обработки изображения"""
#     # Загружаем изображение
#     img = cv2.imread(str(image_path))
#     # Конвертируем в оттенки серого
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # Применяем пороговую обработку для создания черно-белого изображения
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
#
#     return thresh
#
#
# # Обрабатываем изображение
# processed_image = preprocess_image(current_file.parent.parent.parent / 'data' / 'input' / 'Price_tag2.png')
#
# # Распознаем текст с обработанного изображения
# text = pytesseract.image_to_string(processed_image, lang = 'rus')
# print(text)
def training():
    model = YOLO('yolov8m.pt')

    current_path = Path(__file__)

    data_path = current_path.parent.parent.parent /'data'/'input'/'price.v1i.yolov8'/'data.yaml'

    model.train(data = data_path , epochs = 20)


def predict():
    from ultralytics import YOLO
    from pathlib import Path

    # Загружаем вашу обученную модель (автоматически загружается лучшая веса)
    model = YOLO(r'C:\Users\Lev\PycharmProjects\AutoAnalyzer\runs\detect\train5\weights\best.pt')  # путь к обученной модели

    current_file = Path(__file__)
    test_image_path = current_file.parent.parent.parent / 'data' / 'input' / 'tag9.png'

    # Распознавание на изображении
    results = model.predict(test_image_path, save=True, conf=0.25)  # conf - порог уверенности
if __name__ == '__main__':
    predict()