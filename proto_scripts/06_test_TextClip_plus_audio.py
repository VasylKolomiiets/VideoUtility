import time

from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip


def create_video_with_text(
        image_path, audio_path,
        text,
        q_threads=2,
        output_path="output_video.mp4",
):
    """
    Створює відеозаставку зображення, аудіо та тексту.

    Args:
    - image_path: Шлях до зображення.
    - audio_path: Шлях до аудіофайлу.
    - text: Текст, який потрібно додати до зображення.
    - output_path: Шлях для збереження вихідного відеофайлу.

    Returns:
    - Шлях до збереженого відеофайлу.
    """
    # Завантаження аудіо
    audio_clip = AudioFileClip(audio_path)

    # Завантаження зображення та створення відеокліпу з тривалістю аудіо
    image_clip = ImageClip(image_path, duration=audio_clip.duration)
    print(F"{image_clip.size=}")

    # Створення текстового кліпу
    text_clip = TextClip(
        text, fontsize=120, color='white',
        align='West',
        size=image_clip.size,
    ).set_duration(audio_clip.duration)

    # Розташування текстового кліпу на зображенні
    text_clip = text_clip.set_position(
        (1000, 0)).set_duration(audio_clip.duration)

    # Створення композитного відеокліпу
    video_clip = CompositeVideoClip([image_clip, text_clip])

    # Додавання аудіо до відеокліпу
    video_clip = video_clip.set_audio(audio_clip)

    # Збереження відеофайлу
    print(F"{q_threads=}")
    video_clip.write_videofile(
        output_path,
        codec='libx264', audio_codec='aac',
        fps=24,
        threads=q_threads,
    )

    return output_path


# Приклад використання функції
if __name__ == "__main__":
    # Вимірюємо час виконання
    time_0 = time.time()
    q_threads = 2
    # Вказуємо шляхи до зображення та аудіо
    prefix = R"C:\Users\Vasil"
    prefix = R"D:"
    image_path = prefix + \
        R"\OneDrive\Projects\Python4U_if_UR\VideoUtility\data\pict\python1080_red_hat1920Done_blured.png"
    audio_path = prefix + \
        R"\OneDrive\Projects\Python4U_if_UR\VideoUtility\data\sound\36161__sagetyrtle__bells2.wav"

    # Текст для відеозаставки
    text = "33. Операция *\nпри распаковке\nсписков_кортежей"

    # Створюємо відеозаставку
    output_path = create_video_with_text(
        image_path,
        audio_path,
        text,
        output_path=R".\data\video_out\WD\output_prefix_video_33.mp4",
        q_threads=q_threads,
    )

    # Виводимо час виконання
    print(
        F"Час виконання при {q_threads=} у секундах:  {(time.time() - time_0):5.2f}")
    print(F"Відеофайл збережено як {output_path}")

#  "Серія 01.\nНезрозумілий\nвступ, або\nплан\nстворення\nвідеоутиліт"
#  "Серія 02.\nСтворення\nі видалення \nробочого ото\nчення Python в\nAnaconda"
#  "Серія 03.\nПоради Gemini\nта Copilot \nщодо вибору\nмодулів та \nїх встановлення"
#  "Серія 04.\nПогано став\nIpython. Як\nзапобігти"
#  "Серія 05.\nКод з moviepy\nнарізає відео.\nАле жере 100%\nчасу процесора"
#  "Серія 06.\nПоради Gemini\nта Copilot \nщодо параметру\n threads= модуля\nmoviepy"
#  "Серія 07.\nКод додавання\nтексту на \n зображення"
#  "Серія 08.\nCopilot та Gemini\nстворюють\nзаставку\nдля відео"
#  "Серія 09.\nЗберігаю $20\nна встановленні\nPAINT.NET"
#  "Серія 10.\nТуплю з\nрозтягуванням\nзаставки\nв PAINT.NET"
#  "Серія 11.\nБлюр в\nPAINT.NET та\nсмішно з\nCOPILOT"
#  "Серія 12.\nMoviePy.\nВідеозаставка\n=Текст+Аудіо\n+Малюнок"
#  "Серія 13.\nРозміщуємо\nтекст. Метод\nset_position()"
#  "Серія 14.\nMoviePy.\nСклеювання\nдекількох\nвідео в одне"
#  "Серія 15.\nCтворення\nструктури проекту\nопрацювання\nвідео на Python.\nРозробка\nзгори вниз"
#  "Серія 16.\nРозрулюємо\nзатики створення\nрепозитарію\nпроекту із\nVS code"
#  "Серія 17.\nВикористання\nмодуля\nconfigparser для\nініціалізації\nконстант проекту"
#  "Серія 18.\n.gitconfig та\n.gitignore\nщо таке і навіщо"
#  "Серія_19.\nМаркдаун\nрозмітка в\nVS code та\nRedmi.md файл\nдля GitHub"
#  "Серія_20.\nПриклад\nнарізки відео\nнашими\nфункціями.\nДіємо покроково"
#  "Серія 21.\nПроцес\nпублікації \nвідео на\nYouTube"
#  "Серія 22.\nФункція нарізки\nтексту для\nвідео-заставки"
#  "Серія 23.\nПідбір оптималь\nного параметра\nфункції нарізки\nтексту"
#  "Серія 24.\nРекурсія - \nвід початку.\nГРОНО"
#  "Серія 25.\nКритерії ГРОНО.\nРекурсія.\nЧи можна без\nнеї?"
#  "Серія 26.\nVibe coding\nvs AImbiotic\ncoding. ШІмбіот\nичне програму\nвання"
#  "Серія 27.\nПростий приклад\nвикористання\nCitHub Copilot"
#   f
#
