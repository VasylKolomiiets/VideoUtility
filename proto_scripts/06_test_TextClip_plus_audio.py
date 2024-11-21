from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

def create_video_with_text(
        image_path, audio_path, 
        text, 
        q_threads=2,
        output_path="output_video.mp4",
        ):
    """
    Створює відеозаставку зображення, аудіо та тексту.

    Args:
    - image_path: Шлях до зображення.
    - audio_path: Шлях до аудіофайлу.
    - text: Текст, який потрібно додати до зображення.
    - output_path: Шлях для збереження вихідного відеофайлу.

    Returns:
    - Шлях до збереженого відеофайлу.
    """
    # Завантаження аудіо
    audio_clip = AudioFileClip(audio_path)
    
    # Завантаження зображення та створення відеокліпу з тривалістю аудіо
    image_clip = ImageClip(image_path, duration=audio_clip.duration)
    print(F"image_clip.size=")

    # Створення текстового кліпу
    text_clip = TextClip(
        text, fontsize=144, color='white',
        align='West',
        size=image_clip.size,
        ).set_duration(audio_clip.duration)
    
    # Розташування текстового кліпу на зображенні
    text_clip = text_clip.set_position((960, -160)).set_duration(audio_clip.duration)

    # Створення композитного відеокліпу
    video_clip = CompositeVideoClip([image_clip, text_clip])

    # Додавання аудіо до відеокліпу
    video_clip = video_clip.set_audio(audio_clip)

    # Збереження відеофайлу
    video_clip.write_videofile(
        output_path, 
        codec='libx264', audio_codec='aac',
        fps=24,
        threads=q_threads,
        )

    return output_path

# Приклад використання функції
output_video_path = create_video_with_text(
    R"C:\Users\Vasil\OneDrive\Projects\Python4U_if_UR\VideoUtility\data\pict\python1080_red_hat1920Done_blured.png", 
    R"C:\Users\Vasil\OneDrive\Projects\Python4U_if_UR\VideoUtility\data\sound\36161__sagetyrtle__bells2.wav", 
    "Це тестовий\nтекст ой, це\nтекстовий тест",
    q_threads=8,
    output_path="output_video.mp4",
    )

print(F"Відеофайл збережено як {output_video_path}")
