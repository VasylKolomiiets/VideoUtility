from moviepy.editor import VideoClip, TextClip, CompositeVideoClip, ColorClip
from moviepy.video.fx.fadein import fadein 
from moviepy.video.fx.fadeout import fadeout


def create_angled_text_animation(text, font='Arial', fontsize=50, start_color='#FF0000', end_color='#00FF00', duration=3, background_color='black'):
    """
    Створює відео з анімованим текстом, який з'являється з-за кута і змінює колір.

    Args:
        text: Текст для відображення.
        font: Шрифт.
        fontsize: Розмір шрифту.
        start_color: Початковий колір тексту в форматі HEX (наприклад, '#FF0000').
        end_color: Кінцевий колір тексту в форматі HEX (наприклад, '#00FF00').
        duration: Тривалість анімації.
        background_color: Колір фону.
    """
    # Роздільна здатність екрану
    screen_width, screen_height = 1920, 1080

    # Створення фонового кліпу
    bg_clip = ColorClip(size=(screen_width, screen_height), color=background_color).set_duration(duration)

    # Функція для обчислення проміжного кольору
    def interpolate_color(start_color, end_color, factor):
        r = int(int(start_color[1:3], 16) + factor * (int(end_color[1:3], 16) - int(start_color[1:3], 16)))
        g = int(int(start_color[3:5], 16) + factor * (int(end_color[3:5], 16) - int(start_color[3:5], 16)))
        b = int(int(start_color[5:7], 16) + factor * (int(end_color[5:7], 16) - int(start_color[5:7], 16)))
        return f'#{r:02x}{g:02x}{b:02x}'

    # Функція для створення текстового кліпу для певного кадру
    def make_text_frame(t):
        factor = t / duration
        color = interpolate_color(start_color, end_color, factor)
        x_pos = int(screen_width * factor) - screen_width // 2
        txt_clip = TextClip(text, 
                            fontsize=fontsize, font=font, 
                            color=color, bg_color=background_color,
                            size=(screen_width, screen_height),
                            )
        txt_clip = txt_clip.set_position((x_pos, 'center'))
        return txt_clip.get_frame(t)

    # Створення відео з анімованим текстом
    video = VideoClip(make_text_frame, duration=duration)
    
    # Накладання текстового кліпу на фон
    final_clip = CompositeVideoClip([bg_clip, video])

    # Додавання ефектів зникнення/з'явлення
    final_clip = fadein(final_clip, 1)
    final_clip = fadeout(final_clip, 1)

    # Збереження відео
    final_clip.write_videofile("output.mp4", fps=24, codec='libx264')

# Приклад використання:
create_angled_text_animation("Вітаємо!", font="Times New Roman", fontsize=72, start_color='#FF0000', end_color='#00FF00', duration=5, background_color="black")
