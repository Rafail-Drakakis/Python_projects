import os, glob, PyPDF2, pdf2image, pdf2docx

def split_pdf(filename, page_ranges):
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
    extension = os.path.splitext(output_filename)[1][1:]  # Get extension from the given file path
    files = sorted(glob.glob(os.path.join(os.getcwd(), f'*.{extension}')))
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

def main():
    merge_pdf_files("merged.pdf")
    convert_pdf("sample.pdf")
    split_pdf("sample.pdf", [1,"3-5"])

main()