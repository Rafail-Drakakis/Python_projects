import os
import glob
import speech_recognition as sr
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips

def merge_video_or_audio_files(files, output_filename):
    """
    The function `merge_video_or_audio_files` takes a list of video or audio files, checks their
    extensions, creates appropriate clips, concatenates them, and saves the merged file with the
    specified output filename.
    
    :param files: A list of file paths to the video or audio files that you want to merge
    :param output_filename: The output_filename parameter is a string that specifies the name of the
    merged video or audio file that will be created
    """
    clips = []
    
    for file in files:
        try:
            if file.lower().endswith(('.mp4', '.mkv', '.avi')):
                clip = moviepy.editor.VideoFileClip(file)
            elif file.lower().endswith(('.mp3', '.wav')):
                clip = moviepy.editor.AudioFileClip(file)
            else:
                print(f"Skipping unsupported file: {file}")
                continue
            
            clips.append(clip)
        
        except (FileNotFoundError, moviepy.editor.VideoFileClipException, moviepy.editor.AudioFileClipException) as e:
            print(f"Error processing file: {file} - {str(e)}")

    if clips:
        if isinstance(clips[0], moviepy.editor.VideoFileClip):
            try:
                final_clip = moviepy.editor.concatenate_videoclips(clips, method='compose')
                final_clip.write_videofile(output_filename)
                print(f"Merged files saved as {output_filename}")
            except Exception as e:
                print(f"Error writing video file: {str(e)}")
        
        elif isinstance(clips[0], moviepy.editor.AudioFileClip):
            try:
                final_clip = moviepy.editor.concatenate_audioclips(clips)
                final_clip.write_audiofile(output_filename)
                print(f"Merged files saved as {output_filename}")
            except Exception as e:
                print(f"Error writing audio file: {str(e)}")
    
    else:
        print("No supported files to merge.")

def get_filenames_from_file(filename):
    """
    The function `get_filenames_from_file` reads the contents of a file and returns a list of filenames,
    with each filename on a separate line.
    
    :param filename: The filename parameter is a string that represents the name of the file from which
    you want to retrieve the filenames
    :return: The function `get_filenames_from_file` returns a list of filenames read from the specified
    file. If the file is not found, it prints an error message and returns an empty list.
    """
    try:
        with open(filename, 'r') as file:
            return file.read().splitlines()
    
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []

def collect_filenames(extension):
    """
    The function `collect_filenames` collects filenames with a specific extension, prompts the user for
    confirmation to proceed with merging the files, and writes the filenames to a text file.
    
    :param extension: The `extension` parameter is a string that represents the file extension of the
    files you want to collect. For example, if you want to collect all files with the extension ".txt",
    you would pass "txt" as the value for the `extension` parameter
    :return: The function `collect_filenames` returns the list of filenames obtained from the file
    "filenames.txt" using the `get_filenames_from_file` function.
    """
    files = glob.glob(os.path.join(os.getcwd(), f'*{extension}'))
    
    if files:
        print("Collected files:")
        for file in files:
            print(file)
        
        confirm = input("Do you want to proceed with these files (yes/no)? ")
        
        if confirm.lower() != "yes":
            print("Operation canceled.")
            exit(0)
    else:
        print(f"No files with extension {extension} found.")
        exit(0)

    with open('filenames.txt', 'w') as file:
        file.write('\n'.join(files))
    
    return get_filenames_from_file("filenames.txt")

