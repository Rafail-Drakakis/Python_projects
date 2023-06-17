import tkinter as tk, os
from tkinter import filedialog, messagebox

def download_audio(link_entry):
    title.configure(text=link_entry.get(), fg="white")
    terminal_command = f'yt-dlp -x --audio-format mp3 {link_entry.get()}'  
    os.system(terminal_command)

def download_video(link_entry):
    title.configure(text=link_entry.get(), fg="white")
    terminal_command = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" {link_entry.get()}'  
    os.system(terminal_command)

def download_from_file(file_type, download_func):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            for line in file:
                link_entry.delete(0, tk.END)
                link_entry.insert(0, line.strip())
                download_func(link_entry)

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
audio_button = tk.Button(app, text="Download Audio", command=lambda: download_audio(link_entry))
audio_button.pack(padx=10, pady=10)

# Video button
video_button = tk.Button(app, text="Download Video", command=lambda: download_video(link_entry))
video_button.pack(padx=10, pady=10)

# Audio download from file button
audio_file_button = tk.Button(app, text="Download Audio from File", command=lambda: download_from_file("audio", download_audio))
audio_file_button.pack(padx=10, pady=10)

# Video download from file button
video_file_button = tk.Button(app, text="Download Video from File", command=lambda: download_from_file("video", download_video))
video_file_button.pack(padx=10, pady=10)

app.mainloop()