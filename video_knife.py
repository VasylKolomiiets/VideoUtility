from pathlib import Path
import os
import time
from typing import Iterable

import pandas as pd

from PIL import Image
import numpy as np

from pydub import AudioSegment
import tempfile

from moviepy.editor import (
    ImageClip, TextClip,
    AudioFileClip,
    CompositeVideoClip, VideoFileClip, VideoClip,
    concatenate_videoclips,
)

# Ensure comments in functions follow a consistent style


from knife_settings import measure_time


# ##### `01_clip_cut_test_moviepy.py` #####

# video_file_name = R".\data\video_out\23\video1457514656.mp4"
# clip_file_xl = R"C:\Users\Vasil\OneDrive\Projects\Python4U_if_UR\VideoUtility\data\xlsx\Lesson_23.xlsx"

@measure_time
def split_video(
    video_file_path: Path,
    clip_file_xl: Path,
    work_folder: Path,
    skip_names: Iterable[str] = ("шмяка", "skip_it"),
) -> list[Path]:
    """
    Функція для нарізки відео на частини за вказаними часовими мітками.

    Args:
        video_file_path (Path): Шлях до відеофайлу.
        clip_file_xl (Path): Шлях до Excel-файлу з часовими мітками.
        work_folder (Path): Шлях до робочої папки для збереження вихідних файлів.
        skip_names: Список назв частин, які потрібно пропустити.
    """
    resulted_clips = []
    # Зчитування даних з Excel
    df = pd.read_excel(clip_file_xl)

    with VideoFileClip(str(video_file_path)) as clip:
        # Перевірка наявності відеофайлу
        if not clip:
            raise FileNotFoundError(
                F"Відеофайл {video_file_path} не знайдено.")
        print(f"{clip.size=}, {clip.fps=}, {clip.duration=}")

        start_time = "0:00:00.0"
        for index, row in df.iterrows():
            part_title = row["part_title"]
            end_time = row["end_time"]
            print(f"{end_time=} is {type(end_time)} type.")
            output_file = work_folder / F"{video_file_path.stem}_{index}.mp4"

            if part_title not in skip_names:
                print(
                    f"Processed clip: {part_title} from {start_time} to {end_time}")
                # Обрізка відео
                subclip = clip.subclip(start_time, end_time)
                # Збереження обрізаного відео
                subclip.write_videofile(str(output_file), codec="libx264", audio_codec="aac")

                resulted_clips.append(
                    dict(
                        prefix_text=row.part_title,
                        output_file=output_file,
                    )
                )
                print(F"{output_file} записано.")
            start_time = end_time
        print("Відео нарізано!")
    return resulted_clips


def break_str(row, n, tail=0.7):
    """
    Splits a string into multiple lines of a specified maximum length.

    Args:
        row (str): The input string to be split.
        n (int): The maximum length of each line.
        tail (float): A factor to determine where to break the line,
                      prioritizing spaces near the end of the line.

    Returns:
        str: The input string split into multiple lines.
    """
    if len(row) <= n or n < 2:
        return row
    else:
        i_tail = int(tail * n) - 1
        blank_index = row.find(" ", i_tail, n + 1)
        if blank_index > 0:
            return row[:blank_index] + "\n" + break_str(row[blank_index + 1:], n, tail)
        return row[:n] + "\n" + break_str(row[n:], n, tail)


##### `08.10_moviepy_test_audio_norm_RPS.py` #####
@measure_time
def normalize_audio(input_file: str, output_file: str, target_dBFS=-14.0):
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
        clip.audio.write_audiofile(temp_audio.name, codec="pcm_s16le")
        audio = AudioSegment.from_wav(temp_audio.name)

    # Нормалізуємо аудіо до заданого рівня dBFS
    change_in_dBFS = target_dBFS - audio.dBFS
    normalized_audio = audio.apply_gain(change_in_dBFS)

    # Створення тимчасового файлу для нормалізованого аудіо
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_normalized_audio:
        normalized_audio.export(temp_normalized_audio.name, format="wav")
        normalized_audio_clip = AudioFileClip(temp_normalized_audio.name)
        clip = clip.set_audio(normalized_audio_clip)
        clip.write_videofile(output_file, codec="libx264", audio_codec="aac")

    # Видалення тимчасових файлів
    os.remove(temp_audio.name)
    os.remove(temp_normalized_audio.name)


