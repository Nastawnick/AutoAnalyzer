"""import requests

from src.Data.Keys import QWEN_key as qwen_api_key
from src.Data.Keys import QWEN_key
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import base64

# Сервис автоматически скачает и настроит chromedriver
print(1)
service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--headless=new")
print(2)
driver = webdriver.Chrome(service=service, options=options)
print(3)
driver.get("https://static.dreamkas.ru/blog/cenniki/price-tag-mistake-3.jpg")
print(4)
driver.save_screenshot("my_screen1.png")
print(5)
driver.quit()
print(6)
def encode_to_base64(image_path):
    with open(image_path, 'rb') as image:
        file = image.read()
        encode_file = base64.b64encode(file)
        print(encode_file)
        result = encode_file.decode('utf-8')
        # print(f'{result}')
        return result
print(7)
image_to_send = encode_to_base64("my_screen1.png")

# def decode_from_base64(image_path, code):
#     image_data = base64.b64decode(code)
#     with open(image_path,'wb') as file:
#         file.write(image_data)
# print(8)
# decode_from_base64("decode_image1.png", encode_to_base64("my_screen1.png"))
print(9)
response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={'authorization':f'Bearer {QWEN_key}'},
    json = {
        'model':'qwen/qwen-2.5-vl-7b-instruct:free',
        'messages':[
             {
                'role':'user',
                'content':[
                    {'type':'text','text':'Что изображено на картинке?'},
                    {
                        'type':'image_url',
                        'image_url':{
                            'url':f"data:image/png;base64,{image_to_send}"
                        }
                    }

                ]
             },
            ]
         }
    )

a = response.json()
print(a.keys())
print(a['choices'])
print(a['choices'][0]['message']['content'])



class AiRequest:
    def __init__(self, ai_key):
        self.ai_key = ai_key
        self.ai_url = "https://openrouter.ai/api/v1/chat/completions"
        self.image_to_send = None
        self.model = 'qwen/qwen-2.5-vl-7b-instruct:free'
        self.text = 'Что изображено на картинке?'
        response = requests.post(
            url=self.ai_url,
            headers={'authorization': f'Bearer {self.ai_key}'},
            json={
                'model': self.model,
                'messages': [
                    {
                        'role': 'user',
                        'content': [
                            {'type': 'text', 'text': self.text},
                            {
                                'type': 'image_url',
                                'image_url': {
                                    'url': f"data:image/png;base64,{self.image_to_send}"
                                }
                            }

                        ]
                    },
                ]
            }
        )
"""
import requests
from fontTools.feaLib.ast import BaseAxis

from src.Data.Keys import QWEN_key as qwen_api_key
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import base64

# print(1)
# service = Service(ChromeDriverManager().install())
# options = Options()
# options.add_argument("--headless=new")
# print(2)
# driver = webdriver.Chrome(service=service, options=options)
# print(3)
# driver.get("https://static.dreamkas.ru/blog/cenniki/price-tag-mistake-3.jpg")
# print(4)
# driver.save_screenshot("my_screen1.png")
# print(5)
# driver.quit()
# print(6)

model_molmo = 'allenai/molmo-2-8b:free'
model_qwen = 'qwen/qwen-2.5-vl-7b-instruct:free'

def encode_to_base64(image_path):
    with open(image_path, 'rb') as image:
        file = image.read()
        encode_file = base64.b64encode(file)
        result = encode_file.decode('utf-8')
        return result
# print(7)
image_to_send = encode_to_base64("my_screen1.png")
# print(8)
class RequestConfig:
    def __init__(self, api_key, base_url, model):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

class MessageBuilder:
    @staticmethod
    def create_text_content(text):
        return {'type':'text', 'text':text}

    @staticmethod
    def create_image_content(image_url):
        return {'type':'image_url','image_url':{'url': f"data:image/png;base64,{image_url}"}}

    def build_message(self, text, image_base64=None):
        content = [self.create_text_content(text)]
        if image_base64:
            content.append(self.create_image_content(image_base64))

        # print(f'content: {content}')
        return [
            {
                'role': 'user',
                'content': content
            }
        ]

class HttpClient:
    def __init__(self, config: RequestConfig):
        self.config = config

    def post(self, data):
        print("post is started")
        response = requests.post(
            url = self.config.base_url,
            headers = {'Authorization': f'Bearer {self.config.api_key}'},
            json = {
                'model':self.config.model,
                'messages':data
            } #не хватает 'model': self.model, 'messages': [...
        )
        print("post is finished")
        return response

class Parser:
    def __init__(self):
        self.result = None

    def parsed_data(self, response):
        # print(f'parsed_data before: {self.result}')
        self.result = response.json()
        # print(f'parsed_data after: {self.result}')
        return self

    def extract_text(self):
        print(f'extract_text: {self.result}')
        self.result = self.result['choices'][0]['message']['content']
        return self

    def get_result(self):
        return self.result

class ConnectionManager:
    def __init__(self, config: RequestConfig, http_client: HttpClient):
        self.config = config
        self.http_client = http_client
        self.message_builder = MessageBuilder()
        self.parser = Parser()

    def image_analysis(self, image_base64, text = 'Что изображено на этой картинке?'):
        message_image = self.message_builder.build_message(text, image_base64)
        # print("message is ready")
        response = self.http_client.post(message_image)
        # print("response: ",response)
        parsed_data = self.parser.parsed_data(response).extract_text().get_result()
        # print("Ответ: ",parsed_data)

class BaseAi:
    def __init__(self):
        self.config = RequestConfig(api_key = qwen_api_key, base_url = "https://openrouter.ai/api/v1/chat/completions", model = model_molmo)
        self.http_client = HttpClient(config=self.config)
        self.connection = ConnectionManager(config=self.config, http_client=self.http_client)

    def set_image(self,image):
        print('Анализ изображения')
        self.connection.image_analysis(image)

if __name__ == '__main__':
    print('Начало выполнения')
    # config = RequestConfig(api_key = qwen_api_key, base_url = "https://openrouter.ai/api/v1/chat/completions", model = model_molmo)
    # print(1)
    # http_client = HttpClient(config=config)
    # print(2)
    # connection = ConnectionManager(config=config, http_client=http_client)
    # print(3)
    # connection.image_analysis(image_to_send)
    # print('Конец выполнения')
    image = encode_to_base64("network_images/network_img_1.jpg")
    connect = BaseAi()
    connect.set_image(image=image)
    print('Конец выполнения')