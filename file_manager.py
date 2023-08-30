#file_manager.py

import os, json, shutil

os.chdir("C:\Python\YoutubeDLV2")


def load_settings():
    with open("settings.json", "r") as settings_file:
        settings = json.load(settings_file)
        resolution = settings["resolution"]
        file_type = settings["file_type"]
        path = settings["path"]
        return resolution, file_type, path
    
def get_path():
    resolution, file_type, path = load_settings()
    if path == "Desktop":
        return get_desktop_path()
    else:
        return get_download_path()

def save_setting(resolution, file_type, path):
    settings = {
        "resolution": resolution,
        "file_type": file_type,
        "path": path
    }
    with open("settings.json", "w") as settings_file:
        json.dump(settings, settings_file, indent=4)

def get_download_path():
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')

def get_desktop_path():
    return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

def clean_move_files(title):
    
    os.remove("audio.mp4")
    os.remove("video.mp4")

    existing_files = []
    if os.path.exists(f'{title}.mp3'):
        existing_files.append(f'{title}.mp3')
    if os.path.exists(f'{title}.mp4'):
        existing_files.append(f'{title}.mp4')

    # Move existing files based on their extension
    for file_path in existing_files:
        _, file_extension = os.path.splitext(file_path)
        if file_extension.lower() == '.mp3':
            destination = os.path.join(get_path(), f'{title}.mp3')
        elif file_extension.lower() == '.mp4':
            destination = os.path.join(get_path(), f'{title}.mp4')
        else:
            continue  # Skip files with other extensions
        
        shutil.move(file_path, destination)

