from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips

def merge_video_or_audio_files(files, output_filename):
    clips = []
    for file in files:
        try:
            if file.endswith('.mp4') or file.endswith('.mkv') or file.endswith('.avi'):
                clip = VideoFileClip(file)
            elif file.endswith('.mp3') or file.endswith('.wav'):
                clip = AudioFileClip(file)
            else:
                print(f"Skipping unsupported file: {file}")
                continue
            clips.append(clip)
        except Exception as e:
            print(f"Error processing file: {file} - {str(e)}")

    if clips:
        if isinstance(clips[0], VideoFileClip):
            try:
                final_clip = concatenate_videoclips(clips, method='compose')
                final_clip.write_videofile(output_filename)
                print(f"Merged files saved as {output_filename}")
            except Exception as e:
                print(f"Error writing video file: {str(e)}")
        elif isinstance(clips[0], AudioFileClip):
            try:
                final_clip = concatenate_audioclips(clips)
                final_clip.write_audiofile(output_filename)
                print(f"Merged files saved as {output_filename}")
            except Exception as e:
                print(f"Error writing audio file: {str(e)}")
    else:
        print("No supported files to merge.")

def get_filenames_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None

def main():
    choice = int(input("Choose an option:\n1. Enter filenames directly\n2. Specify a file to read filenames from\n"))
    
    if choice < 1 or choice > 2:
        print("Incorrect choice")
        exit(1)
        
    if choice == 1:
        files = input("Enter the file names to merge (separated by commas): ").split(",")
    elif choice == 2:
        filename = input("Enter the filename: ")
        files = get_filenames_from_file(filename)
    
    if files:
        output_filename = input("Enter the output file name: ")
        merge_video_or_audio_files(files, output_filename)
    else:
        print("No files to merge.")
        exit(1)

main()