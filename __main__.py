from pathlib import Path

from knife_settings import (
    XLSX_FOLDER_STR,
    VIDEO_FOLDER_PATH_STR,
    
    AUDIO_FILE_PATH_STR,
    PNG_FILE_PATH_STR,
)

if __name__ == "__main__":
    # get `*.xlsx`
    # take valid `*.xlsx` files by comparing `*.mp4` file names
    # for each `*.xlsx` <--> `*.mp4` files pair do:

    # split `*.mp4` to named parts
    # create to each part - start clip with audio
    # glue `start clip` and `video part`
    # save result in special folder
    # 
    ...
