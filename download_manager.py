# download_manager.py
from pytube import YouTube
from file_manager import load_settings, clean_move_files
import threading, ffmpeg, os

def download_vids(link):
    resolution, file_type, path = load_settings()
    yt = YouTube(link)
    audio_stream = yt.streams.filter(only_audio=True).first()
    if resolution == "Highest":
        video = yt.streams.get_highest_resolution()
        generate_vid(video, audio_stream, yt.title, path, file_type)
    elif resolution == "Lowest":
        video = yt.streams.get_lowest_resolution()
        generate_vid(video, audio_stream, yt.title, path, file_type)

completion_event = threading.Event()

def generate_ffmpeg(title, input_video, input_audio):
    ffmpeg.output(input_video, input_audio,f'{title}.mp4', vcodec='copy', acodec='aac', ).run()
    completion_event.set()  



def generate_ffmpeg_t(title, input_video, input_audio):
    print("Before chdir:", os.getcwd())
    thread = threading.Thread(target=generate_ffmpeg, args=(title, input_video, input_audio))
    thread.start()

def generate_vid(video, audio_stream, title, quality, file_type):
        if file_type == "MP3":
            audio_stream.download(filename=f"{title}.mp3")
            return  
        if quality == True:
            quality = "_hi"
        else:
            quality = "_lo"
        video.download(filename="video.mp4")
        audio_stream.download(filename="audio.mp4")
        input_video = ffmpeg.input('video.mp4')
        input_audio = ffmpeg.input('audio.mp4')
        print(input_video)
        print(input_audio)
        generate_ffmpeg_t(title, input_video, input_audio)
        completion_event.wait()
        clean_move_files(title)
        completion_event.clear()
    
        



