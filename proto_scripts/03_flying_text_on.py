from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout

def create_angled_text_animation(text, font='Arial', fontsize=50, start_color=(255, 0, 0), end_color=(0, 255, 0), duration=3, background_color='black'):
    """
    Створює відео з анімованим текстом, який з'являється з-за кута і змінює колір.

    Args:
        text: Текст для відображення.
        font: Шрифт.
        fontsize: Розмір шрифту.
        start_color: Початковий колір тексту в форматі RGB (R, G, B).
        end_color: Кінцевий колір тексту в форматі RGB (R, G, B).
        duration: Тривалість анімації.
        background_color: Колір фону.
    """

    # Створення фону
    clip = VideoFileClip("animated_text_clip.mp4")  # Замініть на ваш файл фону
    clip = clip.set_duration(duration)

    # Створення текстового кліпу
    txt_clip = TextClip(text, fontsize=fontsize, color=start_color, font=font)
    txt_clip = txt_clip.set_position(('left', 'center')).set_duration(duration)

    # Анімація руху та кольору
    txt_clips = []
    for i in range(duration * 24):  # 24 кадри в секунду
        x_pos = i / (duration * 24) * clip.w
        txt_clip_copy = txt_clip.set_position((x_pos, 'center'))
        txt_clip_copy = txt_clip_copy.set_opacity(i / (duration * 24))
        r, g, b = (
            int(start_color[0] + i / (duration * 24) * (end_color[0] - start_color[0])),
            int(start_color[1] + i / (duration * 24) * (end_color[1] - start_color[1])),
            int(start_color[2] + i / (duration * 24) * (end_color[2] - start_color[2]))
        )
        txt_clip_copy = txt_clip_copy.set_color(color=(r, g, b))
        txt_clips.append(txt_clip_copy)

    # Композиція
    video = CompositeVideoClip(txt_clips, size=clip.size)
    video = CompositeVideoClip([clip, video])

    # Додавання ефектів зникнення/з'явлення
    video = fadein(video, 1)
    video = fadeout(video, 1)

    # Збереження відео
    video.write_videofile("output.mp4", audio_codec='aac')

# Приклад використання:
create_angled_text_animation("Вітаємо!", font="Times New Roman", fontsize=72, start_color=(255, 0, 0), end_color=(0, 255, 0), duration=5, background_color="black")