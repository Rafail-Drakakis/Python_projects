# README
Author: Rafail Drakakis
File name: web_scraping.py

This program is designed to scrape text and images from a given URL and save them to a file. It utilizes the `requests` library for making HTTP requests, `BeautifulSoup` for parsing HTML content, and `docx` for creating a Word document.

## Prerequisites
- Python 3.x
- Required Python libraries: time, sys, os, re, docx, requests, urllib.request, bs4

## Installation
Clone or download the repository to your local machine.

## Usage
1. Open a terminal or command prompt.
2. Navigate to the directory where the program files are located.
3. Run the program using the following command: python web_scraping.py
4. Enter the URL from which you want to scrape text and images when prompted.
5. Enter the desired filename for the output files when prompted.
6. The program will start scraping the text content from the given URL and save it to a text file in a folder with the specified filename.
7. You will be asked whether you want to include the images in the scraping process. Enter 'yes' or 'no' accordingly.
   - If you choose 'yes', the program will scrape the images from the URL and save them to the same folder.
   - If you choose 'no', the program will only scrape the text content.
8. Once the scraping process is complete, a folder with the specified filename will be created, containing the text file and, if applicable, the downloaded images.
9. The elapsed time for the scraping process will be displayed.

## Notes
- If the program encounters any errors during the scraping process (e.g., failed to retrieve the web page or extract the main text), it will display an error message and exit.
- The extracted text will be cleaned and formatted to remove unwanted characters and ensure readability.
- The final output for the text will be a Word document (.docx) instead of a plain text file for better formatting options.

## License
This program is open source and distributed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to modify and use it according to your needs.

## Disclaimer
This program is provided as-is without any warranty. The author is not responsible for any misuse or damage caused by the program. Use it at your own risk.