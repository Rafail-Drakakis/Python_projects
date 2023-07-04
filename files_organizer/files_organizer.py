import os
import shutil
import tkinter as tk
from tkinter import filedialog

def files_organizer():
    """
    The `files_organizer` function organizes files in the selected directory by moving them into
    folders based on their file extensions.
    """
    # Prompt the user to select a directory
    directory = filedialog.askdirectory()

    if not directory:
        return  # No directory selected, exit the function

    # Get all files in the directory
    files = os.listdir(directory)

    # Create a dictionary to hold the file extensions and their corresponding folders
    file_types = {}

    # Loop through each file and organize them by extension
    for file in files:
        # Exclude the files_organizer.py file from being moved (assuming it's the file which contains the code)
        if file == "files_organizer.py":
            continue

        # Get the file extension
        file_extension = os.path.splitext(file)[1]

        # If the file extension doesn't exist in the dictionary, create a new folder for it
        if file_extension not in file_types:
            folder_name = file_extension.replace(".", "")
            folder_path = os.path.join(directory, folder_name)

            # Check if the folder already exists
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            file_types[file_extension] = folder_name

        # Move the file to the corresponding folder
        src_path = os.path.join(directory, file)
        dst_path = os.path.join(directory, file_types[file_extension], file)
        shutil.move(src_path, dst_path)

    # Show a message box indicating the files have been organized
    tk.messagebox.showinfo("Files Organized", "Files have been organized successfully!")

# Create the main GUI window
window = tk.Tk()
window.title("Files Organizer")
window.geometry("300x200")

# Create a button to trigger the files_organizer function
organize_button = tk.Button(window, text="Organize Files", command=files_organizer)
organize_button.pack(pady=10)

# Run the GUI main loop
window.mainloop()