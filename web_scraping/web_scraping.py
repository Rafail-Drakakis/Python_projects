import sys, os, re
import urllib, urllib3
import warnings, shutil, requests
import bs4, docx, PyPDF2
import zipfile, tarfile, gzip

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#site_downloader.py
def collect_filenames(directory, filetype):
    file_list = [file for root, dirs, files in os.walk(directory) for file in files if file.endswith(filetype)]
    sorted_file_list = sorted(set(file_list)) # sort the files to appear correctly
    with open('file_list.txt', 'w') as output_file:
        for file in sorted_file_list:
            output_file.write(file + '\n')

def merge_pdfs(output_filename, folder_name):
    pdf_directory = os.path.join(os.getcwd(), folder_name)
    filenames = []

    with open('file_list.txt', 'r') as file:
        filenames = file.read().splitlines()

    merger = PyPDF2.PdfMerger()
    for filename in filenames:
        filepath = os.path.join(pdf_directory, filename)
        if os.path.isfile(filepath):
            merger.append(filepath)
        else:
            print(f"Warning: File not found - {filepath}")

    if merger.pages:
        merger.write(output_filename)
        merger.close()
    else:
        print("No PDF files found for merging.")

def fetch_and_store_files(url, folder_name):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    response = requests.get(url, verify=False)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    a_tags = soup.find_all('a')
    save_dir = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for tag in a_tags:
        if 'href' in tag.attrs:
            file_url = urllib.parse.urljoin(url, tag['href'])
            file_name = os.path.join(save_dir, file_url.split('/')[-1])
            if '.' in file_name and file_url != url and file_url.startswith(("http://", "https://")):
                file_response = requests.get(file_url, allow_redirects=True, verify=False)
                successful_response = 200
                if file_response.status_code == successful_response:
                    with open(file_name, 'wb') as file:
                        file.write(file_response.content)

#clean_folder.py
def clean_up_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Delete files with .html and .php extensions
            if file.endswith((".html", ".php")):
                os.remove(file_path)

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

#organize_files.py
def organize_files(directory):
    # Get all files in the directory
    files = os.listdir(directory)

    # Create a dictionary to hold the file extensions and their corresponding folders
    file_types = {}

    # Loop through each file and organize them by extension
    for file in files:
        # Exclude the target file from being moved
        if file == "merged.pdf":
            continue
        
        # Get the file extension
        file_extension = os.path.splitext(file)[1]

        # If the file extension doesn't exist in the dictionary, create a new folder for it
        if file_extension not in file_types:
            folder_name = file_extension.replace(".", "")
            folder_path = os.path.join(directory, folder_name)
            
            # Check if the folder already exists
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
            
            file_types[file_extension] = folder_name

        # Move the file to the corresponding folder
        src_path = os.path.join(directory, file)
        dst_path = os.path.join(directory, file_types[file_extension], file)
        shutil.move(src_path, dst_path)
    
#scrape_data.py
def get_page(url):
    response = requests.get(url)
    successful_response = 200
    if response.status_code != successful_response:
        print('Error: Failed to get the web page')
        sys.exit(1)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    return soup
    
def scrape_text(url, folder_name):
    soup = get_page(url)
    main_text = soup.get_text(separator='\n')
    if not main_text:
        print('Error: Failed to extract the main text')
        sys.exit(1)
    main_text = replace_chars(main_text)
    os.makedirs(folder_name, exist_ok=True)
    txt_filename = f"{folder_name}/{folder_name}.txt"
    with open(txt_filename, 'w', encoding='utf-8') as f:
        f.write(main_text)
    clean_text_file(txt_filename)

def scrape_images(url, folder_name):
    soup = get_page(url)
    os.makedirs(folder_name, exist_ok=True)
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if not img_url:
            continue
        try:
            img_name = img_url.split('/')[-1]
            img_name = img_name.split('.')[0] + '.jpg'
            img_path = os.path.join(folder_name, img_name)
            urllib.request.urlretrieve(img_url, img_path)
        except Exception as e:
            print(f'Error downloading {img_url}: {str(e)}')

#clean_text.py
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
    save_text_as_docx(text, filename)
    os.remove(filename)

def save_text_as_docx(text, filename):
    doc = docx.Document()
    doc.add_paragraph(text, style='Normal')
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = docx.shared.Pt(12)
    doc_file_name = os.path.splitext(filename)[0] + '.docx'
    doc.save(doc_file_name)

def pdf_exists(filename):
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            content = file.read()
        if '.pdf' in content:
            return True
    return False

#get_info.py
def get_url_and_folder():    
    url = input("Enter the URL: ")
    folder_name = input("Enter the name of the folder you want to save the files: ")
    directory = os.path.join(os.getcwd(), folder_name)
    return url, folder_name, directory

def merge_pdf_or_not(is_pdf, folder_name, directory):
    if is_pdf:
        merge = input("Do you want to get a merged PDF? ")
        if merge == "yes":
            merge_pdfs("merged.pdf", folder_name)
            os.rename(os.path.join(os.getcwd(), "merged.pdf"), os.path.join(directory, "merged.pdf"))

def scrape_text_and_images():
    url, folder_name, directory = get_url_and_folder()
    scrape_text(url, folder_name)
    include_images = input("Do you want to include the images? ")
    if include_images == 'yes':
        scrape_images(url, folder_name)
    print(f'The {folder_name} folder has been successfully created.')

def download_files_from_website():
    url, folder_name, directory = get_url_and_folder()
    fetch_and_store_files(url, folder_name)
    collect_filenames(directory, ".pdf")
    is_pdf = pdf_exists("file_list.txt")
    merge_pdf_or_not(is_pdf, folder_name, directory)
    clean_up_folder(directory)
    os.remove("file_list.txt")
    organize_files(directory)
    print(f'The {folder_name} folder has been successfully created.')

#main.py
def web_scraping():
    choice = int(input("=== Web Scraping Menu ===\n1. To scrape text and images from a website\n2. To download files from a website: "))
    if choice == 1:
        scrape_text_and_images()
    elif choice == 2:
        download_files_from_website()

web_scraping()