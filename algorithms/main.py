from audio_converter import convert_audio_menu
from count_lines import count_lines_menu
from get_fact import get_fact
from collatz_fibonacci.py import collatz_fibonacci_menu
from words import words
from image_module import image_processing_menu
from mp3_downloader import download_video_menu

def main():
    choice = int(input("Enter \n1.To convert an audio file  \n2.To count lines in a file \n3.To get a fact for a number \n4.To print the plot in Fibonacci sequence \n5.To print the plot for collatz function  \n6.To count all the words in a file \n7.To perform operations in an image \n8.To download videos as mp3: "))
    if choice == 1:
        convert_audio_menu()
    elif choice == 2:
        count_lines_menu()
    elif choice == 3:
        get_fact()
    elif choice == 5:
        collatz_fibonacci_menu()
    elif choice == 6:
    	words()
    elif choice == 7:
        image_processing_menu()
    elif choice == 8:
        download_video_menu()
    else:
        print("Invalid input")
main()
