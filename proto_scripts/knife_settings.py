import configparser

import time
from functools import wraps

config = configparser.ConfigParser()
config.read("video_knife.ini")

AUDIO_FILE = config['SOURCES']['audio']
PNG_FILE = config['SOURCES']['png']
XLSX_FOLDER = config["SOURCES"]["xlsx"]
VIDEO_FOLDER = config['SOURCES']['video_in']
WORK_FOLDER = config['SOURCES']['work']
VIDEO_OUT_FOLDER = config['SOURCES']['video_out']




def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Час виконання функції {func.__name__}: {end_time - start_time:.4f} секунд")
        return result
    return wrapper

# print(XLSX_FOLDER_STR)