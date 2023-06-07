import pdf2image, pdf2docx, PyPDF2, os, glob, img2pdf, pytesseract, os, PIL, tabula, openpyxl, os, tempfile, pandas as pd,

def convert_pdf_to_excel(input_pdf_path, output_excel_path):
    # Convert PDF to Excel
    pdf_data_frames = tabula.read_pdf(input_pdf_path, pages='all')
    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as excel_writer:
        for i, df in enumerate(pdf_data_frames):
            df.to_excel(excel_writer, sheet_name=f"Sheet{i+1}", index=False)

def merge_excel_sheets(input_excel_path, output_excel_path):
    # Merge Excel sheets
    dfs = pd.read_excel(input_excel_path, sheet_name=None)
    merged_data_frame = pd.concat(dfs.values(), ignore_index=True)
    merged_data_frame.to_excel(output_excel_path, index=False)

def shift_empty_cells(output_excel_path):
    # Load output Excel file
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

def extract_image_text(image_path):
    try:
        with PIL.Image.open(image_path).convert('L') as img:
            text = pytesseract.image_to_string(img, lang='eng')
            return text
    except (OSError, pytesseract.TesseractError) as e:
        return f"Error processing image {os.path.basename(image_path)}: {e}"
        return None

def extract_multiple_images_text(output_file_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    texts = []
    for entry in os.scandir(os.getcwd()):
        if entry.is_file() and any(entry.name.lower().endswith(ext) for ext in image_extensions):
            text = extract_image_text(entry.path)
            if text is not None:
                texts.append(os.path.basename(entry.path) + "\n" + text + "\n")

    with open(output_file_path, "w") as output_file:
        output_file.writelines(texts)

    return output_file_path

def mirror_image(input_path, direction, output_dir=None, output_format='png'):
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
    if not os.path.exists(input_path):
        return f"Error: file '{input_path}' does not exist."
    output_dir = os.path.dirname(input_path)
    output_filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{output_filename}.{output_format.lower()}")
    with PIL.Image.open(input_path) as im:
        rgb_im = im.convert('RGB')
        rgb_im.save(output_path, format=output_format.upper())
    return output_path

def validate_page_range(page_range):
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

def split_pdf(filename, page_ranges):
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
        new_filename = "new_file.pdf"
        with open(new_filename, 'wb') as new_file:
            writer.write(new_file)
        return new_filename

def pdf_to_images(filename):
    images = pdf2image.convert_from_path(filename, dpi=1000)
    for idx, img in enumerate(images):
        img.save(f'page_{idx + 1}.jpg', 'JPEG', quality=80)

def pdf_to_word(*pdf_paths):
    docx_paths = []
    for pdf_path in pdf_paths:
        docx_path = pdf_path.replace(".pdf", ".docx")
        pdf2docx.parse(pdf_path, docx_path)
        docx_paths.append(docx_path)

def collect_filenames(extension):
    files = glob.glob(os.path.join(os.getcwd(), f'*.{extension}'))
    target_file = "filenames.txt"
    with open(target_file, 'w') as file:
        file.write('\n'.join(files))
    return target_file

def merge_pdfs(output_filename):
    pdf_directory = os.getcwd()
    text_file = 'filenames.txt'
    merged_pdf = output_filename
    filenames = []

    with open(text_file, 'r') as file:
        filenames = file.read().splitlines()

    merger = PyPDF2.PdfMerger()
    for filename in filenames:
        merger.append(filename)
    merger.write(output_filename)
    merger.close()

def excel_main(input_pdf_path):
    # Define output Excel file path
    output_excel_path = os.path.splitext(input_pdf_path)[0] + ".xlsx"

    # Create temporary Excel file paths
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
        temp_excel_path = temp_file.name
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as merged_file:
        merged_excel_path = merged_file.name

    try:
        convert_pdf_to_excel(input_pdf_path, temp_excel_path)
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

def image_main():
    print("Text extracted and saved to", extract_multiple_images_text("text_from_images.txt"))
    print("Image mirrored successfully", mirror_image('image.png', direction=1))
    print("Image flipped successfully", mirror_image('image.png', direction=2))
    print("Image converted successfully", convert_image('image.png', 'jpeg'))

def pdf_main():    
    pdf_to_word("sample.pdf")
    pdf_to_images("sample.pdf")
    collect_filenames('pdf')
    merge_pdfs('merged.pdf')
    split_pdf("merged.pdf", ("2", "5", "10-11"))

def main():
    excel_main("table.pdf")
    image_main()
    pdf_main()