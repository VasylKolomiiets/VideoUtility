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
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24, threads=8)
    
    return output_path

# Приклад використання функції
clips_tuple = ("output_video.mp4", "Як_встановити_потрібні_модулі.mp4", "Як створити заставку із текстом.mp4")
output_video_path = concatenate_clips(clips_tuple, "concatenated_video.mp4")
print(f"Склеєний відеофайл збережено як {output_video_path}")
