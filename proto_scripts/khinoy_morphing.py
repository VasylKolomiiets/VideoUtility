import requests
from PIL import Image, ImageSequence
import numpy as np
import io

# Загрузка изображений
def load_image_from_url(url):
    response = requests.get(url)
    return Image.open(io.BytesIO(response.content))

# URL изображений
bw_url = "https://page1.genspark.site/v1/base64_upload/0cd27251608576d4edad163dfea49b96"
color_url = "https://page1.genspark.site/v1/base64_upload/885bf3226ed22b19323e9c7f6cf5ecd2"

# Загружаем изображения
bw_img = load_image_from_url(bw_url)
color_img = load_image_from_url(color_url)

# Приводим к одинаковому размеру
target_size = bw_img.size
color_img = color_img.resize(target_size, Image.Resampling.LANCZOS)

# Конвертируем в RGB если нужно
if bw_img.mode != 'RGB':
    bw_img = bw_img.convert('RGB')
if color_img.mode != 'RGB':
    color_img = color_img.convert('RGB')

# Создаем кадры перехода
frames = []
num_transition_frames = 90

# Кадры перехода (18 секунд)
for i in range(num_transition_frames + 1):
    alpha = i / num_transition_frames
    # Линейная интерполяция между изображениями
    blended = Image.blend(bw_img, color_img, alpha)
    frames.append(blended)

# Параметры для GIF
transition_duration = 200  # мс на кадр перехода
final_duration = 7000      # мс для финального кадра

# Создаем список длительностей
durations = [transition_duration] * (num_transition_frames + 1)
durations[-1] = final_duration  # последний кадр держится 7 секунд

# Сохраняем GIF
frames[0].save(
    'pomegranate_transition.gif',
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0  # без повторов
)

print("GIF создан успешно: pomegranate_transition.gif")
print(f"Общее количество кадров: {len(frames)}")
print(f"Длительность перехода: {(num_transition_frames * transition_duration) / 1000} секунд")
print(f"Длительность финального кадра: {final_duration / 1000} секунд")
print(f"Общая длительность: {((num_transition_frames * transition_duration) + final_duration) / 1000} секунд")