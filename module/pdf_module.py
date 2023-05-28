import pdf2image, pdf2docx
from PyPDF2 import PdfReader, PdfWriter
import os

def validate_page_range(page_range):
    if isinstance(page_range, int):
        return [page_range]
    elif isinstance(page_range, str):
        start, _, end = page_range.partition('-')
        if not start.isdigit() or not end.isdigit():
            raise ValueError(f'Invalid page range: {page_range}')
        start = int(start)
        end = int(end)
        if start > end:
            raise ValueError(f'Invalid page range: {page_range}')
        return list(range(start, end + 1))
    else:
        raise ValueError(f'Invalid page range: {page_range}')

def split_pdf(filename, pages):
    all_pages = []
    for page_range in pages:
        all_pages.extend(validate_page_range(page_range))

    with open(filename, 'rb') as file:
        reader = PdfReader(file)
        num_pages = len(reader.pages)
        if not all(1 <= p <= num_pages for p in all_pages):
            raise ValueError('Invalid page range')
        writer = PdfWriter()
        for p in all_pages:
            writer.add_page(reader.pages[p - 1])
        new_filename = f'{os.path.splitext(filename)[0]}_pages_{"_".join(str(p) for p in all_pages)}.pdf'
        with open(new_filename, 'wb') as new_file:
            writer.write(new_file)
        print(f'New file created: {new_filename}')

def merge_pdfs(output_filename):
    pdf_files = [entry.name for entry in os.scandir(os.getcwd()) if
                 entry.is_file() and entry.name.lower().endswith('.pdf')]
    merger = PdfWriter()
    for file_name in pdf_files:
        with open(file_name, 'rb') as file:
            merger.append(PdfReader(file))
    with open(output_filename, 'wb') as file:
        merger.write(file)
    print(f"Merged PDF file saved as {output_filename}")

def pdf_to_images(filename):
    images = pdf2image.convert_from_path(filename, dpi=1000)
    for idx, img in enumerate(images):
        img.save(f'page_{idx + 1}.jpg', 'JPEG', quality=80)
    print("PDF converted successfully")

def pdf_to_word(*pdf_paths):
    for pdf_path in pdf_paths:
        docx_path = pdf_path.replace(".pdf", ".docx")
        pdf2docx.parse(pdf_path, docx_path)
        print(f"Conversion complete. Output file saved as {docx_path}")