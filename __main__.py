import gc  # Import garbage collector to ensure resources are freed
from pathlib import Path

from knife_settings import (
    AUDIO_FILE,
    PNG_FILE,
    XLSX_FOLDER,
    VIDEO_FOLDER,
    WORK_FOLDER,
    VIDEO_OUT_FOLDER,
    NORM_SOUND,
    # list_processes_using_file,
    sanitize_filename,
)

from video_knife import (
    split_video,
    create_video_with_text,
    normalize_audio,
    concatenate_clips,
    break_str,
)

def prefix_file_name(file_path: Path) -> str:
    return "_".join([
        file_path.stem, 
        'prefix', 
        file_path.suffix,
        ]) 


def delete_file(file_path: Path) -> bool:
    """
    Видаляє файл, якщо він існує.

    Аргументи:
        file_path (Path): Шлях до файлу, який потрібно видалити.

    Повертає:
        bool: True, якщо файл успішно видалено, інакше False.
    """
    try:
        file_path.unlink(missing_ok=True)
        print(F"Файл {file_path} успішно видалено")
        return True
    except Exception as excp:
        print(F"Не вдалося видалити {file_path}: {excp}")
        return False


if __name__ == "__main__":
    # get `*.xlsx`
    xlsx_files = set(Path(XLSX_FOLDER).glob("*.xlsx"))
    # get `*.mp4`
    mp4_files = set(Path(VIDEO_FOLDER).glob("*.mp4"))
    # take valid `*.xlsx` files by comparing `*.mp4` file names
    valid_xlsx_files = {xlsx for xlsx in xlsx_files if xlsx.stem in {mp4.stem for mp4 in mp4_files}}

    new_mp4_files = list()
    # for each `*.xlsx` <--> `*.mp4` files pair do:
    for xlsx_file in valid_xlsx_files:
        mp4_file = Path(VIDEO_FOLDER) / (xlsx_file.stem + ".mp4")
        if NORM_SOUND == '1':
            mp4_file_norm = Path(VIDEO_FOLDER) / (mp4_file.stem + "_norm.mp4")
            normalize_audio(
                str(mp4_file.resolve()), 
                str(mp4_file_norm),
            )
            mp4_file_par = mp4_file_norm
        else:
            print(F"Нормалізація звуку вимкнена для {mp4_file}")
            mp4_file_par = mp4_file

        # split `*.mp4` to named parts
        new_mp4_files.extend(split_video(mp4_file_par, xlsx_file, Path(WORK_FOLDER)))
    
    
    for part_data in new_mp4_files:
        # create new video with text for each part
        part_data["prefix_file"] = Path(WORK_FOLDER) / prefix_file_name(
            part_data["output_file"]
        )
        create_video_with_text(
            PNG_FILE,
            AUDIO_FILE,
            break_str(part_data["prefix_text"], 15),
            output_path=str(part_data["prefix_file"]),
        )

        # glue `start clip` and `video part`
        concatenate_clips(
            (str(part_data["prefix_file"]), str(part_data["output_file"])),
            str(Path(VIDEO_OUT_FOLDER) / (sanitize_filename(part_data["prefix_text"]) + ".mp4")),
        )
        # save result in special folder
        
    # Звільняємо ресурси перед початком циклу
    gc.collect()
    undeleted_files = []
    if NORM_SOUND == '1':  # if sound normalization is on  # "mp4_file_norm" in locals() 
        # remove `*_norm.mp4` files
        if not delete_file(mp4_file_norm):
            undeleted_files.append(mp4_file_norm)

    for part_data in new_mp4_files:
        output_file, prefix_file = part_data["output_file"], part_data["prefix_file"]
        print(f"Видаляємо файли:\n {output_file}\n {prefix_file}")
        for file in (output_file, prefix_file):           
            if not delete_file(file):
                undeleted_files.append(file)

    if undeleted_files:
        print("\nСписок файлів, які не вдалося видалити:")
        for f in undeleted_files:
            print(f)

