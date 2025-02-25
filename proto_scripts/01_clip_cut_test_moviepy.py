import pandas as pd
from moviepy.video.io.VideoFileClip import VideoFileClip

# video_file_name = R"C:\Users\Vasil\OneDrive\Projects\PyScools\PythonSpring\Videos\01\S_Lesson_00_Intro.mp4"
video_file_name = R".\data\video_out\15\normalized_audio_video_15.mp4"
clip_file_xl = R"C:\Users\Vasil\OneDrive\Projects\Python4U_if_UR\VideoUtility\data\xlsx\Lesson_15.xlsx"
# Зчитування даних з Excel
df = pd.read_excel(clip_file_xl)

print(df.head())

# end_time	part_title

# Завантаження відео 
clip = VideoFileClip(video_file_name)

start_time = "0:00:00.0"
for index, row in df.iterrows():
    part_title = row['part_title']
    end_time = row['end_time']
    print(F"{end_time=} is {type(end_time)} type.")
    output_file = f"{part_title}.mp4"  # Наприклад, створюємо вихідні файли з індексами

    # Обрізка відео
    subclip = clip.subclip(start_time, end_time)
    
    # Збереження обрізаного відео 
    subclip.write_videofile(output_file, codec='libx264', audio_codec='aac')
    start_time = end_time

    print(output_file)
