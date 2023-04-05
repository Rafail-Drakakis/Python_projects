from collatz import collatz_function, collatz_plot
from count_lines import count_lines
from fibonacci import show_fibonacci_range
from get_fact import get_fact
from lotto_numbers import write_combinations_to_file
from timing import time_function_execution
from image_converter import convert_image
from audio_converter import convert_audio
from mp3_downloader import download_video_as_mp3, download_playlist_as_mp3

def main():
    choice = int(input("Enter \n1.To count lines in a file \n2.To write all the lotto numbers in a text file \n3.To get a fact To a number \n4.To print the plot in Fibonacci sequence \n5.To print the plot To collatz function \n6.To convert an image \n7.To convert an audio file \n8.To download videos as mp3: "))
    if choice == 1:
        file_name = input("Enter the file name: ")
        num_lines = count_lines(file_name)
        print(f"Number of lines in the file: {num_lines}")
        time_function_execution(count_lines, file_name)
    elif choice == 2:
        time_function_execution(write_combinations_to_file, "combinations.txt")
    elif choice == 3:
        number = int(input("Enter a number: "))
        time_function_execution(get_fact, number)
    elif choice == 4:
        last = int(input("Give the last number of the range: "))
        time_function_execution(show_fibonacci_range, 2, last + 1)
    elif choice == 5:
        number = int(input("Give a number: "))
        sequence, count = collatz_function(number)
        collatz_plot(sequence, number)
        time_function_execution(collatz_function, number)
    elif choice == 6:
        input_path = input("Enter the file path To the input image: ")
        output_path = input("Enter the file path To the output image: ")
        time_function_execution(convert_image, input_path, output_path)
    elif choice == 7:
        input_path = input("Enter the file path To the input audio file: ")
        output_path = input("Enter the file path To the output audio file: ")
        time_function_execution(convert_audio, input_path, output_path)
    elif choice == 8:
        video_or_playlist = int(input('Enter \n1.To download a single video or \n2.To download a playlist: '))
        if video_or_playlist == 1:
            url = input('Enter the URL of the video: ')
            time_function_execution(download_video_as_mp3, url)
        elif video_or_playlist == 2:
            filename = input('Enter the name of the file containing the URLs: ')
            time_function_execution(download_playlist_as_mp3, filename)
        else:
            print ("Invalid input!")
    else:
        print("Invalid input")
main()
