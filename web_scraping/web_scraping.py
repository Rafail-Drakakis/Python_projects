import time, sys, os, re
import urllib, urllib3
import urllib.parse, urllib.request
import warnings, glob, requests
import bs4, docx
import pdf2docx, pdf2image, PyPDF2
import os, zipfile, tarfile, gzip

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#site_downloader.py
def collect_pdf_filenames(directory):
    pdf_files = glob.glob(os.path.join(directory, '*.pdf'))
    file = open('pdf_filenames.txt', 'w')
    file.write('\n'.join(pdf_files))
    file.close()
    return file

def merge_pdfs(output_filename):
    pdf_directory = os.path.join(os.getcwd(), 'downloads')
    text_file = 'pdf_filenames.txt'
    merged_pdf = output_filename
    filenames = []

    with open(text_file, 'r') as file:
        filenames = file.read().splitlines()

    merger = PyPDF2.PdfMerger()
    for filename in filenames:
        merger.append(filename)
    merger.write(output_filename)
    merger.close()

    print("PDF merging complete!")

def download_files_from_website(url):
    response = requests.get(url, verify=False)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    a_tags = soup.find_all('a')
    save_dir = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for tag in a_tags:
        file_url = urllib.parse.urljoin(url, tag['href'])
        file_name = os.path.join(save_dir, file_url.split('/')[-1])
        if '.' in file_name and file_url != url:
            file_response = requests.get(file_url, allow_redirects=True, verify=False)
            if file_response.status_code == 200:
                with open(file_name, 'wb') as file:
                    file.write(file_response.content)

#scrape.py
def scrape_text_to_file(url, filename):
    response = requests.get(url)
    if response.status_code != 200:
        print('Error: Failed to get the web page')
        sys.exit(1)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
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
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
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

def clean_up_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Delete files with .html extension
            if file.endswith(".html"):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

            # Unzip files with supported extensions
            elif file.endswith((".zip", ".tgz", ".gz")):
                if file.endswith(".zip"):
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(root)
                elif file.endswith((".tgz", ".tar.gz")):
                    try:
                        with tarfile.open(file_path, 'r:gz') as tar_ref:
                            tar_ref.extractall(root)
                    except tarfile.ReadError:
                        print(f"Skipping file: {file_path} (Not a valid tar file)")
                        continue
                elif file.endswith(".gz"):
                    new_file_path = file_path[:-3]  # Remove .gz extension
                    try:
                        with gzip.open(file_path, 'rb') as gzip_ref:
                            with open(new_file_path, 'wb') as output_file:
                                output_file.write(gzip_ref.read())
                    except (gzip.BadGzipFile, OSError):
                        print(f"Skipping file: {file_path} (Not a valid gzip file)")
                        continue

                os.remove(file_path)
                print(f"Unzipped and deleted file: {file_path}")

#main.py
def web_scraping():
    print("=== Web Scraping Menu ===")
    print("1. Scrape data from a website")
    print("2. Download files from a website")
    
    choice = int(input("Enter your choice: "))
    url = input("Enter the URL: ")

    if choice == 1:
        filename = input("Enter the filename: ")
        scrape_text_to_file(url, filename)
        images_true = input("Do you want to include the images? ")
        if images_true == 'yes':
            scrape_image_to_file(url, filename)
        print(f'The {filename} folder has been successfully created.')
    elif choice == 2:
        download_files_from_website(url)
        collect_pdf_filenames(os.path.join(os.getcwd(), 'downloads'))
        merge_pdfs("merged.pdf")
        clean_up_folder(os.path.join(os.getcwd(), 'downloads'))

web_scraping()