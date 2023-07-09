#pdf_operations.py

import os
import glob
import PyPDF2
import pdf2image
import pdf2docx
import tabula
import openpyxl
from PyPDF2 import PdfReader, PdfWriter

def split_pdf(filename, page_ranges, output_filename):
    try:
        pdf = PdfReader(filename)
        output_pdf = PdfWriter()

        for range_string in page_ranges:
            pages = parse_page_range(range_string)
            for page_num in pages:
                output_pdf.add_page(pdf.pages[page_num - 1])

        with open(output_filename, "wb") as output_file:
            output_pdf.write(output_file)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def parse_page_range(range_string):
    pages = []
    ranges = range_string.split(",")
    for rng in ranges:
        if "-" in rng:
            start, end = map(int, rng.split("-"))
            pages.extend(range(start, end + 1))
        else:
            pages.append(int(rng))
    return pages

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
