import tkinter
from tkinter import filedialog, messagebox
import os
import yt_dlp

def validate_link(link):
    try:
        ydl = yt_dlp.YoutubeDL()
        ydl.extract_info(link, download=False)
        return True
    except yt_dlp.DownloadError as e:
        messagebox.showerror("Download Error")
        return False
    except Exception as e:
        messagebox.showerror("Download Error")
        return False

def download_audio(link_entry):
    link = link_entry.get()
    if validate_link(link):
        title.configure(text=link, fg="white")
        terminal_command = f'yt-dlp -x --audio-format mp3 {link}'
        try:
            os.system(terminal_command)
        except Exception as e:
            messagebox.showerror("Error")

def download_video(link_entry):
    link = link_entry.get()
    if validate_link(link):
        title.configure(text=link, fg="white")
        terminal_command = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" {link}'
        try:
            os.system(terminal_command)
        except Exception as e:
            messagebox.showerror("Error")

def download_from_file(file_type, download_func):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            for line in file:
                link_entry.delete(0, tk.END)
                link_entry.insert(0, line.strip())
                try:
                    download_func(link_entry)
                except Exception as e:
                    messagebox.showerror("Error")

# The app frame
app = tkinter.Tk()
app.geometry("720x480")
app.title("Youtube Downloader")

# Adding UI elements
title = tkinter.Label(app, text="Insert a YouTube link")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link_entry = tkinter.Entry(app, width=350, textvariable=url_var)
link_entry.pack()

# Audio button
audio_button = tkinter.Button(app, text="Download Audio", command=lambda: download_audio(link_entry))
audio_button.pack(padx=10, pady=10)

# Video button
video_button = tkinter.Button(app, text="Download Video", command=lambda: download_video(link_entry))
video_button.pack(padx=10, pady=10)

# Audio download from file button
audio_file_button = tkinter.Button(app, text="Download Audio from File", command=lambda: download_from_file("audio", download_audio))
audio_file_button.pack(padx=10, pady=10)

# Video download from file button
video_file_button = tkinter.Button(app, text="Download Video from File", command=lambda: download_from_file("video", download_video))
video_file_button.pack(padx=10, pady=10)

app.mainloop()