import time
import sys
import os
import re
import docx
import requests
from bs4 import BeautifulSoup
import urllib.request

# Function to print the elapsed time
def print_elapsed_time(start_time):
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)
    print(f"Elapsed time: {elapsed_time} seconds")

#scrape.py
def scrape_text_to_file(url, filename):
    response = requests.get(url)
    if response.status_code != 200:
        print('Error: Failed to get the web page')
        sys.exit(1)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_text = soup.get_text(separator='\n')
    if not main_text:
        print('Error: Failed to extract the main text')
        sys.exit(1)
    main_text = replace_chars(main_text)
    os.makedirs(filename, exist_ok=True)
    with open(f"{filename}/{filename}.txt", 'w', encoding='utf-8') as f:
        f.write(main_text)
    clean_text_file(f"{filename}/{filename}.txt")

def scrape_image_to_file(url, filename):
    response = requests.get(url)
    if response.status_code != 200:
        print('Error: Failed to get the web page')
        sys.exit(1)
    soup = BeautifulSoup(response.content, 'html.parser')
    os.makedirs(filename, exist_ok=True)
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if not img_url:
            continue
        try:
            img_name = img_url.split('/')[-1]
            img_name = img_name.split('.')[0] + '.jpg'
            img_path = os.path.join(filename, img_name)
            urllib.request.urlretrieve(img_url, img_path)
        except Exception as e:
            print(f'Error downloading {img_url}: {str(e)}')

#clean.py
def replace_chars(text):
    chars_to_replace = [f"[{i}]" for i in range(1, 100)]
    for char in chars_to_replace:
        text = text.replace(char, ' ')
    text = text.replace('\t', '   ')  # Replace tab with three spaces
    return text

def clean_text_file(filename):
    if not os.path.isfile(filename):
        print(f'Error: {filename} does not exist')
        sys.exit(1)
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    # Replace multiple consecutive new lines with a single new line and add three spaces instead of new line
    text = re.sub(r'\n+', '   ', text.strip())
    # Replace 3 or more spaces with 2 spaces
    text = re.sub(r' {3,}', '  ', text)
    doc = docx.Document()
    doc.add_paragraph(text, style='Normal')
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = docx.shared.Pt(12)
    doc_file_name = os.path.splitext(filename)[0] + '.docx'
    doc.save(doc_file_name)
    os.remove(filename)

def web_scraping():
    # Ask the user for the URL and filename input
    url = input("Enter the URL: ")
    filename = input("Enter the filename: ")
    start_time = time.time() # Start the timer
    scrape_text_to_file(url, filename)
    choice = input("Do you want to include the images? (yes/no) ")
    if choice == 'yes':
        scrape_image_to_file(url, filename)
    print(f'The {filename} folder has been successfully created.')
    print_elapsed_time(start_time) # Print the elapsed time

web_scraping()