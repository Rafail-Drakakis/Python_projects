import os

def download_from_file(file_path):
    if not os.path.isfile(file_path):  # Check if the file exists
        print(f"File '{file_path}' does not exist.")
        return
    else:
        with open(file_path, 'r') as file:
            for line in file:
                link = line.strip()  # Remove any leading/trailing whitespaces from the line
                download_link(link)  # Call the function to download the link

def download_link(link):
    choice = int(input("Choose an option\n1. Download video\n2. Download audio: "))  # Prompt the user to choose an option
    if choice == 1:
        terminal_command = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" {link}'  # Prepare the terminal command to download video
    elif choice == 2:
        terminal_command = f'yt-dlp -x --audio-format mp3 {link}'  # Prepare the terminal command to download audio
    print(terminal_command)  # Print the terminal command for debugging purposes
    os.system(terminal_command)  # Execute the terminal command using os.system()

def main():
    choice = int(input("Enter\n1. To download from a text file\n2. To download a link: "))  # Prompt the user to choose an option
    if choice == 1:
        file_path = input("Enter the file which contains the links: ")  # Prompt the user to enter the file path
        download_from_file(file_path)  # Call the function to download links from the file
    elif choice == 2:
        link = input("Enter the link you want to download: ")  # Prompt the user to enter the link
        download_link(link)  # Call the function to download the link

main()