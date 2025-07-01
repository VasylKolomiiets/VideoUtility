import math


def get_interpolator(method):
    if method == "linear":
        return lambda x: x
    elif method == "cosine":
        return lambda x: 0.5 * (1 - math.cos(math.pi * x))
    elif method == "smoothstep":
        return lambda x: x * x * (3 - 2 * x)
    else:
        raise ValueError("Невідомий метод інтерполяції")


def create_color_loop_gif(
    bw_url,
    color_url,
    output_filename="pomegranate_loop.gif",
    transition_frames=90,
    transition_duration=200,
    final_duration=7000,
    interpolation="cosine",
):
    import requests
    from PIL import Image
    import io

    def load_image_from_url(url):
        response = requests.get(url)
        return Image.open(io.BytesIO(response.content))

    bw_img = load_image_from_url(bw_url).convert("RGB")
    color_img = load_image_from_url(color_url).convert("RGB")
    color_img = color_img.resize(bw_img.size, Image.Resampling.LANCZOS)

    interpolator = get_interpolator(interpolation)
    frames = []
    durations = []

    # Морфінг до кольору
    for i in range(transition_frames + 1):
        alpha = interpolator(i / transition_frames)
        frame = Image.blend(bw_img, color_img, alpha)
        frames.append(frame)
        durations.append(transition_duration)

    # Утримання кольору
    frames.append(color_img)
    durations.append(final_duration)

    # Морфінг назад
    for i in range(transition_frames + 1):
        alpha = interpolator(1 - (i / transition_frames))
        frame = Image.blend(bw_img, color_img, alpha)
        frames.append(frame)
        durations.append(transition_duration)

    # Утримання ч/б
    frames.append(bw_img)
    durations.append(final_duration)

    frames[0].save(
        output_filename,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
    )

    print(f"GIF створено: {output_filename}")
    print(f"Загальна тривалість: {sum(durations) / 1000} секунд, Кадрів: {len(frames)}")


if __name__ == "__main__":
    bw_url = (
        "https://page1.genspark.site/v1/base64_upload/0cd27251608576d4edad163dfea49b96"
    )
color_url = (
    "https://page1.genspark.site/v1/base64_upload/885bf3226ed22b19323e9c7f6cf5ecd2"
)

create_color_loop_gif(
    bw_url=bw_url,
    color_url=color_url,
    output_filename="pomegranate_loop_smooth.gif",
    transition_frames=90,
    transition_duration=200,
    final_duration=7000,
    interpolation="smoothstep",  # 👈 можна спробувати 'linear', 'cosine', або 'smoothstep'
)