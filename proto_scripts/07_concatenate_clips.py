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
        R".\data\video_out\WD\output_prefix_video_01_4.mp4",
        R".\data\video_out\WD\normalized_audio_video_03_2.mp4",
    )
    output_video_path = concatenate_clips(
        clips_tuple,
        R".\data\video_out\WD\Серія 01_4. Чи є в Excel Python  Їх є три! Надбудова-Python запрацювала.mp4",
    )
    print(F"Склеєний відеофайл збережено як {output_video_path}")
