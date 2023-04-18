#mp3_downloader.py
import os
from pytube import YouTube
import moviepy.editor as mp

# function to download a single video as mp3
def download_video_as_mp3(url): 
    # create a YouTube object with the given URL
    youtube = YouTube(url)
    # get the audio stream of the video
    video = youtube.streams.filter(only_audio=True).first()
    # get the title of the video
    title = video.title
    # print a message to show that the download is starting
    print(f'Downloading "{title}" as an mp3...')
    # download the video
    video_path = video.download()
    # create the output mp3 filename by changing the extension of the video filename
    mp3_path = os.path.splitext(video_path)[0] + '.mp3'
    # create a MoviePy audio file clip from the video file
    clip = mp.AudioFileClip(video_path)
    # write the audio clip to the output mp3 file
    clip.write_audiofile(mp3_path)
    # close the clip object
    clip.close()
    # delete the video file
    os.remove(video_path)
    # print a message to show that the download is complete
    print(f'Download complete: "{title}.mp3"')

# function to download a playlist as mp3
def download_playlist_as_mp3(filename): 
    # open the file that contains the URLs of the videos in the playlist
    with open(filename, 'r') as file:
        # read the URLs into a list and remove any leading or trailing whitespace
        urls = file.readlines()
        urls = [url.strip() for url in urls]
    # print a message to show how many URLs were found in the file
    print(f'Found {len(urls)} URLs in "{filename}"')
    # download each video in the playlist
    for url in urls:
        download_video_as_mp3(url)
