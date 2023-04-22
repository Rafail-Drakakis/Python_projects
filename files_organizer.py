import os
import shutil

# Get the current working directory
directory = os.getcwd()

# Get all files in the directory
files = os.listdir(directory)

# Create a dictionary to hold the file extensions and their corresponding folders
file_types = {}

# Loop through each file and organize them by extension
for file in files:
    # Exclude the file_organizer.py file from being moved
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

print("Files have been organized!")
