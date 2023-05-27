import os
import pathlib
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
import pytesseract
import img2pdf
import pdf2docx
import pdf2image

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
    pdf_files = [entry.name for entry in os.scandir(os.getcwd()) if entry.is_file() and entry.name.lower().endswith('.pdf')]
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

def image_to_pdf(output_path):
    image_paths = [entry.name for entry in os.scandir(os.getcwd()) if entry.is_file() and (entry.name.lower().endswith('.jpg') or entry.name.lower().endswith('.png') or entry.name.lower().endswith('.jpeg'))]
    
    pdf_bytes = img2pdf.convert(image_paths)
    
    with open(output_path, "wb") as file:
        file.write(pdf_bytes)
    
    print("Successfully created PDF file")

def extract_image_text(image_path, output_file):
    try:
        with Image.open(image_path).convert('L') as img:
            text = pytesseract.image_to_string(img, lang='eng')
            output_file.write(os.path.basename(image_path) + "\n")
            output_file.write(text + "\n")
    except (OSError, pytesseract.TesseractError) as e:
        print(f"Error processing image {os.path.basename(image_path)}: {e}")

def extract_multiple_images_text(output_file_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    cwd = os.getcwd()

    with open(output_file_path, "w") as output_file:
        for entry in os.scandir(cwd):
            if entry.is_file() and any(entry.name.lower().endswith(ext) for ext in image_extensions):
                extract_image_text(entry.path, output_file)

    print(f'Text extracted and saved to {output_file_path} file.')

def mirror_image(input_path, direction, output_dir=None, output_format='png'):
    if not os.path.isfile(input_path):
        print(f"Error: {input_path} does not exist")
        return

    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    output_filename = os.path.splitext(os.path.basename(input_path))[0]

    try:
        with Image.open(input_path) as img:
            if direction == 1:
                mirror_img = img.transpose(Image.FLIP_LEFT_RIGHT)
                mirror_output_path = os.path.join(output_dir, f"{output_filename}_mirror.{output_format.lower()}")
                mirror_img.save(mirror_output_path)
                print(f"Image mirrored successfully")
            elif direction == 2:
                mirror_img = img.transpose(Image.FLIP_TOP_BOTTOM)
                mirror_output_path = os.path.join(output_dir, f"{output_filename}_flip.{output_format.lower()}")
                mirror_img.save(mirror_output_path)
                print(f"Image flipped successfully")
            else:
                print("Invalid direction specified")
                return
    except OSError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def convert_image(input_path, output_format):
    if not os.path.exists(input_path):
        print(f"Error: file '{input_path}' does not exist.")
        return

    output_dir = os.path.dirname(input_path)
    output_filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{output_filename}.{output_format.lower()}")

    with Image.open(input_path) as im:
        rgb_im = im.convert('RGB')
        rgb_im.save(output_path, format=output_format.upper())

    print(f"Conversion from {os.path.splitext(input_path)[1][1:].upper()} to {output_format.upper()}")  

def main():
    extract_multiple_images_text("text_from_images.txt")
    mirror_image('image.png', direction=1)
    mirror_image('image.png', direction=2)
    convert_image('image.png', 'jpeg')
    
    os.remove("image.jpeg")
    os.remove("image_flip.png")
    os.remove("image_mirror.png")
    os.remove("text_from_images.txt")

    pdf_to_word("sample.pdf")
    pdf_to_images("sample.pdf")
    merge_pdfs("merged.pdf")
    split_pdf("sample.pdf", [7, "2-5"])
    image_to_pdf("output.pdf")

    os.remove("sample_pages_7_2_3_4_5.pdf")
    os.remove("merged.pdf")
    os.remove("sample.docx")
    for index in range(1, 11):
        os.remove(f'page_{index}.jpg')
    os.remove("output.pdf")

main()