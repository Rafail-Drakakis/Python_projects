#mp3_downloader.py
import os
import pytube
import moviepy.editor as mp

def download_video_as_mp3(url): # function to download a single video as mp3
    youtube = pytube.YouTube(url)
    video = youtube.streams.filter(only_audio=True).first()
    title = video.title
    print(f'Downloading "{title}" as an mp3...')
    video_path = video.download()
    mp3_path = os.path.splitext(video_path)[0] + '.mp3'
    clip = mp.AudioFileClip(video_path)
    clip.write_audiofile(mp3_path)
    clip.close()
    os.remove(video_path)
    print(f'Download complete: "{title}.mp3"')

def download_playlist_as_mp3(filename): # function to download a playlist as mp3
    with open(filename, 'r') as file:
        urls = file.readlines()
        urls = [url.strip() for url in urls]
    print(f'Found {len(urls)} URLs in "{filename}"')
    for url in urls:
        download_video_as_mp3(url)