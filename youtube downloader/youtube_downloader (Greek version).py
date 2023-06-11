import os

def download_from_file(file_path):
    if not os.path.isfile(file_path):  # Check if the file exists
        print(f"File '{file_path}' does not exist.")
        return
    else:
        with open(file_path, 'r') as file:
            for line in file:
                download_link(link)  # Call the function to download the link

def download_link(link):
    choice = int(input("Επιλέξτε\n1. Για βίντεο\n2. Για ήχο: "))  # Prompt the user to choose an option
    if choice == 1:
        terminal_command = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" {link}'  # Prepare the terminal command to download video
    elif choice == 2:
        terminal_command = f'yt-dlp -x --audio-format mp3 {link}'  # Prepare the terminal command to download audio
    print(terminal_command)  # Print the terminal command for debugging purposes
    os.system(terminal_command)  # Execute the terminal command using os.system()

link = input("Πληκτρολογήστε τον σύνδεσμο που επιθυμείτε να κατεβάσετε: ")  # Prompt the user to enter the link
download_link(link)  # Call the function to download the link