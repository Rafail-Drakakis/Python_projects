import os, glob, PyPDF2, pdf2image, pdf2docx
import tabula, openpyxl, os, tempfile, pandas as pd

def split_pdf(filename, page_ranges):
    """
    The `split_pdf` function takes a PDF file and a list of page ranges as input, and creates a new PDF
    file containing only the specified pages.
    
    :param filename: The `filename` parameter is the name of the PDF file that you want to split. It
    should be a string representing the file path or file name of the PDF file
    :param page_ranges: The `page_ranges` parameter is a list of page ranges that specify which pages to
    extract from the PDF file. Each page range can be specified in one of the following formats:
    """
    all_pages = []
    for page_range in page_ranges:
        if isinstance(page_range, int):
            all_pages.append(page_range)
        elif isinstance(page_range, str):
            if '-' in page_range:
                start, end = page_range.split('-')
                if not start.isdigit() or not end.isdigit():
                    raise ValueError(f'Invalid page range: {page_range}')
                start = int(start)
                end = int(end)
                if start > end:
                    raise ValueError(f'Invalid page range: {page_range}')
                all_pages.extend(range(start, end + 1))
            else:
                if not page_range.isdigit():
                    raise ValueError(f'Invalid page range: {page_range}')
                all_pages.append(int(page_range))
        else:
            raise ValueError(f'Invalid page range: {page_range}')

    with open(filename, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        if not all(1 <= p <= num_pages for p in all_pages):
            raise ValueError('Invalid page range')
        writer = PyPDF2.PdfWriter()
        for p in all_pages:
            writer.add_page(reader.pages[p - 1])
        with open("new_file.pdf", 'wb') as new_file:
            writer.write(new_file)

def convert_pdf(*pdf_paths):
    """
    The `convert_pdf` function converts PDF files to either images or Word documents based on the user's
    input.
    """
    conversion_option = input("Enter the conversion option (word/images): ")

    if conversion_option.lower() == "images":
        for pdf_path in pdf_paths:
            images = pdf2image.convert_from_path(pdf_path, dpi=1000)
            for idx, img in enumerate(images):
                img.save(f'page_{idx + 1}.jpg', 'JPEG', quality=80)
    
    elif conversion_option.lower() == "word":
        docx_paths = []
        for pdf_path in pdf_paths:
            docx_path = pdf_path.replace(".pdf", ".docx")
            pdf2docx.parse(pdf_path, docx_path)
            docx_paths.append(docx_path)

def merge_pdf_files(output_filename):
    """
    The function `merge_pdf_files` merges multiple PDF files into a single PDF file, and optionally
    deletes the original files.
    
    :param output_filename: The `output_filename` parameter is the name of the merged PDF file that will
    be created. It should be a string representing the desired name of the output file
    """
    files = sorted(glob.glob(os.path.join(os.getcwd(), f'*.pdf')))
    target_file = "filenames.txt"

    with open(target_file, 'w') as file:
        file.write('\n'.join(files))

    filenames = []
    with open(target_file, 'r') as file:
        filenames = file.read().splitlines()

    merger = PyPDF2.PdfMerger()
    for filename in filenames:
        merger.append(filename)
    merger.write(output_filename)
    merger.close()

    delete = input("Do you want to delete the original files (yes/no): ")
    if delete.lower() == "yes":
        with open(target_file, 'r') as file:
            for line in file:
                filepath = line.strip()  # Remove newline character
                os.remove(filepath)

    if os.path.exists(target_file):
        os.remove(target_file)

def convert_pdf_to_excel(input_pdf_path, output_excel_path):
    """
    The function `convert_pdf_to_excel` converts a PDF file into an Excel file by using the `tabula`
    library in Python.
    
    :param input_pdf_path: The input_pdf_path parameter is the file path of the PDF file that you want
    to convert to Excel. It should be a string that specifies the location of the PDF file on your
    computer
    :param output_excel_path: The `output_excel_path` parameter is the file path where you want to save
    the converted Excel file. It should include the file name and the extension `.xlsx`. For example, if
    you want to save the file as `converted_data.xlsx` in the current directory, you can set
    `output_excel
    """
    # Convert PDF to Excel
    pdf_data_frames = tabula.read_pdf(input_pdf_path, pages='all')
    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as excel_writer:
        for i, df in enumerate(pdf_data_frames):
            df.to_excel(excel_writer, sheet_name=f"Sheet{i+1}", index=False)

def merge_excel_sheets(input_excel_path, output_excel_path):
    """
    The function `merge_excel_sheets` merges multiple sheets from an input Excel file into a single
    sheet and saves it to an output Excel file.
    
    :param input_excel_path: The path to the input Excel file that contains the sheets you want to merge
    :param output_excel_path: The path where the merged Excel sheets will be saved
    """
    # Merge Excel sheets
    dfs = pd.read_excel(input_excel_path, sheet_name=None)
    merged_data_frame = pd.concat(dfs.values(), ignore_index=True)
    merged_data_frame.to_excel(output_excel_path, index=False)

def shift_empty_cells(output_excel_path):
    """
    The function `shift_empty_cells` takes an output Excel file path as input, loads the file, and
    shifts the values of empty cells to the right, filling them with the values of the non-empty cells
    in the same row.
    
    :param output_excel_path: The `output_excel_path` parameter is the file path of the Excel file that
    you want to modify. It should be a string that specifies the location of the file on your computer
    """
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

def flow(input_pdf_path):
    """
    The `flow` function takes an input PDF file path, converts it to an Excel file, merges the sheets in
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

def main():
    """
    The main function performs various operations on PDF files, including merging, converting, and
    splitting.
    """
    merge_pdf_files("merged.pdf")
    convert_pdf("sample.pdf")
    split_pdf("sample.pdf", [1,"3-5"])
    flow("table.pdf")

main()