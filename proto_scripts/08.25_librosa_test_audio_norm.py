from moviepy.editor import VideoFileClip
import librosa
# from librosa.loudness import loudness
import numpy as np

def normalize_to_lufs(input_file, output_file, target_lufs=-14):
    """
    Нормалізує аудіо до вказаного рівня LUFS.

    Args:
        input_file: Шлях до вхідного відеофайлу.
        output_file: Шлях до вихідного відеофайлу.
        target_lufs: Бажаний рівень LUFS.
    """

    # Завантажуємо відео
    clip = VideoFileClip(input_file)

    # Отримуємо аудіодорожку
    audio_clip = clip.audio

    # Зберігаємо аудіо у тимчасовий файл
    audio_clip.write_audiofile("temp.wav")

    # Завантажуємо аудіо за допомогою librosa для обробки
    y, sr = librosa.load("temp.wav", sr=None)

    # Обчислюємо гучність і коригуємо посилення
    loudness = librosa.loudness.loudness(y)
    gain = target_lufs - loudness[0]
    y_normalized = librosa.util.normalize(y, norm=np.inf) * 10**(gain/20)

    # Зберігаємо нормалізоване аудіо
    librosa.output.write_wav("normalized_audio.wav", y_normalized, sr)

    # Замінюємо аудіо в відео
    clip = clip.set_audio("normalized_audio.wav")
    clip.write_videofile(output_file)

if __name__ == '__main__':
    test_mp4 = R"C:\Users\Vasil\OneDrive\Документи\Zoom\2024-11-18 15.55.31 Vasyl Kolomiets's Zoom Meeting\video1305318331.mp4"
    norm_audio = "normalized_audio_video.mp4"
    normalize_to_lufs(test_mp4, norm_audio)
