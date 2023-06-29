import os, glob, moviepy.editor

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
        except FileNotFoundError as e:
            print(f"File not found: {file}")
        except moviepy.editor.VideoFileClipException as e:
            print(f"Error processing video file: {file} - {str(e)}")
        except moviepy.editor.AudioFileClipException as e:
            print(f"Error processing audio file: {file} - {str(e)}")

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

# Main function
def main():
    # Prompt the user to choose an option
    choice = int(input("Choose an option:\n1. Enter filenames directly\n2. Specify a file to read filenames from\n"))

    if choice == 1:
        # Prompt the user to enter filenames directly
        files = [file.strip() for file in input("Enter the file names to merge (separated by commas): ").split(",")]
    elif choice == 2:
        all_files = input("Do you want to include all files in this directory with a specified extension (yes/no)? ")

        if all_files.lower() == "yes":
            # Prompt the user to enter a file extension and collect filenames from the directory
            extension = input("Enter the file extension (e.g., mp4, mp3, wav): ")
            files = collect_filenames(extension)
        else:
            # Prompt the user to enter a filename containing the files
            filename = input("Enter the filename which contains the files: ")
            files = get_filenames_from_file(filename)

    if os.path.exists("filenames.txt"):
        os.remove("filenames.txt")

    if files:
        # Prompt the user to enter the output file name and merge the files
        output_filename = input("Enter the output file name: ")
        merge_video_or_audio_files(files, output_filename)
    else:
        print("No files to merge.")
        exit(0)

main()