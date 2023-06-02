import sys, os, re
import urllib, urllib3
import warnings, shutil, requests
import bs4, docx, PyPDF2
import zipfile, tarfile, gzip

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#site_downloader.py
def collect_filenames(directory, filetype):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(filetype):
                file_list.append(file)
    
    sorted_file_list = sorted(set(file_list)) # sort the files to appear correctly
    
    with open('file_list.txt', 'w') as output_file:
        for file in sorted_file_list:
            output_file.write(file + '\n')

def merge_pdfs(output_filename, folder_name):
    pdf_directory = os.path.join(os.getcwd(), folder_name)
    text_file = 'file_list.txt'
    merged_pdf = output_filename
    filenames = []

    with open(text_file, 'r') as file:
        filenames = file.read().splitlines()

    merger = PyPDF2.PdfMerger()
    for filename in filenames:
        filepath = os.path.join(pdf_directory, filename)
        if os.path.isfile(filepath):
            merger.append(filepath)
        else:
            print(f"Warning: File not found - {filepath}")

    if len(merger.pages) > 0:
        merger.write(output_filename)
        merger.close()
        print("PDF merging complete!")
    else:
        print("No PDF files found for merging.")

def download_files_from_website(url, folder_name):
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
                if file_response.status_code == 200:
                    with open(file_name, 'wb') as file:
                        file.write(file_response.content)

#scrape_data.py
def scrape_text_to_file(url, folder_name):
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
    os.makedirs(folder_name, exist_ok=True)
    with open(f"{folder_name}/{folder_name}.txt", 'w', encoding='utf-8') as f:
        f.write(main_text)
    clean_text_file(f"{folder_name}/{folder_name}.txt")

def scrape_images_to_file(url, folder_name):
    response = requests.get(url)
    if response.status_code != 200:
        print('Error: Failed to get the web page')
        sys.exit(1)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
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
    doc = docx.Document()
    doc.add_paragraph(text, style='Normal')
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = docx.shared.Pt(12)
    doc_file_name = os.path.splitext(filename)[0] + '.docx'
    doc.save(doc_file_name)
    os.remove(filename)

#clean_folder.py
def clean_up_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            # Delete files with .html and .php extensions
            if file.endswith(".html") or file.endswith(".php"):
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

#file_organizer.py
def file_organizer(directory):
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

    print("Files have been organized!")

#main.py
def web_scraping():
    print("=== Web Scraping Menu ===")
    print("0. To exit")
    print("1. To scrape text and images from a website")
    print("2. To download files from a website")

    choice = int(input("Enter your choice: "))
    
    if choice == 0:
        exit(1)

    url = input("Enter the URL: ")
    folder_name = input("Enter the name of the folder you want to save the files: ")
    directory = os.path.join(os.getcwd(), folder_name)

    if choice == 1:
        scrape_text_to_file(url, folder_name)
        images_true = input("Do you want to include the images? ")
        if images_true == 'yes':
            scrape_images_to_file(url, folder_name)
        print(f'The {folder_name} folder has been successfully created.')
    elif choice == 2:
        download_files_from_website(url, folder_name)
        collect_filenames(directory, ".pdf")
        merge_true = input("Do you want to get a merged PDF? ")
        if merge_true == "yes":
            merge_pdfs("merged.pdf", folder_name)
            os.rename(os.path.join(os.getcwd(), "merged.pdf"), os.path.join(directory, "merged.pdf"))
        clean_up_folder(directory)
        os.remove("file_list.txt")
        file_organizer(directory)

web_scraping()