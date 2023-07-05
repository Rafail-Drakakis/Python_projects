import sys, os, re
import urllib, urllib3
import warnings, shutil, requests
import bs4, docx, PyPDF2
import zipfile, tarfile, gzip

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#site_downloader.py
def collect_filenames(directory, filetype):
    """
    The function "collect_filenames" collects all filenames with a specific filetype in a given
    directory and writes them to a text file.
    
    :param directory: The "directory" parameter is the path to the directory where you want to collect
    the filenames from. It can be an absolute path or a relative path
    :param filetype: The `filetype` parameter is a string that specifies the type of files you want to
    collect. For example, if you want to collect all the text files in a directory, you would pass
    `'txt'` as the `filetype` parameter
    """
    file_list = [file for root, dirs, files in os.walk(directory) for file in files if file.endswith(filetype)]
    sorted_file_list = sorted(set(file_list)) # sort the files to appear correctly
    with open('file_list.txt', 'w') as output_file:
        for file in sorted_file_list:
            output_file.write(file + '\n')

def merge_pdfs(output_filename, folder_name):
    """
    The function `merge_pdfs` merges multiple PDF files from a specified folder into a single PDF file.
    
    :param output_filename: The name of the merged PDF file that will be created
    :param folder_name: The `folder_name` parameter is the name of the folder where the PDF files are
    located
    """
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
    """
    The function `fetch_and_store_files` fetches files from a given URL and stores them in a specified
    folder.
    
    :param url: The `url` parameter is the URL of the webpage from which you want to fetch and store
    files. It can be a webpage URL or a file URL
    :param folder_name: The `folder_name` parameter is the name of the folder where the fetched files
    will be stored
    """
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
    """
    The `clean_up_folder` function deletes files with .html and .php extensions and unzips files with
    supported extensions (.zip, .tgz, .gz) in a given folder path.
    
    :param folder_path: The `folder_path` parameter is a string that represents the path to the folder
    that needs to be cleaned up
    """
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
    """
    The `organize_files` function organizes files in a given directory by moving them into folders based
    on their file extensions.
    
    :param directory: The `directory` parameter is the path to the directory where the files are located
    """
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
def scrape_text(url, folder_name):
    """
    The function `scrape_text` takes a URL and a folder name as input, scrapes the main text from the
    webpage at the given URL, and saves the cleaned text in a text file within the specified folder.
    
    :param url: The `url` parameter is the URL of the webpage you want to scrape the text from
    :param folder_name: The `folder_name` parameter is the name of the folder where you want to save the
    extracted text file
    """
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
    """
    The function `scrape_images` takes a URL and a folder name as input, scrapes all the images from the
    webpage at the given URL, and saves them in the specified folder.
    
    :param url: The `url` parameter is the URL of the webpage from which you want to scrape images. It
    should be a string
    :param folder_name: The `folder_name` parameter is the name of the folder where the scraped images
    will be saved
    """
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
    """
    The function `replace_chars` takes a text as input and replaces all characters from 1 to 99 with a
    space, and replaces tabs with three spaces.
    
    :param text: The `text` parameter is a string that represents the text you want to modify
    :return: the modified text after replacing certain characters.
    """
    chars_to_replace = [f"[{i}]" for i in range(1, 100)]
    for char in chars_to_replace:
        text = text.replace(char, ' ')
    text = text.replace('\t', '   ')  # Replace tab with three spaces
    return text

def clean_text_file(filename):
    """
    The function `clean_text_file` reads a text file, replaces multiple consecutive new lines with a
    single new line and adds three spaces instead of a new line, replaces three or more spaces with two
    spaces, saves the modified text as a DOCX file, and finally deletes the original text file.
    
    :param filename: The `filename` parameter is the name of the text file that you want to clean
    """
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
    """
    The function `save_text_as_docx` takes in a string of text and a filename, and saves the text as a
    .docx file with the specified filename.
    
    :param text: The `text` parameter is the content that you want to save as a .docx file. It can be a
    string containing any text you want to include in the document
    :param filename: The `filename` parameter is the name of the file you want to save the text as. It
    should include the file extension, such as ".txt" or ".docx"
    """
    doc = docx.Document()
    doc.add_paragraph(text, style='Normal')
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = docx.shared.Pt(12)
    doc_file_name = os.path.splitext(filename)[0] + '.docx'
    doc.save(doc_file_name)

def pdf_exists(filename):
    """
    The function checks if a file exists and if it contains the string ".pdf".
    
    :param filename: The parameter "filename" is a string that represents the name or path of the file
    that you want to check if it exists and if it is a PDF file
    :return: a boolean value. It returns True if the file exists and contains the string ".pdf" in its
    content, and False otherwise.
    """
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            content = file.read()
        if '.pdf' in content:
            return True
    return False

#get_info.py
def get_url_and_folder():    
    """
    The function `get_url_and_folder` prompts the user to enter a URL and a folder name, and then
    returns the URL, folder name, and the directory path where the files will be saved.
    :return: three values: the URL entered by the user, the name of the folder entered by the user, and
    the directory path where the folder will be created.
    """
    url = input("Enter the URL: ")
    folder_name = input("Enter the name of the folder you want to save the files: ")
    directory = os.path.join(os.getcwd(), folder_name)
    return url, folder_name, directory

def get_page(url):
    """
    The function `get_page` takes a URL as input, sends a GET request to that URL, and returns the
    parsed HTML content of the web page.
    
    :param url: The `url` parameter is the URL of the web page that you want to retrieve
    :return: a BeautifulSoup object, which is created from the content of the web page obtained from the
    given URL.
    """
    response = requests.get(url)
    successful_response = 200
    if response.status_code != successful_response:
        print('Error: Failed to get the web page')
        sys.exit(1)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    return soup

def merge_pdf_or_not(is_pdf, folder_name, directory):
    """
    The function checks if the file is a PDF, asks the user if they want to merge the PDFs, and if yes,
    it merges the PDFs and renames the merged file.
    
    :param is_pdf: A boolean value indicating whether the files in the folder are PDFs or not
    :param folder_name: The name of the folder where the PDF files are located
    :param directory: The `directory` parameter represents the path to the directory where the merged
    PDF file will be saved
    """
    if is_pdf:
        merge = input("Do you want to get a merged PDF? ")
        if merge == "yes":
            merge_pdfs("merged.pdf", folder_name)
            os.rename(os.path.join(os.getcwd(), "merged.pdf"), os.path.join(directory, "merged.pdf"))

#menu.py
def scrape_text_and_images():
    """
    The function `scrape_text_and_images` scrapes text and images from a given URL, saves the text in a
    folder with a specified name, and optionally saves the images in the same folder.
    """
    url, folder_name, directory = get_url_and_folder()
    scrape_text(url, folder_name)
    include_images = input("Do you want to include the images? ")
    if include_images == 'yes':
        scrape_images(url, folder_name)
    print(f'The {folder_name} folder has been successfully created.')

def download_files_from_website():
    """
    The function `download_files_from_website` downloads files from a website, stores them in a
    specified folder, checks if any of the files are PDFs, merges the PDFs if necessary, cleans up the
    folder, organizes the files, and prints a success message.
    """
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
    """
    The function `web_scraping()` presents a menu to the user, allowing them to choose between scraping
    text and images from a website or downloading files from a website.
    """
def web_scraping():
    choice = int(input("=== Web Scraping Menu ===\n1. To scrape text and images from a website\n2. To download files from a website: "))
    if choice == 1:
        scrape_text_and_images()
    elif choice == 2:
        download_files_from_website()

web_scraping()