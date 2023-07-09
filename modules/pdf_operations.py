#pdf_operations.py

import os
import glob
import PyPDF2
import pdf2image
import pdf2docx
import tabula
import openpyxl

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

def split_pdf(filename, page_ranges, output_filename):
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

def merge_pdf_files(output_filename, all_files=True):
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

def pdf_to_word(*pdf_paths):
    """
    The `convert_pdf` function converts PDF files to either images or Word documents based on the user's
    input.
    """
    try:
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

def pdf_to_images(*pdf_paths):
    try:
        for pdf_path in pdf_paths:
            try:
                images = pdf2image.convert_from_path(pdf_path, dpi=1000)
                for idx, img in enumerate(images):
                    img.save(f'page_{idx + 1}.jpg', 'JPEG', quality=80)
            except Exception as e:
                print(f"Error converting PDF to images: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