def convert_video_to_text(input_filenames, read_from_file=False):
    """
    The function `convert_video_to_text` takes a list of input filenames, converts video or audio files
    to text using speech recognition, and saves the transcriptions to text files.
    
    :param input_filenames: The `input_filenames` parameter is a list of filenames of the videos or
    audio files that you want to convert to text. Each filename should be a string
    :param read_from_file: The `read_from_file` parameter is a boolean flag that determines whether or
    not to remove the original file(s) after converting them to text. If `read_from_file` is set to
    `True`, the user will be prompted to confirm whether they want to remove the original file(s) after
    conversion, defaults to False (optional)
    """
    for filename in input_filenames:
        if filename.lower().endswith(('.mp4', '.mkv', '.avi', '.mp3', '.wav')):
            if filename.lower().endswith(('.mp4', '.mkv', '.avi')):
                video = VideoFileClip(filename)
                audio = video.audio
            else:
                audio = AudioFileClip(filename)

            audio.write_audiofile("temp.wav", codec='pcm_s16le')

            recognizer = sr.Recognizer()

            with sr.AudioFile("temp.wav") as audio_file:
                audio = recognizer.record(audio_file)

            text = recognizer.recognize_google(audio)

            output_file_path = os.path.splitext(filename)[0] + ".txt"
            
            with open(output_file_path, "w") as output_file:
                output_file.write(text)

            os.remove("temp.wav")

            if read_from_file:
                remove = input(f"Do you want to remove the original file '{filename}' (yes/no)? ")
                
                if remove == "yes":
                    os.remove(filename)
        else:
            print(f"Skipping unsupported file: {filename}")

    if not read_from_file:
        remove = input("Do you want to remove the original file(s) (yes/no)? ")
        
        if remove == "yes":
            for file in input_filenames:
                os.remove(file)

def merge_files_by_extension(merged_file_name, extension):
    """
    The function `merge_files_by_extension` merges all files with a given extension into a single file.
    
    :param merged_file_name: The name of the merged file that will be created. This should be a string
    without the file extension
    :param extension: The "extension" parameter is a string that represents the file extension you want
    to merge. For example, if you want to merge all files with the extension ".txt", you would pass
    ".txt" as the value for the "extension" parameter
    :return: the name of the merged file.
    """
    merged_file = merged_file_name + extension
    files = [file for file in os.listdir() if file.endswith(extension)]

    with open(merged_file, "w") as merged_file_obj:
        for file_name in files:
            if file_name != merged_file:
                with open(file_name, "r") as file:
                    merged_file_obj.write("// " + file_name + "\n")
                    merged_file_obj.write(file.read())
                    merged_file_obj.write("\n\n")

    return merged_file

# Menu functions
def merge_menu():
    """
    The `merge_menu` function allows the user to choose different options for merging files, including
    entering filenames directly, specifying a file to read filenames from, or including all files in a
    directory with a specified extension.
    """
    choice = int(input("Choose an option:\n1. Enter filenames directly\n2. Specify a file to read filenames from\n3. To include all files in this directory with a specified extension: "))

    if choice == 1:
        files = [file.strip() for file in input("Enter the file names to merge (separated by commas): ").split(",")]
    elif choice == 2:
        filename = input("Enter the filename which contains the files: ")
        files = get_filenames_from_file(filename)
    elif choice == 3:
        extension = input("Enter the file extension (e.g., mp4, mp3, wav): ")
        files = collect_filenames(extension)
        os.remove("filenames.txt")

    if files:
        output_filename = input("Enter the output file name: ")
        merge_video_or_audio_files(files, output_filename)
    else:
        print("No files to merge.")
        exit(0)
        
def convert_menu():
    """
    The `convert_menu` function allows the user to choose between collecting filenames from the current
    directory or entering them manually, converts video files to text, merges the resulting text files,
    and optionally removes the individual text files after merging.
    """
    choice = int(input("Enter \n1 to convert all the files in the current directory\n2 to enter filenames manually: "))
    
    if choice == 1:
        extension = input("Enter the extension you want: ")
        filenames = collect_filenames(extension)
    elif choice == 2:
        filenames = input("Enter the filenames (separated by commas): ").split(",")
    else:
        print("Invalid choice.")
        exit(0)

    convert_video_to_text(filenames)
    merged_file = merge_files_by_extension("merged", ".txt")

    remove_txt_files = input("Do you want to remove the text files after merging (yes/no)? ")
        
    if remove_txt_files.lower() == "yes":
        for file in os.listdir():
            if file.endswith(".txt") and file != merged_file:
                os.remove(file)

def get_user_input():
    try:
        choice = int(input("Menu:\n1. To merge audio/video\n2. To convert audio/video to text: "))
        if choice not in [1, 2]:
            print("Invalid choice. Please enter 1 or 2")
            return None
        return choice
    except ValueError:
        print("Invalid choice. Please enter 1 or 2")
        return None
    

def main():
    """
    The main function allows the user to either merge video/audio files or convert them to text, based
    on their choice.
    """
    choice = get_user_input()
    if choice is not None:
        if choice == 1:
            merge_menu()
        elif choice == 2:
            convert_menu()
 
if __name__ == "__main__":
    main()