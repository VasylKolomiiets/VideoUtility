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
    final_clip.write_videofile(
        output_path, codec='libx264', audio_codec='aac', fps=24)  # , threads=8
    return output_path


# Приклад використання функції
if __name__ == "__main__":
    clips_tuple = (
        R".\data\video_out\WD\output_prefix_video_33.mp4",
        R"C:\_\video\33. unpacking_.mp4",
        # R"C:\_\video\video_in\4_кортеж_1.mp4"
    )
    output_video_path = concatenate_clips(
        clips_tuple,
        R"C:\_\video\33. 33. Операция _ при распаковке списков и кортежей.mp4",
    )
    print(F"Склеєний відеофайл збережено як {output_video_path}")
