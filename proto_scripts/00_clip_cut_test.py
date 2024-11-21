import pandas as pd
import ffmpeg

video_file_name = R"C:\Users\Vasil\OneDrive\Projects\PyScools\PythonSpring\Videos\01\S_Lesson_00_Intro.mp4"
clip_file_xl = R"C:\Users\Vasil\OneDrive\Projects\Python4U_if_UR\VideoUtility\Lesson_01.xlsx"
# Зчитування даних з Excel
df = pd.read_excel(clip_file_xl)

num_threads = 5

print(df.head())
# end_time	part_title
start_time = "0:00:00"
for index, row in df.iterrows():
    part_title = row['part_title']
    end_time = row['end_time']
    output_file = f"{part_title}.mp4"  # Наприклад, створюємо вихідні файли з індексами

    # Обрізання відео за допомогою FFmpeg
    # stream = ffmpeg.input(video_file_name)
    # stream = stream.trim(start=start_time, end=end_time)
    # stream = stream.output(output_file)
    # ffmpeg.run(stream)
    # stream = ffmpeg.input(video_file_name)
    # stream = stream.trim(start=start_time, end=end_time)
    stream = ffmpeg.input(video_file_name, ss=start_time, to=end_time)
    stream = ffmpeg.output(stream, output_file,  **{'c:a': 'copy', 'threads': num_threads}   )
    ffmpeg.run(stream)
    start_time = end_time
    print(output_file)

print("It's happens")
