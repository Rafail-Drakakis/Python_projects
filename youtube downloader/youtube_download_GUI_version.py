import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess, yt_dlp

def validate_link(link):
    """
    The function `validate_link` checks if a given link is a valid YouTube video link.
    
    :param link: The `link` parameter is a string that represents a URL or link to a video
    :return: The function `validate_link` returns a boolean value. It returns `True` if the link is
    valid and can be successfully extracted using `yt_dlp.YoutubeDL()`, and it returns `False` if there
    is a `yt_dlp.DownloadError` while trying to extract the information from the link.
    """
    try:
        ydl = yt_dlp.YoutubeDL()
        ydl.extract_info(link, download=False)
        return True
    except yt_dlp.DownloadError:
        return False

def download_audio(link_entry, is_one):
    """
    The function `download_audio` downloads audio from a YouTube link and displays a message box if the
    download is complete or if the link is invalid.
    
    :param link_entry: The `link_entry` parameter is a reference to an entry widget in a graphical user
    interface (GUI) where the user can enter a YouTube link
    :param is_one: The parameter "is_one" is a flag that indicates whether the user wants to download
    only one audio file or multiple audio files. If "is_one" is set to 1, it means the user wants to
    download only one audio file
    """
    link = link_entry.get()
    if validate_link(link):
        terminal_command = f'yt-dlp -x --audio-format mp3 {link}'
        subprocess.run(terminal_command, shell=True)
        if is_one == 1:
            messagebox.showinfo("Download Complete", "File has been downloaded.")
    else:
        messagebox.showerror("Invalid Link", "Please enter a valid YouTube link.")

def download_video(link_entry, is_one):
    """
    The function `download_video` takes a YouTube link as input, validates it, and downloads the video
    using the `yt-dlp` command line tool. If the `is_one` parameter is set to 1, a message box is
    displayed indicating that the download is complete.
    
    :param link_entry: The `link_entry` parameter is a reference to an entry widget in a graphical user
    interface (GUI) where the user can enter a YouTube link
    :param is_one: The parameter "is_one" is a flag that indicates whether the user wants to download
    only one video or multiple videos. If "is_one" is set to 1, it means the user wants to download only
    one video. If it is set to 0 or any other value, it means
    """
    link = link_entry.get()
    if validate_link(link):
        terminal_command = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" {link}'
        subprocess.run(terminal_command, shell=True)
        if is_one == 1:
            messagebox.showinfo("Download Complete", "File has been downloaded.")
    else:
        messagebox.showerror("Invalid Link", "Please enter a valid YouTube link.")

def download_from_file(download_func, is_one):
    """
    The function `download_from_file` allows the user to select a text file, reads each line in the
    file, and calls a specified download function with the line as an argument.
    
    :param download_func: The download_func parameter is a function that will be called to download a
    file. It should take two arguments: link_entry and is_one
    :param is_one: The parameter "is_one" is likely a boolean value that determines whether the download
    function should download only one file or multiple files. If "is_one" is True, the download function
    will download only one file. If "is_one" is False, the download function will download multiple
    files
    """
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            for line in file:
                link_entry.delete(0, tk.END)
                link_entry.insert(0, line.strip())
                download_func(link_entry, is_one)
        messagebox.showinfo("Download Complete", "All links have been downloaded.")

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
audio_button = tk.Button(app, text="Download Audio", command=lambda: download_audio(link_entry, 1))
audio_button.pack(padx=10, pady=10)

# Video button
video_button = tk.Button(app, text="Download Video", command=lambda: download_video(link_entry, 1))
video_button.pack(padx=10, pady=10)

# Audio download from file button
audio_file_button = tk.Button(app, text="Download Audio from File", command=lambda: download_from_file(download_audio, 0))
audio_file_button.pack(padx=10, pady=10)

# Video download from file button
video_file_button = tk.Button(app, text="Download Video from File", command=lambda: download_from_file(download_video, 0))
video_file_button.pack(padx=10, pady=10)

app.mainloop()