import time
import sys
from scrape import scrape_text_to_file, scrape_image_to_file
from timing import print_elapsed_time

def main():
    # Ask the user for the URL and filename input
    url = input("Enter the URL: ")
    filename = input("Enter the filename: ")
    try:
        start_time = time.time() # Start the timer
        scrape_text_to_file(url, filename)
        choice = input("Do you want to include the images? (yes/no) ")
        if choice == 'yes':
            scrape_image_to_file(url, filename)
        print(f'The {filename} folder has been successfully created.')
        print_elapsed_time(start_time) # Print the elapsed time
    except Exception as e:
        print(f'Error: {str(e)}')
        sys.exit(1)

main()
