import os

def download_from_file(file_path):
    """
    The function `download_from_file` reads a file line by line and calls another function to download
    each line as a link.
    
    :param file_path: The file path is the location of the file that contains the download links. It
    should be a string that specifies the path to the file, including the file name and extension. For
    example, "C:/Downloads/links.txt" or "/home/user/links.txt"
    :return: nothing (None) if the file does not exist.
    """
    if not os.path.isfile(file_path):  # Check if the file exists
        print(f"File '{file_path}' does not exist.")
        return
    else:
        with open(file_path, 'r') as file:
            for line in file:
                download_link(line)  # Call the function to download the link

def download_link(link):
    """
    The function `download_link` prompts the user to choose between downloading a video or audio file
    from a given link, and then executes the corresponding terminal command to download the file using
    `os.system()`.
    
    :param link: The link parameter is the URL of the video or audio file that you want to download
    """
    choice = int(input("Choose an option\n1. Download video\n2. Download audio: "))  # Prompt the user to choose an option
    if choice == 1:
        terminal_command = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]" {link}'  # Prepare the terminal command to download video
    elif choice == 2:
        terminal_command = f'yt-dlp -x --audio-format mp3 {link}'  # Prepare the terminal command to download audio
    print(terminal_command)  # Print the terminal command for debugging purposes
    os.system(terminal_command)  # Execute the terminal command using os.system()

def main():
    """
    The main function prompts the user to choose between downloading links from a text file or a single
    link, and calls the appropriate function based on the user's choice.
    """
    choice = int(input("Enter\n1. To download from a text file\n2. To download a link: "))  # Prompt the user to choose an option
    if choice == 1:
        file_path = input("Enter the file which contains the links: ")  # Prompt the user to enter the file path
        download_from_file(file_path)  # Call the function to download links from the file
    elif choice == 2:
        link = input("Enter the link you want to download: ")  # Prompt the user to enter the link
        download_link(link)  # Call the function to download the link

main()