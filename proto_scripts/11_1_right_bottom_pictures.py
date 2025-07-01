from moviepy.editor import VideoFileClip, CompositeVideoClip, VideoClip
import numpy as np
from PIL import Image


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
            idx = int(rel_time / duration_morph * (len(forward_frames) - 1))
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
        elif (
            2 * duration_static + duration_morph
            <= t_in_cycle
            < total_cycle_duration
        ):
            # Перехід від другого до першого з використанням кешованих кадрів
            rel_time = t_in_cycle - (2 * duration_static + duration_morph)
            idx = int(rel_time / duration_morph * (len(reverse_frames) - 1))
            # Беремо лише перші 3 канали (RGB)
            return reverse_frames[idx][:, :, :3]
        else:
            # Змінено на 3 канали
            return np.zeros((new_height, overlay_size, 3), dtype=np.uint8)
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
            (overlay_size, new_height), Image.Resampling.LANCZOS)
        img2_resized = img2_full.resize(
            (overlay_size, new_height), Image.Resampling.LANCZOS)

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
        print(f"Виникла помилка: {e}")
        return None


if __name__ == "__main__":

    prefix = R"C:\Users\Vasil"
    prefix = R"D:"

    # "input.mp4"  # Шлях до відео
    input_video = R"C:\_\video\video_in\unpacking___.mp4"
    image_file1 = prefix + \
        R"\OneDrive\Projects\Python4U_if_UR\VideoUtility\data\pict\python_red_hat_700_700.png"  # Перший PNG
    image_file2 = prefix + \
        R"\OneDrive\Projects\Python4U_if_UR\VideoUtility\data\pict\bmc_qr.png"  # Другий PNG

    final_video_clip = corner_morph_overlay(
        input_video,
        image_file1,
        image_file2,
        duration_static=60,
        duration_morph=20,
        overlay_size=150,
    )

    if final_video_clip:
        output_video = R"C:\_\video\33. unpacking_.mp4"
        final_video_clip.write_videofile(
            output_video,
            codec="h264",  # codec="h264_nvenc",  codec="libx264",
            audio_codec="aac",
            fps=26,      # final_video_clip.fps,
        )

        # final_video_clip.write_videofile(
        #     output_video,
        #     codec="h264_nvenc",  # Використовуємо апаратний енкодер NVIDIA
        #     audio_codec="aac",
        #     fps=final_video_clip.fps,
        #     ffmpeg_params=[
        #         # # Вибір пресету "slow" змушує енкодер виконувати більше роботи –
        #         # # це дозволяє досягнути кращої якості та стиснення, що рівноцінно сильнішому завантаженню GPU.
        #         # "-preset", "slow",
        #         # # Режим керування бітрейтом: VBR (variable bitrate)
        #         # # в комбінації з параметром якості (-cq) дає баланс між якістю та розміром файлу.
        #         # "-rc", "vbr",
        #         # "-cq", "19",  # Значення 19 (чим менше – тим вища якість, але трохи більший розмір).
        #         # # Встановлюємо стандарт сумісності H.264.
        #         # "-level", "4.1",
        #         # Оптимізація завантаження GPU: Lookahead аналізує наперед кількість кадрів для розподілу бітрейту
        #         "-rc-lookahead", "64",
        #         # Налаштування кількості поверхонь для обробки кадрів у пам’яті GPU
        #         "-surfaces", "64",
        #         "-pix_fmt", "yuv420p",
        #     ],
        # )

        final_video_clip.close()
        print(
            F"Відео з накладеним морфінгом створено та збережено у {output_video}")
