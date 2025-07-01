from moviepy.editor import VideoFileClip
from moviepy.video.fx.resize import resize


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

        print(f"Відео успішно оброблено та збережено у {output_path}")

    except Exception as e:
        print(f"Виникла помилка: {e}")


if __name__ == "__main__":
    input_video_path = R"C:\Users\Vasil\OneDrive\Projects\PyScools\PythonSpring\Videos\01\S_Lesson_01_Turtle (2).mp4"  # Замініть на шлях до вашого вхідного відео
    output_video_path = "output_fullhd_0_68_1012_1674.mp4"
    left_x = 0
    top_y = 68
    right_x = 1674
    bottom_y = 1012

    crop_and_resize_video(
        input_video_path, output_video_path, left_x, top_y, right_x, bottom_y
    )
