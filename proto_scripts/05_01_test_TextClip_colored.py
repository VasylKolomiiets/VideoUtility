import numpy as np
from moviepy.editor import VideoClip, TextClip, CompositeVideoClip, ColorClip
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout

def create_angled_text_animation(text, font='Arial', fontsize=50, 
                                 start_color='#FF0000', end_color='#00FF00', 
                                 duration=3, background_color='black',
                                 angle=45):
    """
    Створює відео з анімованим текстом, що рухається під заданим кутом і змінює колір.

    Аргументи:
        text: Текст для відображення.
        font: Шрифт.
        fontsize: Розмір шрифту.
        start_color: Початковий колір тексту в HEX форматі.
        end_color: Кінцевий колір тексту в HEX форматі.
        duration: Тривалість анімації в секундах.
        background_color: Колір фону.
        angle: Кут руху тексту в градусах.
    """

    # Розмір відео
    width, height = 1920, 1080

    # Створення фону
    background = ColorClip(size=(width, height), color=background_color).set_duration(duration)

    # Функція для обчислення проміжного кольору
    def interpolate_color(start_color, end_color, factor):
        start_color = np.array([int(start_color[i:i+2], 16) for i in (1, 3, 5)])
        end_color = np.array([int(end_color[i:i+2], 16) for i in (1, 3, 5)])
        return '#{:02x}{:02x}{:02x}'.format(*(int(c) for c in (start_color + factor * (end_color - start_color))))

    # Функція для створення кадру з текстом
    def make_frame(t):
        factor = t / duration
        color = interpolate_color(start_color, end_color, factor)

        # Розрахунок координат тексту
        x = int(width * factor * np.cos(np.radians(angle))) - width // 2
        y = int(height * factor * np.sin(np.radians(angle))) + height // 2

        text_clip = TextClip(text, font=font, fontsize=fontsize, color=color,
                            bg_color=background_color, size=(width, height))
        text_clip = text_clip.set_position((x, y))
        return text_clip.get_frame(t)

    # Створення відеокліпу
    video = VideoClip(make_frame, duration=duration)

    # Комбінування фону та тексту
    final_clip = CompositeVideoClip([background, video])

    # Додавання ефектів плавного з'явлення та зникнення
    final_clip = fadein(final_clip, 1)
    final_clip = fadeout(final_clip, 1)

    # Збереження відео
    final_clip.write_videofile("output.mp4", fps=24, codec='libx264')

# Приклад використання
create_angled_text_animation("Hello, world!", fontsize=72, angle=30, duration=5)