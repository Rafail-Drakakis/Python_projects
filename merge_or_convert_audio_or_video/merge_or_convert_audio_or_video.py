import os, glob, moviepy.editor, speech_recognition as sr
from moviepy.editor import VideoFileClip, AudioFileClip

# Function to merge video or audio files
def merge_video_or_audio_files(files, output_filename):
    clips = []
    for file in files:
        try:
            # Check the file extension and create appropriate clips
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
                # Concatenate video clips and write the final merged video file
                final_clip = moviepy.editor.concatenate_videoclips(clips, method='compose')
                final_clip.write_videofile(output_filename)
                print(f"Merged files saved as {output_filename}")
            except Exception as e:
                print(f"Error writing video file: {str(e)}")
        elif isinstance(clips[0], moviepy.editor.AudioFileClip):
            try:
                # Concatenate audio clips and write the final merged audio file
                final_clip = moviepy.editor.concatenate_audioclips(clips)
                final_clip.write_audiofile(output_filename)
                print(f"Merged files saved as {output_filename}")
            except Exception as e:
                print(f"Error writing audio file: {str(e)}")
    else:
        print("No supported files to merge.")

# Function to read filenames from a file
def get_filenames_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []

# Function to collect filenames with a specified extension from the current directory
def collect_filenames(extension):
    files = glob.glob(os.path.join(os.getcwd(), f'*.{extension}'))
    if files:
        print("Collected files:")
        for file in files:
            print(file)
        confirm = input("Do you want to proceed with merging these files (yes/no)? ")
        if confirm.lower() != "yes":
            print("Merge operation canceled.")
            exit(0)
    else:
        print(f"No files with extension {extension} found.")
        exit(0)

    with open('filenames.txt', 'w') as file:
        file.write('\n'.join(files))
    return get_filenames_from_file("filenames.txt")

# Function to convert video files to text
def convert_video_to_text(input_filenames, read_from_file=False):
    for filename in input_filenames:
        if filename.lower().endswith(('.mp4', '.mkv', '.avi', '.mp3', '.wav')):
            if filename.lower().endswith(('.mp4', '.mkv', '.avi')):
                # Convert video to audio
                video = VideoFileClip(filename)
                audio = video.audio
            else:
                # Use the audio file directly
                audio = AudioFileClip(filename)

            # Save audio to a temporary file
            audio.write_audiofile("temp.wav", codec='pcm_s16le')

            # Convert audio to text
            recognizer = sr.Recognizer()

            with sr.AudioFile("temp.wav") as audio_file:
                audio = recognizer.record(audio_file)

            text = recognizer.recognize_google(audio)

            # Save the transcriptions to a text file
            output_file_path = os.path.splitext(filename)[0] + ".txt"
            with open(output_file_path, "w") as output_file:
                output_file.write(text)

            # Clean up temporary file
            os.remove("temp.wav")

            if not read_from_file:
                remove = input(f"Do you want to remove the original file '{filename}' (yes/no)? ")
                if remove == "yes":
                    os.remove(filename)
        else:
            print(f"Skipping unsupported file: {filename}")

    if read_from_file:
        remove = input("Do you want to remove the original file(s) (yes/no)? ")
        if remove == "yes":
            for file in input_filenames:
                os.remove(file)

# Function to merge text files by extension
def merge_files_by_extension(merged_file_name, extension):
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

# Main function
def main():
    merge_or_convert = int(input("1. To merge video/audio\n2. To convert it to text: "))
    if merge_or_convert == 1:
        choice = int(input("Choose an option:\n1. Enter filenames directly\n2. Specify a file to read filenames from\n3. To include all files in this directory with a specified extension: "))

        if choice == 1:
            # Prompt the user to enter filenames directly
            files = [file.strip() for file in input("Enter the file names to merge (separated by commas): ").split(",")]
        elif choice == 2:
            # Prompt the user to enter a filename containing the files
            filename = input("Enter the filename which contains the files: ")
            files = get_filenames_from_file(filename)
        elif choice == 3:
            extension = input("Enter the file extension (e.g., mp4, mp3, wav): ")
            files = collect_filenames(extension)
            os.remove("filenames.txt")

        if files:
            # Prompt the user to enter the output file name and merge the files
            output_filename = input("Enter the output file name: ")
            merge_video_or_audio_files(files, output_filename)
        else:
            print("No files to merge.")
            exit(0)
    
    elif merge_or_convert == 2:
        choice = int(input("Enter \n1 to collect filenames from the current directory\n2 to enter filenames manually: "))
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

main()