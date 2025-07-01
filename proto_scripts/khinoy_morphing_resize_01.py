from PIL import Image
import os


def load_and_resize_image(path, target_height):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    aspect_ratio = w / h
    new_width = int(target_height * aspect_ratio)
    return img.resize((new_width, target_height), Image.Resampling.LANCZOS)


def create_morph_gif_from_files(
    bw_path,
    color_path,
    output_filename="morph.gif",
    transition_frames=90,
    transition_duration=200,
    final_duration=7000,
    target_height=None,
):
    # Завантаження та масштабування
    bw_img = Image.open(bw_path).convert("RGB")
    color_img = Image.open(color_path).convert("RGB")

    if target_height:
        bw_img = load_and_resize_image(bw_path, target_height)
        color_img = load_and_resize_image(color_path, target_height)
    else:
        color_img = color_img.resize(bw_img.size, Image.Resampling.LANCZOS)

    # Створення кадрів
    frames = []
    for i in range(transition_frames + 1):
        alpha = i / transition_frames
        frame = Image.blend(bw_img, color_img, alpha)
        frames.append(frame)

    durations = [transition_duration] * (transition_frames + 1)
    durations[-1] = final_duration

    # Збереження GIF
    frames[0].save(
        output_filename,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
    )

    print(f"✅ GIF збережено: {output_filename}")
    print(f"📸 Кадрів: {len(frames)}")
    print(f"⏱️ Перехід: {(transition_frames * transition_duration) / 1000} сек")
    print(f"🎯 Фінальний кадр: {final_duration / 1000} сек")
    print(
        f"🧭 Всього: {((transition_frames * transition_duration) + final_duration) / 1000} сек"
    )


# 🔧 Приклад виклику:
# create_morph_gif_from_files("bw_image.png", "color_image.png", target_height=500)
if __name__ == "__main__":
    # Приклад використання
    create_morph_gif_from_files(
        "C:\\Users\\Vasil\\Downloads\\церква_сіра.jpg",
        "C:\\Users\\Vasil\\Downloads\\церква_колор.jpg",
        output_filename="церква_morph_256.gif",
        target_height=256,
    )

