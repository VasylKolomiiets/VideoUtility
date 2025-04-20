from pathlib import Path

from knife_settings import (
    AUDIO_FILE,
    PNG_FILE,
    XLSX_FOLDER,
    VIDEO_FOLDER,
    WORK_FOLDER,
    VIDEO_OUT_FOLDER,
    list_processes_using_file,
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
        # split `*.mp4` to named parts
        new_mp4_files.extend(split_video(mp4_file, xlsx_file, Path(WORK_FOLDER)))
    
    
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
        
    import gc  # Import garbage collector to ensure resources are freed

    for part_data in new_mp4_files:
        # Ensure all resources are released before unlinking
        gc.collect()
        print(F"Deleting {part_data['output_file']} and \n {part_data['prefix_file']}")
        for file in (part_data["output_file"], part_data["prefix_file"]):
            if not list_processes_using_file(file):
                file.unlink(missing_ok=True)
        # remove temporary files
    # End of processing     
