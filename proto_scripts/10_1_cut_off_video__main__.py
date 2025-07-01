from pathlib import Path

from moviepy.editor import VideoFileClip
# from moviepy.video.fx.resize import resize
from pathlib import Path
import importlib.util


def load_helper_module():
    """
    Динамічно завантажує модуль helper.py,
    який знаходиться в кореневій теці проекту.
    Структура:
        project/
        ├── video_knife.py    # містить normalize_audio
        └── current/
            └── script.py  # тут виконується завантаження модуля
    """
    # Визначаємо шлях до проекту, піднімаючись на один рівень від поточної теки
    project_path = Path(__file__).resolve().parent.parent
    helper_file = project_path / "video_knife.py"

    # Створення специфікації модуля за шляхом до video_knife.py
    spec = importlib.util.spec_from_file_location("video_knife", str(helper_file))
    video_knife = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(video_knife)
    return video_knife


def crop_and_resize_video(input_path, output_path, x1, y1, x2, y2):
    """
    Вирізає прямокутну область з відео та розтягує її до Full HD.

    Args:
        input_path (str): Шлях до вхідного відеофайлу.
        output_path (str): Шлях для збереження вихідного відеофайлу.
        x1 (int): Координата x лівої межі прямокутника.
        y1 (int): Координата y верхньої межі прямокутника.
        x2 (int): Координата x правої межі прямокутника.
        y2 (int): Координата y нижньої межі прямокутника.
    """
    try:
        # Завантаження відеокліпу
        clip = VideoFileClip(input_path)

        # Вирізання вказаної області
        cropped_clip = clip.crop(x1=x1, y1=y1, x2=x2, y2=y2)
        # x_width=x2 - x1, y_height=y2 - y1
        # Розтягування до роздільної здатності Full HD (1920x1080)
        resized_clip = cropped_clip.resize((1920, 1080))

        # Запис обробленого відео у файл
        resized_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        # Закриття кліпів для звільнення ресурсів
        clip.close()
        cropped_clip.close()
        resized_clip.close()

        print(F"Відео успішно оброблено та збережено у {output_path}")

    except Exception as e:
        print(F"Виникла помилка: {e}")


if __name__ == "__main__":
    video_knife = load_helper_module()
    
    folder = Path(R"C:\Users\Vasil\OneDrive\Projects\PyScools\PythonSpring\Videos\01")
    left_x, top_y, right_x, bottom_y = 0, 68, 1674, 1012    
    for file in folder.glob("*.mp4"):
        print(file)
        input_video_path = file
        output_video_path = file.parent / "cropped" / F'cropped_{file.name}'
        crop_and_resize_video(
            str(input_video_path), str(output_video_path),
            left_x, top_y, right_x, bottom_y,
        )
        print(F"Відео {file.name} успішно оброблено та збережено у {output_video_path}")
        # Нормалізація аудіо
        norm_video_path = output_video_path.parent.parent / "norm_audio" / F"norm_{output_video_path.name}"
        video_knife.normalize_audio(str(output_video_path), str(norm_video_path))
        print(F"Аудіо у відео {output_video_path} успішно нормалізовано.")
