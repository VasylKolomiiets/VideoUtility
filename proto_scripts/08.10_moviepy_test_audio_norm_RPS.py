from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
import tempfile
import os

from knife_settings import measure_time


@measure_time
def normalize_audio(input_file, output_file, target_dBFS=-14.0):
    """
    Нормалізує аудіо трек у відеофайлі до заданого рівня dBFS.

    Args:
        input_file: Шлях до вхідного відеофайлу.
        output_file: Шлях до вихідного відеофайлу.
        target_dBFS: Бажаний рівень гучності в dBFS.
    """

    # Завантажуємо відео
    clip = VideoFileClip(input_file)

    # Створення тимчасового файлу для аудіо
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        # Зберігаємо аудіо у тимчасовий файл
        clip.audio.write_audiofile(temp_audio.name, codec='pcm_s16le')
        
        # Завантажуємо аудіо для обробки за допомогою pydub
        audio = AudioSegment.from_wav(temp_audio.name)

        # Нормалізуємо аудіо до заданого рівня dBFS
        change_in_dBFS = target_dBFS - audio.dBFS
        normalized_audio = audio.apply_gain(change_in_dBFS)

        # Створення тимчасового файлу для нормалізованого аудіо
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_normalized_audio:
            # Зберігаємо нормалізоване аудіо
            normalized_audio.export(temp_normalized_audio.name, format="wav")

            # Замінюємо аудіо у відео
            normalized_audio_clip = AudioFileClip(temp_normalized_audio.name)
            clip = clip.set_audio(normalized_audio_clip)
            clip.write_videofile(output_file, codec='libx264', audio_codec='aac')

        # Видалення тимчасового нормалізованого аудіо файлу
        os.remove(temp_normalized_audio.name)

    # Видалення тимчасового аудіо файлу
    os.remove(temp_audio.name)


if __name__ == "__main__":
    input_video_mp4 = R"C:\Users\Vasil\OneDrive\Projects\Python4U_if_UR\VideoUtility\data\video_in\2024-11-21 15.36.12 Vasyl Kolomiets's Zoom Meeting\video1136031557.mp4"
    norm_audio_mp4 = "normalized_audio_video_14.mp4"
    # Приклад використання:
    normalize_audio(input_video_mp4, norm_audio_mp4, target_dBFS=-14.0)
    print(F"Вихідний відеофайл з нормалізованим аудіо збережено як {norm_audio_mp4}")
