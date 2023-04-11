This repository contains a collection of Python scripts for scraping web content and converting it to different file formats.

Files
scrape.py: Contains two functions scrape_text_to_file and scrape_image_to_file for scraping text and images from a web page and saving them to a file.
clean.py: Contains two functions replace_chars and clean_text_file for cleaning text files and saving the cleaned text to a Word document.
timing.py: Contains a single function print_elapsed_time for measuring elapsed time in a Python program.
main.py: The main Python script that prompts the user for a URL and filename, and uses the functions from scrape.py, clean.py, and timing.py to scrape the web page, clean the text, and save the content to a Word document and image files.

Libraries
This program uses the following Python libraries:
1.requests: Used for making HTTP requests to web pages.
2.beautifulsoup4: Used for parsing HTML content and extracting data from web pages.
3.python-docx: Used for creating Word documents from text files.
4.time: Used for measuring elapsed time in the program.

To install them, type the following command in the terminal:
pip install requests beautifulsoup4 python-docx time

Usage
To use this program, follow these steps:
Clone or download this repository to your local machine.
Open a terminal or command prompt and navigate to the directory where you downloaded the files.
Run the main.py script using the command python main.py.
Enter the URL of the web page you want to scrape and the desired filename when prompted.
Wait for the program to complete. The elapsed time will be displayed when the program finishes.
Check the output directory for the cleaned text file, Word document, and image files.

License
This project is licensed under the MIT License.
