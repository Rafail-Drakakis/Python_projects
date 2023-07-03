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
    The function `collect_filenames` collects all filenames with a specific filetype in a given
    directory and writes them to a text file.
    
    :param directory: The `directory` parameter is the path to the directory where you want to collect
    the filenames from. It can be an absolute path or a relative path
    :param filetype: The `filetype` parameter is a string that specifies the file extension or type you
    want to collect. For example, if you want to collect all the text files in a directory, you would
    pass `'txt'` as the `filetype` parameter
    """
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
    """
    The function `merge_pdfs` merges multiple PDF files from a specified folder into a single PDF file.
    
    :param output_filename: The name of the merged PDF file that will be created
    :param folder_name: The `folder_name` parameter is the name of the folder where the PDF files are
    located
    """
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
    """
    The function `download_files_from_website` downloads files from a given website URL and saves them
    in a specified folder.
    
    :param url: The URL of the website from which you want to download files
    :param folder_name: The `folder_name` parameter is the name of the folder where the downloaded files
    will be saved
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
                if file_response.status_code == 200:
                    with open(file_name, 'wb') as file:
                        file.write(file_response.content)

#clean_folder.py
def clean_up_folder(folder_path):
    """
    The `clean_up_folder` function deletes files with .html and .php extensions and unzips files with
    supported extensions in a given folder path.
    
    :param folder_path: The `folder_path` parameter is a string that represents the path to the folder
    that you want to clean up
    """
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
    """
    The `file_organizer` function organizes files in a given directory by moving them into folders based
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

    print("Files have been organized!")
    
#scrape_data.py
def scrape_text_to_file(url, folder_name):
    """
    The function `scrape_text_to_file` scrapes the main text from a web page specified by the `url`
    parameter, saves it to a text file in a folder specified by the `folder_name` parameter, and
    performs some cleaning operations on the text before saving it.
    
    :param url: The `url` parameter is the URL of the web page you want to scrape the text from
    :param folder_name: The `folder_name` parameter is the name of the folder where you want to save the
    text file. It will be used as both the folder name and the file name for the text file
    """
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
    """
    The function `scrape_images_to_file` downloads all the images from a given URL and saves them to a
    specified folder.
    
    :param url: The `url` parameter is the URL of the web page from which you want to scrape images
    :param folder_name: The `folder_name` parameter is the name of the folder where the scraped images
    will be saved
    """
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
    """
    The function `replace_chars` replaces certain characters in a given text with spaces.
    
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
    The function `clean_text_file` takes a filename as input, reads the text from the file, cleans the
    text by replacing multiple consecutive new lines with a single new line and adding three spaces
    instead of a new line, replaces three or more spaces with two spaces, creates a new Word document,
    adds the cleaned text to the document with a specified style, saves the document with a .docx
    extension, and finally deletes the original text file.
    
    :param filename: The `filename` parameter is the name of the text file that you want to clean and
    convert to a Word document
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
    doc = docx.Document()
    doc.add_paragraph(text, style='Normal')
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = docx.shared.Pt(12)
    doc_file_name = os.path.splitext(filename)[0] + '.docx'
    doc.save(doc_file_name)
    os.remove(filename)

#main.py
def web_scraping():
    """
    The `web_scraping` function allows users to choose between scraping text and images from a website
    or downloading files from a website, and performs the corresponding actions based on the user's
    choice.
    """
    choice = int(input("=== Web Scraping Menu ===\n1. To scrape text and images from a website\n2. To download files from a website: "))

    if choice > 2 or choice < 1:
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