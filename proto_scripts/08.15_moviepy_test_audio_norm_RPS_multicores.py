from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
import concurrent.futures
import tempfile
import os

from knife_settings import measure_time


def process_audio_chunk(args):
    """
    Нормалізує один аудіо чанк до заданого рівня dBFS.
    """
    audio_chunk, target_dBFS = args
    change_in_dBFS = target_dBFS - audio_chunk.dBFS
    return audio_chunk.apply_gain(change_in_dBFS)


@measure_time
def normalize_audio(input_file, output_file, target_dBFS=-14.0, chunk_size_ms=5000, max_workers=4):
    """
    Нормалізує аудіо трек у відеофайлі до заданого рівня dBFS з використанням багатоядерної обробки.

    Args:
        input_file: Шлях до вхідного відеофайлу.
        output_file: Шлях до вихідного відеофайлу.
        target_dBFS: Бажаний рівень гучності в dBFS.
        chunk_size_ms: Розмір чанку в мілісекундах.
        max_workers: Максимальна кількість потоків для обробки.
    """

    # Завантажуємо відео
    clip = VideoFileClip(input_file)

    # Створення тимчасового файлу для аудіо
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        # Зберігаємо аудіо у тимчасовий файл
        clip.audio.write_audiofile(temp_audio.name, codec='pcm_s16le')
        
        # Завантажуємо аудіо для обробки за допомогою pydub
        audio = AudioSegment.from_wav(temp_audio.name)

        # Розбиваємо аудіо на чанки для паралельної обробки
        audio_chunks = [(audio[i:i + chunk_size_ms], target_dBFS) for i in range(0, len(audio), chunk_size_ms)]

        # Паралельна обробка аудіо чанків
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            normalized_chunks = list(executor.map(process_audio_chunk, audio_chunks))

        # Об'єднуємо нормалізовані чанки
        normalized_audio = sum(normalized_chunks)

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
    input_video_mp4 = R"C:\Users\Vasil\OneDrive\Документи\Zoom\2024-11-18 15.55.31 Vasyl Kolomiets's Zoom Meeting\video3305318331.mp4"
    norm_audio_mp4 = "normalized_audio_video_12.mp4"
    # Приклад використання функції:
    normalize_audio(input_video_mp4, norm_audio_mp4, target_dBFS=-14.0, chunk_size_ms=5000, max_workers=5)
    print(f"Вихідний відеофайл з нормалізованим аудіо збережено як {norm_audio_mp4}")
