from moviepy.editor import AudioFileClip
from pydub import AudioSegment
from pytube import YouTube
from os import remove
from os.path import splitext

#audio_converter.py
def convert_audio(input_path, output_path):
    # Get the input file extension
    input_file_ext = input_path.split(".")[-1]
    # Get the output file extension
    output_file_ext = output_path.split(".")[-1]
    # Load audio file
    audio = AudioSegment.from_file(input_path, format=input_file_ext)
    # Export audio file
    audio.export(output_path, format=output_file_ext)
    print("File converted successfully")

#audio_downloader.py
def download_audio(url, extension):
    # create a YouTube object with the given URL
    youtube = YouTube(url)
    # get the audio stream of the video
    video = youtube.streams.filter(only_audio=True).first()
    # get the title of the video
    title = video.title
    # print a message to show that the download is starting
    print(f'Downloading "{title}" as a {extension}...')
    # download the video
    video_path = video.download()
    # create the output audio filename by changing the extension of the video filename
    audio_path = splitext(video_path)[0] + f'.{extension}'
    # create a MoviePy audio file clip from the video file
    clip = AudioFileClip(video_path)
    # write the audio clip to the output audio file
    clip.write_audiofile(audio_path)
    # close the clip object
    clip.close()
    # delete the video file
    remove(video_path)
    # print a message to show that the download is complete
    print(f'Download complete: "{title}.{extension}"')

def download_playlist(filename, extension): 
    # open the file that contains the URLs of the videos in the playlist
    with open(filename, 'r') as file:
        # read the URLs into a list and remove any leading or trailing whitespace
        urls = file.readlines()
        urls = [url.strip() for url in urls]
    # print a message to show how many URLs were found in the file
    print(f'Found {len(urls)} URLs in "{filename}"')
    # download each video in the playlist
    for url in urls:
        download_audio(url, extension)
