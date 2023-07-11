import webbrowser
import os
import yt_dlp
from googleapiclient.discovery import build

# API key to access the YouTube Data API
API_KEY = "YOUR_API_KEY"

def validate_link(link):
    try:
        ydl = yt_dlp.YoutubeDL()
        ydl.extract_info(link, download=False)
        return True
    except yt_dlp.DownloadError:
        return False

def download_audio(link):
    if validate_link(link):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
        }
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.extract_info(link)
    else:
        print(f"Error while downloading {link}")            

def download_video(link):
    if validate_link(link):
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',
            'outtmpl': '%(title)s.%(ext)s',
        }
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.extract_info(link)
    else:
        print(f"Error while downloading {link}")

def download_from_file(download_func):
    with open("temp.txt", 'r') as file:
        for line in file:
            link = line.strip()
            download_func(link)
    print("Download Complete, All links have been downloaded.")

def search_youtube(query):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    
    # Search for the query on YouTube
    response = youtube.search().list(part="snippet", q=query, maxResults=1).execute()
    items = response.get("items", [])
    
    # Extract the URL of the first search result
    if items:
        video_id = items[0]["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    
    return None

def save_link_to_file(file_path, query):
    video_url = search_youtube(query)
    
    if video_url:
        with open(file_path, "a") as file:
            file.write(video_url + "\n")
        print(f"Saved link for '{query}'")

def search_with_each_line(file_path):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                query = line.strip()
                save_link_to_file("temp.txt", query)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def download_from_file_menu():
    try:
        file_path = input("Enter the file name: ")
        search_with_each_line(file_path)
        video_or_audio = int(input("Enter\n1.For video\n2.For audio: "))
        if video_or_audio == 1:
            download_from_file(download_video)
        elif video_or_audio == 2:
            download_from_file(download_audio)
        os.remove("temp.txt")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
def download_link_menu():
    link = input("Enter the link: ")
    video_or_audio = int(input("Enter\n1.For video\n2.For audio: "))
    if video_or_audio == 1:
        download_video(link)
    elif video_or_audio == 2:
        download_audio(link)

def main():
    print("Welcome to youtube downloader!")
    file_or_link = input("Do you want to download from a file or a single link? ")
    
    if file_or_link.lower() == "file":
        download_from_file_menu()    
    elif file_or_link.lower() == "single link":
        download_link_menu()

if __name__ == "__main__":
    main()