import os, glob, PyPDF2, pdf2image, pdf2docx
import tabula, openpyxl, os, tempfile, pandas as pd
import img2pdf, pytesseract, PIL

def validate_page_range(page_range):
    """
    The `validate_page_range` function takes a page range as input and returns a list of page numbers if
    the input is valid, otherwise it raises a `ValueError` with an appropriate error message.
    
    :param page_range: The `page_range` parameter is the input that represents a range of pages. It can
    be either an integer or a string. If it is an integer, it is considered as a single page. If it is a
    string, it can be in the format of "start-end" to represent a
    :return: The function `validate_page_range` returns a list of integers representing the page range.
    """
    if isinstance(page_range, int):
        return [page_range]
    elif isinstance(page_range, str):
        if '-' in page_range:
            start, end = page_range.split('-')
            if not start.isdigit() or not end.isdigit():
                raise ValueError(f'Invalid page range: {page_range}')
            start = int(start)
            end = int(end)
            if start > end:
                raise ValueError(f'Invalid page range: {page_range}')
            return list(range(start, end + 1))
        else:
            if not page_range.isdigit():
                raise ValueError(f'Invalid page range: {page_range}')
            return [int(page_range)]
    else:
        raise ValueError(f'Invalid page range: {page_range}')

def split_pdf(filename, page_ranges, output_filename):
    """
    The function `split_pdf` takes a PDF file, a list of page ranges, and an output filename, and splits
    the PDF into separate files based on the specified page ranges.
    
    :param filename: The filename parameter is the name of the PDF file that you want to split. It
    should be a string that includes the file extension (e.g., "example.pdf")
    :param page_ranges: The `page_ranges` parameter is a list of tuples, where each tuple represents a
    range of pages to be included in the split PDF. Each tuple should contain two integers: the starting
    page and the ending page of the range. For example, `[(1, 3), (5,
    :param output_filename: The output_filename parameter is the name of the file that will be created
    after splitting the PDF. It is the name of the file that will contain the extracted pages from the
    original PDF file
    """
    all_pages = []
    for page_range in page_ranges:
        all_pages.extend(validate_page_range(page_range))

    with open(filename, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        if not all(1 <= p <= num_pages for p in all_pages):
            raise ValueError('Invalid page range')
        writer = PyPDF2.PdfWriter()
        for p in all_pages:
            writer.add_page(reader.pages[p - 1])
        with open(output_filename, 'wb') as new_file:
            writer.write(new_file)

def convert_pdf(*pdf_paths):
    """
    The `convert_pdf` function converts PDF files to either images or Word documents based on the user's
    input.
    """
    try:
        conversion_option = input("Enter the conversion option (word/images): ")

        if conversion_option.lower() == "images":
            for pdf_path in pdf_paths:
                try:
                    images = pdf2image.convert_from_path(pdf_path, dpi=1000)
                    for idx, img in enumerate(images):
                        img.save(f'page_{idx + 1}.jpg', 'JPEG', quality=80)
                except Exception as e:
                    print(f"Error converting PDF to images: {e}")

        elif conversion_option.lower() == "word":
            docx_paths = []
            for pdf_path in pdf_paths:
                try:
                    docx_path = pdf_path.replace(".pdf", ".docx")
                    pdf2docx.parse(pdf_path, docx_path)
                    docx_paths.append(docx_path)
                except Exception as e:
                    print(f"Error converting PDF to Word: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def merge_pdf_files(output_filename, all_files=True):
    """
    The `merge_pdf_files` function merges multiple PDF files into a single PDF file, either by selecting
    all files in the current directory or by manually entering the filenames.

    :param output_filename: The output_filename parameter is a string that specifies the name of the
    merged PDF file that will be created
    :param all_files: The `all_files` parameter is a boolean flag that determines whether to merge all
    PDF files in the current working directory or to manually enter the filenames to be merged, defaults
    to True (optional)
    """
    try:
        if all_files:
            files = sorted(glob.glob(os.path.join(os.getcwd(), '*.pdf')))
            if not files:
                print("Error: No PDF files found in the current directory.")
                return

            merger = PyPDF2.PdfMerger()
            for filename in files:
                merger.append(filename)
            merger.write(output_filename)
            merger.close()
        else:
            filenames = []
            while True:
                try:
                    filename = input("Enter the filename (or 'done' to finish): ")
                    if filename == "done":
                        break
                    if not os.path.exists(filename):
                        print(f"Error: File '{filename}' does not exist.")
                        continue
                    filenames.append(filename)
                except Exception as e:
                    print(f"An error occurred: {e}")

            if not filenames:
                print("No files specified.")
                return

            merger = PyPDF2.PdfMerger()
            for filename in filenames:
                merger.append(filename)
            merger.write(output_filename)
            merger.close()

    except Exception as e:
        print(f"An error occurred: {e}")

def pdf_to_excel(input_pdf_path, output_excel_path):
    """
    The function `pdf_to_excel` converts a PDF file into an Excel file by using the `tabula`
    library in Python.

    :param input_pdf_path: The input_pdf_path parameter is the file path of the PDF file that you want
    to convert to Excel. It should be a string that specifies the location of the PDF file on your
    computer
    :param output_excel_path: The `output_excel_path` parameter is the file path where you want to save
    the converted Excel file. It should include the file name and the extension `.xlsx`. For example, if
    you want to save the file as `converted_data.xlsx` in the current directory, you can set
    `output_excel
    """
    try:
        # Convert PDF to Excel
        pdf_data_frames = tabula.read_pdf(input_pdf_path, pages='all')
        with pd.ExcelWriter(output_excel_path, engine='openpyxl') as excel_writer:
            for i, df in enumerate(pdf_data_frames):
                df.to_excel(excel_writer, sheet_name=f"Sheet{i + 1}", index=False)
    
    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def merge_excel_sheets(input_excel_path, output_excel_path):
    """
    The function `merge_excel_sheets` merges multiple sheets from an input Excel file into a single
    sheet and saves it to an output Excel file.
    
    :param input_excel_path: The path to the input Excel file that contains the sheets you want to merge
    :param output_excel_path: The path where the merged Excel sheets will be saved
    """
    # Merge Excel sheets
    try:
        dfs = pd.read_excel(input_excel_path, sheet_name=None)
        merged_data_frame = pd.concat(dfs.values(), ignore_index=True)
        merged_data_frame.to_excel(output_excel_path, index=False)
    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def shift_empty_cells(output_excel_path):
    """
    The function `shift_empty_cells` takes an output Excel file path as input, loads the file, and
    shifts the values of empty cells to the right, filling them with the values of the non-empty cells
    in the same row.
    
    :param output_excel_path: The `output_excel_path` parameter is the file path of the Excel file that
    you want to modify. It should be a string that specifies the location of the file on your computer
    """
    # Load output Excel file
    try:
        excel_workbook = openpyxl.load_workbook(output_excel_path)
        for worksheet_name in excel_workbook.sheetnames:
            excel_worksheet = excel_workbook[worksheet_name]
            for row in excel_worksheet.iter_rows():
                empty_cell_list = []
                for current_cell in row:
                    if current_cell.value is None:
                        empty_cell_list.append(current_cell)
                    else:
                        for empty_cell_to_fill in empty_cell_list:
                            empty_cell_to_fill.value = current_cell.value
                            current_cell.value = None
                            empty_cell_list.remove(empty_cell_to_fill)
                            empty_cell_list.append(current_cell)
                            break
        excel_workbook.save(output_excel_path)
    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_pdf_to_excel(input_pdf_path):
    """
    The `convert_pdf_to_excel` function takes an input PDF file path, converts it to an Excel file, merges the sheets in
    the Excel file, and optionally shifts empty cells before saving the final Excel file.
    
    :param input_pdf_path: The input_pdf_path parameter is the file path of the PDF file that you want
    to convert to an Excel file
    """
    # Define output Excel file path
    output_excel_path = os.path.splitext(input_pdf_path)[0] + ".xlsx"

    # Create temporary Excel file paths
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
        temp_excel_path = temp_file.name
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as merged_file:
        merged_excel_path = merged_file.name

    try:
        pdf_to_excel(input_pdf_path, temp_excel_path)
        merge_excel_sheets(temp_excel_path, merged_excel_path)
        os.replace(merged_excel_path, output_excel_path)

        # Check if user wants to shift empty cells
        option = input("Do you want to shift empty cells? (yes/no) ")
        if option == "yes":
            shift_empty_cells(output_excel_path)

        print(f'File {output_excel_path} has been created successfully.')
    finally:
        # Remove temporary files
        os.remove(temp_excel_path)
        if os.path.exists(merged_excel_path):
            os.remove(merged_excel_path)

def extract_images_to_text(image_paths, output_file_path):
    """
    The function `extract_images_to_text` takes a list of image paths, extracts text from each image
    using Tesseract OCR, and writes the extracted text along with the image filename to an output file.
    
    :param image_paths: image_paths is a list of file paths to the images that you want to extract text
    from. Each image should be in a format that can be opened by PIL (Python Imaging Library)
    :param output_file_path: The output_file_path parameter is the path where the extracted text will be
    saved. It should be a string representing the file path, including the file name and extension. For
    example, "C:/output/text.txt" or "output/text.txt"
    :return: the file path of the output file.
    """
    texts = []
    for image_path in image_paths:
        try:
            with PIL.Image.open(image_path).convert('L') as img:
                text = pytesseract.image_to_string(img, lang='eng')
                if text:
                    texts.append(os.path.basename(image_path) + "\n" + text + "\n")
        except (OSError, pytesseract.TesseractError) as e:
            texts.append(f"Error processing image {os.path.basename(image_path)}: {e}\n")

    with open(output_file_path, "w") as output_file:
        output_file.writelines(texts)

    return output_file_path


def mirror_image(input_path, direction, output_dir=None, output_format='png'):
    """
    The `mirror_image` function takes an input image file, a direction (1 for left-right mirror, 2 for
    top-bottom mirror), and optional output directory and format, and returns the path of the mirrored
    image file.
    
    :param input_path: The path to the input image file that you want to mirror
    :param direction: The `direction` parameter specifies the type of mirror image transformation to be
    applied. It can take one of the following values:
    :param output_dir: The `output_dir` parameter is an optional parameter that specifies the directory
    where the mirrored image will be saved. If no `output_dir` is provided, the function will use the
    directory of the input image as the output directory
    :param output_format: The `output_format` parameter specifies the format of the output image file.
    By default, it is set to 'png', but you can change it to any supported image format such as 'jpg',
    'jpeg', 'gif', etc, defaults to png (optional)
    :return: the path of the mirrored image if successful, or an error message if there is an issue with
    the input file or the mirroring process.
    """
    if not os.path.isfile(input_path):
        return f"Error: {input_path} does not exist"
    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    output_filename = os.path.splitext(os.path.basename(input_path))[0]
    try:
        with PIL.Image.open(input_path) as img:
            if direction == 1:
                mirror_img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                mirror_output_path = os.path.join(output_dir, f"{output_filename}_mirror.{output_format.lower()}")
                mirror_img.save(mirror_output_path)
                return mirror_output_path
            elif direction == 2:
                mirror_img = img.transpose(PIL.Image.FLIP_TOP_BOTTOM)
                mirror_output_path = os.path.join(output_dir, f"{output_filename}_flip.{output_format.lower()}")
                mirror_img.save(mirror_output_path)
                return mirror_output_path
            else:
                return "Invalid direction specified"
    except OSError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def convert_image(input_path, output_format):
    """
    The function `convert_image` takes an input image file path and an output format, converts the image
    to the specified format, and returns the output file path.
    
    :param input_path: The input_path parameter is the path to the image file that you want to convert.
    It should be a string representing the file path, including the file name and extension. For
    example, "C:/images/image.jpg" or "/home/user/images/image.png"
    :param output_format: The `output_format` parameter is a string that specifies the desired format of
    the output image. It can be any valid image format supported by the PIL library, such as "JPEG",
    "PNG", "BMP", etc
    :return: the output path of the converted image.
    """
    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Error: File '{input_path}' does not exist.")

        output_dir = os.path.dirname(input_path)
        output_filename = input("Enter the output filename: ")
        output_path = os.path.join(output_dir, f"{output_filename}.{output_format.lower()}")

        with PIL.Image.open(input_path) as im:
            rgb_im = im.convert('RGB')
            rgb_im.save(output_path, format=output_format.upper())

        return output_path
    
    except FileNotFoundError as e:
        return f"Error: {e}"
    except PIL.UnidentifiedImageError as e:
        return f"Error: Invalid image format. {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def images_to_pdf(images, pdf_name):
    """
    The function `images_to_pdf` converts a list of images into a PDF file.
    
    :param images: A list of file paths to the images that you want to convert to a PDF
    :param pdf_name: The name of the PDF file that will be created
    """
    try:
        # create a new pdf file
        pdf_images = []
        for image in images:
            img = PIL.Image.open(image)
            pdf_images.append(img)

        if pdf_images:
            pdf_images[0].save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=pdf_images[1:])
        else:
            print("Error: No images found.")
    except Exception as e:
        print("Error: Failed to convert images to PDF.\nError:", str(e))

def split_pdf_menu():    
    """
    The `split_pdf_menu` function prompts the user to enter a PDF filename, page ranges, and an output
    filename, and then calls the `split_pdf` function to split the PDF into separate files based on the
    specified page ranges.
    """
    filename = input("Enter the PDF filename: ")
    while not os.path.isfile(filename):
        print("Invalid file name. Please try again.")
        filename = input("Enter the PDF filename: ")
        
    page_ranges = input("Enter the page ranges (comma-separated): ").split(",")
    while True:
        try:
            if all(validate_page_range(range) for range in page_ranges):
                break
        except ValueError as error:
            print(f"Error: {str(error)}")
        page_ranges = input("Error. Enter the page ranges (comma-separated): ").split(",")

    output_filename = input("Enter the output filename: ")
    while not output_filename.endswith('.pdf'):
        print("Invalid output filename. Please choose a different output filename.")
        output_filename = input("Enter the output filename: ")

    split_pdf(filename, page_ranges, output_filename)

def extract_images_to_text_menu():
    """
    The function `extract_images_to_text_menu()` prompts the user to enter an image path and an output
    file path, and then calls the `extract_images_to_text()` function with the provided paths.
    """
    image_path = input("Enter the image path: ")
        
    while not os.path.isfile(image_path):
        print("Invalid image path. Please try again.")
        image_path = input("Enter the image path: ")

    output_file_path = input("Enter the output file path: ")
        
    while not output_file_path.endswith(('.png', '.jpg', '.jpeg')):
        print("Invalid output filename. Please choose a different output filename.")
        output_file_path = input("Enter the output filename: ")

    extract_images_to_text([image_path], output_file_path)

def mirror_image_menu():
    """
    The `mirror_image_menu` function prompts the user to enter an image path and a direction, and then
    calls the `mirror_image` function with the provided inputs.
    """
    image_path = input("Enter the image path: ")
    while not os.path.isfile(image_path):
        print("Invalid image path. Please try again.")
        image_path = input("Enter the image path: ")
        
    direction = int(input("Enter the direction (1 for left-right mirror, 2 for top-bottom mirror): "))
    while not (direction == 1 or direction == 2):
        direction = int(input("Enter the direction (1 for left-right mirror, 2 for top-bottom mirror): "))

    mirror_image(image_path, direction)

def convert_image_menu():
    """
    The function `convert_image_menu` prompts the user to enter an image path and output format,
    validates the inputs, and then calls the `convert_image` function with the provided inputs.
    """
    image_path = input("Enter the image path: ")
                
    while not os.path.isfile(image_path):
        print("Invalid image path. Please try again.")
        image_path = input("Enter the image path: ")

    output_format = input("Enter the output format: ")
                    
    while not output_format.endswith(('.png', '.jpg', '.jpeg')):
        print("Invalid output filename. Please choose a different output format.")
        output_format = input("Enter the output format: ")
            
    convert_image(image_path, output_format)

def images_to_pdf_menu():
    """
    The function `images_to_pdf_menu()` prompts the user to enter a list of image paths, validates the
    paths, prompts for a PDF name, validates the name, and then calls the `images_to_pdf()` function
    with the valid image paths and PDF name.
    """
    image_paths = input("Enter the image paths (comma-separated): ").split(",")
    valid_image_paths = []

    for image_path in image_paths:
        while not os.path.isfile(image_path.strip()):
            print(f"Invalid image path: {image_path.strip()}. Please try again.")
            image_path = input("Enter the image path: ")
        valid_image_paths.append(image_path.strip())

    pdf_name = input("Enter the PDF name: ")
    while not output_format.endswith(('.pdf')):
        print("Invalid PDF name. Please choose a different output format.")
        output_format = input("Enter the output format: ")

    images_to_pdf(valid_image_paths, pdf_name)

def merge_pdf_files_menu():
    """
    The function `merge_pdf_files_menu` prompts the user to enter an output PDF filename and choose
    whether to specify individual PDF files or merge all PDF files in a directory, and then calls the
    `merge_pdf_files` function accordingly.
    """
    output_filename = input("Enter the output PDF filename: ")
    while not output_filename.endswith(('.pdf')):
        print("Invalid PDF name. Please choose a different output format.")
        output_filename = input("Enter the output filename: ")
        
    all_files = int(input("Press 1 to specify the pdf files or 2 to merge all of them in the directory: "))
    while all_files not in [1, 2] or not isinstance(all_files, int):
        all_files = input("Error! Press 1 to specify the PDF files or 2 to merge all of them in the directory: ")
        try:
            all_files = int(all_files)
        except ValueError:
            all_files = None

    if all_files == 1:
        merge_pdf_files(output_filename, all_files=False)
    elif all_files == 2:
        merge_pdf_files(output_filename, all_files=True)

def convert_pdf_menu():
    """
    The function `convert_pdf_menu()` prompts the user to enter a list of PDF paths, validates the
    paths, and then calls the `convert_pdf()` function with the valid paths as arguments.
    """
    pdf_paths = input("Enter the PDF paths (comma-separated): ").split(",")
    valid_pdf_paths = []

    for pdf_path in pdf_paths:
        while not os.path.isfile(pdf_path.strip()):
            print(f"Invalid pdf path: {pdf_path.strip()}. Please try again.")
            pdf_path = input("Enter the pdf path: ")
        valid_pdf_paths.append(pdf_path.strip())
        
    convert_pdf(*valid_pdf_paths)

def convert_pdf_to_excel_menu():
    """
    The function `convert_pdf_to_excel_menu()` prompts the user to enter a PDF file path, validates the
    path, and then calls the `convert_pdf_to_excel()` function.
    """
    input_pdf_path = input("Enter the input PDF path: ")
    
    while not os.path.isfile(input_pdf_path.strip()):
        print(f"Invalid PDF path: {input_pdf_path.strip()}. Please try again.")
        input_pdf_path = input("Enter the PDF path: ")

    convert_pdf_to_excel(input_pdf_path)

def menu():
    """
    The menu function takes user input to select a specific task and then calls the corresponding
    sub-menu function.
    """
    try:
        choice = int(input("1.Extract Images to Text\n2.Mirror Image\n3.Convert Image\n4.Convert Images to PDF\n5.Merge PDF Files\n6.Convert PDF to Images or Word\n7.Split PDF\n8.Convert PDF to Excel\nEnter your choice: "))
        if choice == 1:
            extract_images_to_text_menu()
        elif choice == 2:
            mirror_image_menu()
        elif choice == 3:
            convert_image_menu()
        elif choice == 4:
            images_to_pdf_menu()
        elif choice == 5:
            merge_pdf_files_menu()
        elif choice == 6:
            convert_pdf_menu()
        elif choice == 7:
            split_pdf_menu()
        elif choice == 8:
            convert_pdf_to_excel_menu()
    except ValueError:
        choice = None

menu()