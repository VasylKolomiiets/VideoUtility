import configparser

config = configparser.ConfigParser()
config.read("video_knife.ini")

XLSX_FOLDER_STR = config['SOURCES']['xlsx']
AUDIO_FILE_PATH_STR = config['SOURCES']['audio']
PNG_FILE_PATH_STR = config['SOURCES']['png']
VIDEO_FOLDER_PATH_STR = config['SOURCES']['video']

print(XLSX_FOLDER_STR)