from moviepy.editor import TextClip, CompositeVideoClip

def create_text_clip(output_path):
    """
    Створює відеокліп з текстом та зберігає його.

    :param output_path: Шлях до вихідного відео (mp4)
    """
    # Створення текстового кліпу
    text_clip = TextClip("Hello, MoviePy!", fontsize=70, color='white', size=(640, 480), bg_color='black')
    
    # Встановлення тривалості текстового кліпу
    text_clip = text_clip.set_duration(5)

    # Створення композитного відеокліпу
    video_clip = CompositeVideoClip([text_clip])

    # Збереження відео
    video_clip.write_videofile(output_path, codec='libx264', fps=24)
    print(f"Відео з текстом збережено як {output_path}")

# Приклад використання функції
create_text_clip("text_clip.mp4")
