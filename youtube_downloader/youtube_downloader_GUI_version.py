import yt_dlp
import os
from googleapiclient.discovery import build
import tkinter as tk
from tkinter import messagebox, filedialog

# API key to access the YouTube Data API
API_KEY = "YOUR_API_KEY"

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

def validate_link(link):
    try:
        ydl = yt_dlp.YoutubeDL()
        ydl.extract_info(link, download=False)
        return True
    except yt_dlp.DownloadError:
        return False

def download_single_audio(link_entry, is_one):
    if is_one == 1:
        link = link_entry.get()
    else:
        link = link_entry
    if validate_link(link) or is_one == 1:
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
        if is_one == 1:
            messagebox.showinfo("Download Complete", "File has been downloaded.")
    else:
        messagebox.showerror("Invalid Link", "Please enter a valid YouTube link.")

def download_single_video(link_entry, is_one):
    if is_one == 1:
        link = link_entry.get()
    else:
        link = link_entry
    if validate_link(link) or is_one == 1:
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',
            'outtmpl': '%(title)s.%(ext)s',
        }
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.extract_info(link)
        if is_one == 1:
            messagebox.showinfo("Download Complete", "File has been downloaded.")
    else:
        messagebox.showerror("Invalid Link", "Please enter a valid YouTube link.")

def download_from_file(download_func, is_one):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        search_with_each_line(file_path)
    with open("temp.txt", 'r') as file:
        for line in file:
            link = line.strip()
            download_func(link, is_one)
    os.remove("temp.txt")
    messagebox.showinfo("Download Complete", "Files have been downloaded.")

def main():
    # The app frame
    app = tk.Tk()
    app.geometry("720x480")
    app.title("Youtube Downloader")

    # Adding UI elements
    title = tk.Label(app, text="Insert a YouTube link")
    title.pack(padx=10, pady=10)

    # Link input
    url_var = tk.StringVar()
    link_entry = tk.Entry(app, width=350, textvariable=url_var)
    link_entry.pack()

    # Audio button
    audio_button = tk.Button(app, text="Download Audio", command=lambda: download_single_audio(link_entry, 1))
    audio_button.pack(padx=10, pady=10)

    # Video button
    video_button = tk.Button(app, text="Download Video", command=lambda: download_single_video(link_entry, 1))
    video_button.pack(padx=10, pady=10)

    # Audio download from file button
    audio_file_button = tk.Button(app, text="Download Audio from File", command=lambda: download_from_file(download_single_audio, 0))
    audio_file_button.pack(padx=10, pady=10)

    # Video download from file button
    video_file_button = tk.Button(app, text="Download Video from File", command=lambda: download_from_file(download_single_video, 0))
    video_file_button.pack(padx=10, pady=10)

    app.mainloop()

if __name__ == "__main__":
    main()