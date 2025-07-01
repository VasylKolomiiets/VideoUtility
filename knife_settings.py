import configparser

import time
from functools import wraps

import psutil
from pathlib import Path

import re

config = configparser.ConfigParser()
# config = configparser.ConfigParser(
#     interpolation=configparser.ExtendedInterpolation())
#
config.read("video_knife.ini")

# config.read(R"D:\OneDrive\Projects\Python4U_if_UR\VideoUtility\video_knife.ini")

AUDIO_FILE = config['SOURCES']['audio']
PNG_FILE = config['SOURCES']['png']
XLSX_FOLDER = config["SOURCES"]["xlsx"]
VIDEO_FOLDER = config['SOURCES']['video_in']
WORK_FOLDER = config['SOURCES']['work']
VIDEO_OUT_FOLDER = config['SOURCES']['video_out']
NORM_SOUND = config['SOURCES']['norm_sound']

CORNER_MORFING = config['SOURCES']['corner_morfing']
CORNER_PNG_1 = config['SOURCES']['corner_png_1']
CORNER_PNG_2 = config['SOURCES']['corner_png_2']


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            F"{12*'-'}>Час виконання функції {func.__name__}: {end_time - start_time:.4f} секунд")
        return result
    return wrapper


@measure_time
def list_processes_using_file(file_path, verbose=True):
    """
    Виводить список процесів, які використовують заданий файл,
    та повертає список кортежів (назва процесу, PID). Якщо процес відкрив файл
    кілька разів, він з’явиться лише один раз.

    Аргументи:
        file_path (str або Path): Шлях до файлу, який потрібно перевірити.
        verbose (bool): Якщо True, результати виводяться на екран. За замовчуванням True.

    Повертає:
        list[tuple]: Список процесів у форматі (ім'я процесу, PID).
    """

    # Переконаємося, що file_path є об'єктом Path та отримуємо його канонічний вигляд.
    file_path = Path(file_path).resolve(strict=False)

    processes = []
    seen_pids = set()  # Щоб уникнути дублювання процесів

    # Перебір усіх процесів
    for proc in psutil.process_iter(attrs=["pid", "name"]):
        try:
            # Перегляд відкритих файлів процесу
            for file_info in proc.open_files():
                try:
                    opened_path = Path(file_info.path).resolve(strict=False)
                except Exception:
                    # Якщо не вдалось отримати канонічний шлях, використовуємо оригінальний рядок шляху.
                    opened_path = Path(file_info.path)

                # Якщо шляхи співпадають і процес ще не доданий до списку:
                if opened_path == file_path and proc.info["pid"] not in seen_pids:
                    seen_pids.add(proc.info["pid"])
                    processes.append((proc.info["name"], proc.info["pid"]))
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

    if verbose:
        if processes:
            print(f"\nФайл {file_path} використовується наступними процесами:")
            for name, pid in processes:
                print(f"- {name} (PID: {pid})")
        else:
            print(f"\nФайл {file_path} не використовується жодним процесом.")

    return processes


def sanitize_filename(filename, replacement="_"):
    """
    Очищає назву файлу, замінюючи пробіли та неприпустимі символи на заданий символ (за замовчуванням '_').

    Args:
        filename (str): Оригінальна назва файлу.
        replacement (str): Символ для заміни пробілів та недопустимих знаків (за замовчуванням '_').

    Returns:
        str: Очищена назва файлу.
    """
    # Список неприпустимих символів у назві файлу (Windows/Linux)
    invalid_chars = r'[<>:"/\\|?*\t\r\n]'

    # Замінюємо пробіли та неприпустимі символи
    sanitized = re.sub(invalid_chars, replacement, filename)
    sanitized = sanitized.replace(" ", replacement)

    return sanitized


# Приклад використання:
if __name__ == "__main__":
    test_file = "C:\\Users\\Vasil\\OneDrive\\Projects\\Python4U_if_UR\\VideoUtility\\data\\video_work\\DW_01_2.mp4"
    list_processes_using_file(test_file)

    # Приклад використання
    original_name = "My File: With /Invalid?Chars.txt"
    clean_name = sanitize_filename(original_name)
    print(f"Оригінальна назва: {original_name}")
    print(f"Очищена назва: {clean_name}")

# print(XLSX_FOLDER_STR)
