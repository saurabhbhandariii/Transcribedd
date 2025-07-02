import os
import re
import subprocess
import whisper
from urllib.parse import urlparse
from yt_dlp import YoutubeDL

def extract_video_id(url):
    # Extract unique 11-character YouTube video ID
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else "video"

def download_video(url, output_path):
    print(f"Downloading video from: {url}")
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'quiet': False,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"Downloaded: {output_path}")

def extract_audio(video_path, audio_path):
    print("Extracting audio with ffmpeg...")
    if os.path.exists(audio_path):
        os.remove(audio_path)
    subprocess.run(['ffmpeg', '-y', '-i', video_path, '-ar', '16000', '-ac', '1', '-q:a', '0', '-map', 'a', audio_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def transcribe_audio(audio_path):
    print("Transcribing audio using Whisper...")
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, language="en")
    return result['text']

def main():
    url = input("Enter YouTube/TikTok/Instagram Reel URL: ").strip()
    video_id = extract_video_id(url)
    video_filename = f"{video_id}.mp4"
    audio_filename = f"{video_id}.mp3"

    if os.path.exists(video_filename):
        os.remove(video_filename)

    download_video(url, video_filename)
    extract_audio(video_filename, audio_filename)
    transcript = transcribe_audio(audio_filename)

    print("\n--- Transcript ---\n")
    print(transcript)

if __name__ == "__main__":
    main()