##### `06_test_TextClip_plus_audio.py` #####
@measure_time
def create_video_with_text(
    image_path,
    audio_path,
    text,
    num_threads=None,
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
    print(f"{image_clip.size=}")

    # Створення текстового кліпу
    text_clip = TextClip(
        text,
        fontsize=120,
        color="white",
        align="west",
        size=image_clip.size,
    ).set_duration(audio_clip.duration)

    # Розташування текстового кліпу на зображенні
    text_clip = text_clip.set_position(
        (1000, 0)).set_duration(audio_clip.duration)

    # Створення композитного відеокліпу
    video_clip = CompositeVideoClip([image_clip, text_clip])

    # Додавання аудіо до відеокліпу
    video_clip = video_clip.set_audio(audio_clip)

    # Збереження відеофайлу
    if num_threads is None:
        # Визначаємо кількість потоків автоматично
        num_threads = max(1, (os.cpu_count() or 1) - 2)
        print("Auto picked ", end="")
    print(F"{num_threads=}")

    video_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=24,
        threads=num_threads,
    )

    return output_path

##### `07_concatenate_clips.py` #####


@measure_time
def concatenate_clips(
        clips: Iterable[str],
        output_path: str = "concatenated_video.mp4"
) -> str:
    """
    Склеює відеокліпи з ітерабельного об'єкта шляхів до файлів та зберігає їх у вихідний відеофайл.
    Args:
      - clips: Iterable object (e.g., list or tuple) of paths to video files (mp4)
      - output_path: Path to the output video file (mp4)

    Returns:
      - Path to the saved video file
    """
    # Завантаження відеокліпів
    video_clips = [VideoFileClip(clip) for clip in clips]

    # Склеювання відеокліпів
    final_clip = concatenate_videoclips(video_clips)

    # Збереження вихідного відеофайлу
    final_clip.write_videofile(
        output_path, codec="libx264", audio_codec="aac", fps=24
    )  # , threads=8
    return output_path


