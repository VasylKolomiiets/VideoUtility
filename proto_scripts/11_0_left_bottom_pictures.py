from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip


def overlay_fading_images(
    video_path,
    image1_path,
    image2_path,
    output_path,
    position=("left", "bottom"),
    fade_duration=20,
    static_duration=60,
):
    # Завантажуємо відео
    clip = VideoFileClip(video_path)

    # Створюємо перше зображення
    img1 = (
        ImageClip(image1_path, duration=static_duration)
        .set_position(position)
        .resize(height=200)
    )

    # Створюємо друге зображення
    img2 = (
        ImageClip(image2_path, duration=static_duration)
        .set_position(position)
        .resize(height=200)
    )

    # Додаємо плавні переходи між зображеннями
    transition1 = img1.crossfadein(fade_duration)
    transition2 = img2.crossfadein(fade_duration)

    # Формуємо цикл зміни зображень
    loop_sequence = [img1, transition1, img2, transition2]

    # Об'єднуємо все у фінальне відео
    final_clip = CompositeVideoClip([clip] + loop_sequence, size=clip.size)

    # Запис у файл
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)

if __name__ == "__main__":
    # Шляхи до файлів
    video_path = R"output_fullhd__bil.mp4"
    image1_path = R"C:\Users\Vasil\OneDrive\Projects\Python4U_if_UR\VideoUtility\data\pict\pesah_2025_copilot.png"
    image2_path = R"C:\Users\Vasil\OneDrive\Projects\Python4U_if_UR\VideoUtility\data\pict\python1080_red_hat1920Done_blured.png"
    output_path = R"..\output_video.mp4"
    # Використання функції
    overlay_fading_images(
        video_path,
        image1_path,
        image2_path,
        output_path,
    )

