import os

def download_from_file(file_path):
    if not os.path.isfile(file_path):
        print(f"File '{file_path}' does not exist.")
        return
    else:
        with open(file_path, 'r') as file:
            for line in file:
                link = line.strip()
                download_link(link)

def download_link(link):
    choice = int(input("Choose an option\n1. Download video\n2. Download audio: "))
    if choice == 1:
        terminal_command = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" {link}'
    elif choice == 2:
        terminal_command = f'yt-dlp -x --audio-format mp3 {link}'
    print(terminal_command)  # Print the command
    os.system(terminal_command)

def main():
    choice = int(input("Enter\n1. To download from a text file\n2. To download a link: "))        
    if choice == 1:
        file_path = input("Enter the file which contains the links: ")
        download_from_file(file_path)
    elif choice == 2:
        link = input("Enter the link you want to download: ")
        download_link(link)
main()