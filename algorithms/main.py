from converter import converter_menu
from count_text import count_text_menu
from get_fact import get_fact
from collatz_fibonacci import collatz_fibonacci_menu
from image_module import image_processing_menu
from mp3_downloader import download_video_menu

def main():
    choice = int(input("Enter \n1.To convert files to other formats  \n2.To count lines or unique words in a file \n3.To get a fact for a number \n4.To Generate a sequence \n5.To perform operations in an image \n6.To download videos as mp3: "))
    if choice == 1:
        converter_menu()
    elif choice == 2:
        count_text_menu()
    elif choice == 3:
        get_fact()
    elif choice == 4:
        collatz_fibonacci_menu()
    elif choice == 5:
        image_processing_menu()
    elif choice == 6:
        download_video_menu()
    else:
        print("Invalid input")
main()
