import tkinter as tk, subprocess, yt_dlp
from tkinter import messagebox, filedialog

def validate_link(link):
    try:
        ydl = yt_dlp.YoutubeDL()
        ydl.extract_info(link, download=False)
        return True
    except yt_dlp.DownloadError:
        return False

def download_audio(link_entry, is_one):
    link = link_entry.get()
    if validate_link(link):
        terminal_command = f'yt-dlp -x --audio-format mp3 {link}'
        subprocess.run(terminal_command, shell=True)
        if is_one == 1:
            messagebox.showinfo("Download Complete", "File has been downloaded.")
    else:
        messagebox.showerror("Invalid Link", "Please enter a valid YouTube link.")

def download_video(link_entry, is_one):
    link = link_entry.get()
    if validate_link(link):
        terminal_command = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" {link}'
        subprocess.run(terminal_command, shell=True)
        if is_one == 1:
            messagebox.showinfo("Download Complete", "File has been downloaded.")
    else:
        messagebox.showerror("Invalid Link", "Please enter a valid YouTube link.")

def download_from_file(download_func, is_one):
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