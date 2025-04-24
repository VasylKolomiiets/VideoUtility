from moviepy.editor import VideoFileClip, concatenate_videoclips

def concatenate_clips(clips, output_path="concatenated_video.mp4"):
    """
    Склеює відеокліпи з кортежа та зберігає їх у вихідний відеофайл.

    :param clips: Кортеж шляхів до відеофайлів (mp4)
    :param output_path: Шлях до вихідного відеофайлу (mp4)
    :return: Шлях до збереженого відеофайлу
    """
    # Завантаження відеокліпів
    video_clips = [VideoFileClip(clip) for clip in clips]

    # Склеювання відеокліпів
    final_clip = concatenate_videoclips(video_clips)

    # Збереження вихідного відеофайлу
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)  # , threads=8
    return output_path

# Приклад використання функції
if __name__ == "__main__":
    clips_tuple = (
        R".\data\video_out\30\output_prefix_video_30.mp4",
        R".\data\video_out\30\pyinstaller.mp4",
        R".\data\video_out\30\openpyxl.mp4",
        R".\data\video_out\30\the_final_part.mp4",
    )
    output_video_path = concatenate_clips(
        clips_tuple,
        R".\data\video_out\30\Серія 30. Як із Python-файлу створити .exe.mp4",
    )
    print(F"Склеєний відеофайл збережено як {output_video_path}")
