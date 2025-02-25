import configparser

config = configparser.ConfigParser()
config.read("video_knife.ini")

XLSX_FOLDER_STR = config['SOURCES']['xlsx']
AUDIO_FILE_PATH_STR = config['SOURCES']['audio']
PNG_FILE_PATH_STR = config['SOURCES']['png']
VIDEO_FOLDER_PATH_STR = config['SOURCES']['video']

import time
from functools import wraps

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