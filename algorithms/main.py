from converter import converter_menu
from count_text import count_text_men
from collatz_fibonacci import collatz_fibonacci_menu
from image_module import image_processing_menu
from mp3_downloader import download_mp3_menu

def main():
    choice = int(input("Enter \n1.To convert files to other formats  \n2.To count lines or unique words in a file \n3.To Generate a sequence \n4.To perform operations in an image \n5.To download videos as mp3: "))
    if choice == 1:
        converter_menu()
    elif choice == 2:
        count_text_menu()
    elif choice == 3:
        collatz_fibonacci_menu()
    elif choice == 4:
        image_processing_menu()
    elif choice == 5:
        download_mp3_menu()
    else:
        print("Invalid input")
main()
