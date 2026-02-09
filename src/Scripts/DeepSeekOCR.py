from transformers import AutoModel, AutoTokenizer
import torch
from PIL import Image

# Загрузка модели без flash-attn
model_name = 'deepseek-ai/DeepSeek-OCR'
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name,
                                  trust_remote_code=True,
                                  use_safetensors=True,
                                  attn_implementation="eager")  # Явно отключаем flash attention
model = model.eval()

# Остальной код без изменений
def simple_ocr(image_path):
    image = Image.open(image_path).convert('RGB')
    prompt = "<image>\nРаспознайте текст на изображении."

    with torch.no_grad():
        result = model.infer(
            tokenizer,
            prompt=prompt,
            image_file=image_path,
            output_path=None,
            base_size=640,
            image_size=512,
            crop_mode=False
        )
    return result

# Использование
text = simple_ocr(r'C:\Users\Lev\PycharmProjects\AutoAnalyzer\data\input\OCR.png')
print(text)