from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

def download_and_convert_to_mp3(youtube_url):
    # Download video
    print("Downloading video...")
    yt = YouTube(youtube_url)
    video_stream = yt.streams.filter(file_extension='mp4').first()
    video_path = os.path.join(r"C:\Users\AMozy\Videos", video_stream.download(output_path=r"C:\Users\AMozy\Videos"))
    # Convert to MP3
    print("Converting to MP3...")
    video_clip = VideoFileClip(video_path)
    mp3_path = video_path.replace(r"C:\Users\AMozy\Videos", r"C:\Users\AMozy\Music").replace(".mp4", ".mp3")
    mp3_path = os.path.join(r"C:\Users\AMozy\Music", os.path.basename(mp3_path))
    video_clip.audio.write_audiofile(mp3_path)
    print("Conversion complete. MP3 file saved at:", mp3_path)

while True:
    youtube_url = input('Enter Youtube video link => ')
    if youtube_url == 'c':
        break
    else:
        download_and_convert_to_mp3(youtube_url)
    