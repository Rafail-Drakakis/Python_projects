import urllib.request
import sys
import requests
import os
from bs4 import BeautifulSoup
from clean import replace_chars, clean_text_file

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