def corner_morfing(
    input_video,
    image1_path,
    image2_path,
    output_video,
    duration_static=60,
    duration_morph=20,
    overlay_size=150,
):
    """
    Накладає анімоване морфоване зображення у правому нижньому куті відео.
    """

    def morph_images(img1, img2, factor):
        """
        Плавно змішує два зображення (PIL.Image) на основі фактору (0...1).
        """
        morphed_image = Image.blend(img1, img2, factor)
        return np.array(morphed_image)

    def precompute_transition_frames(img1, img2, duration_morph, fps):
        """
        Генерує список проміжних кадрів для морфінгу між img1 та img2.

        Args:
            img1, img2 (PIL.Image): Зображення повинні мати однакові розміри та формат RGBA.
            duration_morph (float): Тривалість переходу в секундах.
            fps (float): Кількість кадрів за секунду.

        Returns:
            forward_frames (list[np.array]): Список кадрів для переходу від img1 до img2.
            reverse_frames (list[np.array]): Список кадрів для переходу від img2 до img1.
        """
        num_frames = int(duration_morph * fps)
        forward_frames = []
        for i in range(num_frames):
            # Розраховуємо фактор інтерполяції від 0 до 1
            factor = i / (num_frames - 1) if num_frames > 1 else 0
            frame = Image.blend(img1, img2, factor)
            forward_frames.append(np.array(frame))
        # Для зворотного переходу можна просто використати перевернутий список
        reverse_frames = list(reversed(forward_frames))
        return forward_frames, reverse_frames

    def corner_morph_overlay(
        video_path,
        image1_path,
        image2_path,
        duration_static=60,
        duration_morph=20,
        overlay_size=150,
    ):
        """
        Накладає анімоване морфоване зображення у правому нижньому куті відео.

        Args:
            video_path (str): Шлях до відеофайлу.
            image1_path (str): Шлях до першого PNG-зображення.
            image2_path (str): Шлях до другого PNG-зображення (однакового розміру).
            duration_static (int): Час показу статичного зображення.
            duration_morph (int): Час переходу між зображеннями.
            overlay_size (int): Бажана ширина накладного зображення (зберігаючи пропорції; за замовчуванням 150 пікселів).

        Returns:
            CompositeVideoClip: Комбінований відеокліп з накладеним морфованим зображенням.
        """

        # Функція для створення кадрів накладеного зображення
        def make_frame(t):
            """
            Генерує кадр накладеного зображення відповідно до поточного часу t.
            """
            t_in_cycle = t % total_cycle_duration
            if 0 <= t_in_cycle < duration_static:
                # Статичне показ першого зображення
                # Беремо лише перші 3 канали (RGB)
                return np.array(img1_resized)[:, :, :3]
            elif duration_static <= t_in_cycle < duration_static + duration_morph:
                # Перехід від першого до другого з використанням кешованих кадрів
                rel_time = t_in_cycle - duration_static
                idx = int(rel_time / duration_morph *
                          (len(forward_frames) - 1))
                # Беремо лише перші 3 канали (RGB)
                return forward_frames[idx][:, :, :3]
            elif (
                duration_static + duration_morph
                <= t_in_cycle
                < 2 * duration_static + duration_morph
            ):
                # Статичне показ другого зображення
                # Беремо лише перші 3 канали (RGB)
                return np.array(img2_resized)[:, :, :3]
            elif 2 * duration_static + duration_morph <= t_in_cycle < total_cycle_duration:
                # Перехід від другого до першого з використанням кешованих кадрів
                rel_time = t_in_cycle - (2 * duration_static + duration_morph)
                idx = int(rel_time / duration_morph *
                          (len(reverse_frames) - 1))
                # Беремо лише перші 3 канали (RGB)
                return reverse_frames[idx][:, :, :3]
            else:
                return np.zeros(
                    (new_height, overlay_size, 3), dtype=np.uint8
                )  # Змінено на 3 канали
                # Повертаємо чорний кадр, якщо час не відповідає жодному з випадків

        try:
            # Завантаження відео та отримання fps
            video_clip = VideoFileClip(video_path)
            fps = video_clip.fps

            # Завантаження зображень і конвертація у формат RGBA
            img1_full = Image.open(image1_path).convert("RGBA")
            img2_full = Image.open(image2_path).convert("RGBA")

            if img1_full.size != img2_full.size:
                raise ValueError("Зображення мають різні розміри.")

            orig_width, orig_height = img1_full.size
            # Підтримуємо пропорції при зміні ширини до overlay_size
            new_height = int(orig_height * overlay_size / orig_width)

            # Масштабування зображень до розмірів (overlay_size x new_height)
            img1_resized = img1_full.resize(
                (overlay_size, new_height), Image.Resampling.LANCZOS
            )
            img2_resized = img2_full.resize(
                (overlay_size, new_height), Image.Resampling.LANCZOS
            )

            # Попереднє обчислення кадрів для переходів
            forward_frames, reverse_frames = precompute_transition_frames(
                img1_resized, img2_resized, duration_morph, fps
            )

            # Повна тривалість одного циклу анімації
            total_cycle_duration = 2 * (duration_static + duration_morph)

            # Створення відеокліпу для накладання анімації
            overlay_clip = VideoClip(make_frame, duration=video_clip.duration)
            overlay_clip = overlay_clip.set_position(("right", "bottom"))

            final_clip = CompositeVideoClip([video_clip, overlay_clip])
            final_clip.fps = video_clip.fps

            return final_clip

        except Exception as e:
            print(F"Виникла помилка: {e}")
            return None

    final_video_clip = corner_morph_overlay(
        input_video,
        image1_path,
        image2_path,
        duration_static=60,
        duration_morph=20,
        overlay_size=150,
    )

    if final_video_clip:
        # final_video_clip.write_videofile(
        #     output_video,
        #     codec="h264_nvenc",  # codec="h264_nvenc",  codec="libx264",
        #     audio_codec="aac",
        #     fps=final_video_clip.fps,
        # )

        final_video_clip.write_videofile(
            output_video,
            codec="h264_nvenc",  # Використовуємо апаратний енкодер NVIDIA
            audio_codec="aac",
            fps=final_video_clip.fps,
            ffmpeg_params=[
                # # Вибір пресету "slow" змушує енкодер виконувати більше роботи –
                # # це дозволяє досягнути кращої якості та стиснення, що рівноцінно сильнішому завантаженню GPU.
                # "-preset", "slow",
                # # Режим керування бітрейтом: VBR (variable bitrate)
                # # в комбінації з параметром якості (-cq) дає баланс між якістю та розміром файлу.
                # "-rc", "vbr",
                # "-cq", "19",  # Значення 19 (чим менше – тим вища якість, але трохи більший розмір).
                # # Встановлюємо стандарт сумісності H.264.
                # "-level", "4.1",
                # Оптимізація завантаження GPU: Lookahead аналізує наперед кількість кадрів для розподілу бітрейту
                "-rc-lookahead",
                "64",
                # Налаштування кількості поверхонь для обробки кадрів у пам’яті GPU
                "-surfaces",
                "64",
                "-pix_fmt",
                "yuv420p",
            ],
        )

        final_video_clip.close()
        print(F"Відео з накладеним морфінгом створено та збережено у {output_video}")


