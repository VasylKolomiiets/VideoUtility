from moviepy.editor import VideoFileClip

def speed_up_video(input_file, output_file, speed_up_factor=2):
    """
    Прискорює відео.

    Args:
        input_file: Шлях до вхідного відеофайлу.
        output_file: Шлях до вихідного відеофайлу.
        speed_up_factor: Коефіцієнт прискорення.
    """

    clip = VideoFileClip(input_file)
    clip = clip.speedx(1 / speed_up_factor)  # Чим менший коефіцієнт, тим швидше відео
    clip.write_videofile(output_file, audio_codec='aac', bitrate='192k')

if __name__ == '__main__':
    # Приклад використання:
    speed_up_video("normalized_audio_video__.mp4", "fast_my_video.mp4", 0.75)