# Приклад використання функції
if __name__ == "__main__":
    # Вимірюємо час виконання
    time_0 = time.time()
    q_threads = 5
    # Вказуємо шляхи до зображення та аудіо
    image_path = R"C:\Users\Vasil\OneDrive\Projects\Python4U_if_UR\VideoUtility\data\pict\python1080_red_hat1920Done_blured.png"
    audio_path = R"C:\Users\Vasil\OneDrive\Projects\Python4U_if_UR\VideoUtility\data\sound\36161__sagetyrtle__bells2.wav"

    # Текст для відеозаставки
    text = "Серія 28.\nМуки творчості\nіз GitHub Copilot"

    # Створюємо відеозаставку
    output_path = create_video_with_text(
        image_path,
        audio_path,
        text,
        output_path=R".\data\video_out\28\output_prefix_video_28.mp4",
        num_threads=q_threads,
    )

    # Виводимо час виконання
    print(
        F"Час виконання при {q_threads=} у секундах:  {(time.time() - time_0):5.2f}")
    print(F"Відеофайл збережено як {output_path}")


# if __name__ == "__main__":
#     video_folder = Path(
#         R"C:\Users\Vasil\OneDrive\Projects\Python4U_if_UR\VideoUtility\data"
#     )

#     input_video_mp4 = video_folder / "video_in" / "2025-04-05 09.10.40 Vasyl Kolomiets's Zoom Meeting" / "video1617769953.mp4"
#     norm_audio_mp4 = video_folder / "video_out" / "28" / "normalized_audio_video_28.mp4"

#     # Приклад використання:
#     normalize_audio(
#         str(input_video_mp4.resolve()),
#         str(norm_audio_mp4.resolve()),
#     )

#     print(f"Вихідний відеофайл з нормалізованим аудіо збережено як {norm_audio_mp4}")

# Приклад використання функції
if __name__ == "__main__":
    clips_tuple = (
        R".\data\video_out\28\output_prefix_video_28.mp4",
        R".\data\video_out\28\normalized_audio_video_28.mp4",
    )
    output_video_path = concatenate_clips(
        clips_tuple,
        R".\data\video_out\28\Серія 28. Муки творчості із GitHub Copilot.mp4",
    )
    print(F"Склеєний відеофайл збережено як {output_video_path}")
