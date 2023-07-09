#sub_menu.py

import os
import pdf_operations
import image_module
import pdf_to_excel

def split_pdf_menu():
    filename = input("Enter the PDF filename: ")
    while not os.path.isfile(filename):
        print("Invalid file name. Please try again.")
        filename = input("Enter the PDF filename: ")

    page_ranges = input("Enter the page ranges (comma-separated): ").split(",")
    while True:
        try:
            if all(pdf_operations.validate_page_range(range) for range in page_ranges):
                break
        except ValueError as error:
            print(f"Error: {str(error)}")
        page_ranges = input("Error. Enter the page ranges (comma-separated): ").split(",")

    output_filename = input("Enter the output filename: ")
    while not output_filename.endswith('.pdf'):
        print("Invalid output filename. Please choose a different output filename.")
        output_filename = input("Enter the output filename: ")

    pdf_operations.split_pdf(filename, page_ranges, output_filename)

def extract_images_to_text_menu():
    image_path = input("Enter the image path: ")
    while not os.path.isfile(image_path):
        print("Invalid image path. Please try again.")
        image_path = input("Enter the image path: ")

    output_file_path = input("Enter the output file path: ")
    while not output_file_path.endswith('.txt'):
        print("Invalid output filename. Please choose a different output filename.")
        output_file_path = input("Enter the output file path: ")

    image_module.extract_images_to_text([image_path], output_file_path)

def mirror_image_menu():
    image_path = input("Enter the image path: ")
    while not os.path.isfile(image_path):
        print("Invalid image path. Please try again.")
        image_path = input("Enter the image path: ")

    direction = int(input("Enter the direction (1 for left-right mirror, 2 for top-bottom mirror): "))
    while direction not in [1, 2]:
        direction = int(input("Enter the direction (1 for left-right mirror, 2 for top-bottom mirror): "))

    image_module.mirror_image(image_path, direction)

def convert_image_menu():
    image_path = input("Enter the image path: ")
    while not os.path.isfile(image_path):
        print("Invalid image path. Please try again.")
        image_path = input("Error! Enter the image path: ")

    output_format = input("Enter the output format: ")
    image_module.convert_image(image_path, output_format)

def images_to_pdf_menu():
    image_paths = input("Enter the image paths (comma-separated): ").split(",")
    valid_image_paths = []

    for image_path in image_paths:
        while not os.path.isfile(image_path.strip()):
            print(f"Invalid image path: {image_path.strip()}. Please try again.")
            image_path = input("Enter the image path: ")
        valid_image_paths.append(image_path.strip())

    pdf_name = input("Enter the PDF name: ")
    while not pdf_name.endswith('.pdf'):
        print("Invalid PDF name. Please choose a different PDF name.")
        pdf_name = input("Enter the PDF name: ")

    image_module.images_to_pdf(valid_image_paths, pdf_name)

def merge_pdf_files_menu():
    output_filename = input("Enter the output PDF filename: ")
    while not output_filename.endswith('.pdf'):
        print("Invalid PDF name. Please choose a different output filename.")
        output_filename = input("Enter the output PDF filename: ")

    all_files = int(input("Press 1 to specify the PDF files or 2 to merge all of them in the directory: "))
    while all_files not in [1, 2]:
        all_files = int(input("Error! Press 1 to specify the PDF files or 2 to merge all of them in the directory: "))

    if all_files == 1:
        pdf_operations.merge_pdf_files(output_filename, all_files=False)
    elif all_files == 2:
        pdf_operations.merge_pdf_files(output_filename, all_files=True)

def pdf_to_word_menu():
    pdf_paths = input("Enter the PDF paths (comma-separated): ").split(",")
    valid_pdf_paths = []

    for pdf_path in pdf_paths:
        while not os.path.isfile(pdf_path.strip()):
            print(f"Invalid PDF path: {pdf_path.strip()}. Please try again.")
            pdf_path = input("Enter the PDF path: ")
        valid_pdf_paths.append(pdf_path.strip())

    pdf_operations.pdf_to_word(*valid_pdf_paths)

def pdf_to_images_menu():
    pdf_paths = input("Enter the PDF paths (comma-separated): ").split(",")
    valid_pdf_paths = []

    for pdf_path in pdf_paths:
        while not os.path.isfile(pdf_path.strip()):
            print(f"Invalid PDF path: {pdf_path.strip()}. Please try again.")
            pdf_path = input("Enter the PDF path: ")
        valid_pdf_paths.append(pdf_path.strip())

    pdf_operations.pdf_to_images(*valid_pdf_paths)

def convert_pdf_to_excel_menu():
    input_pdf_path = input("Enter the input PDF path: ")
    while not os.path.isfile(input_pdf_path.strip()):
        print(f"Invalid PDF path: {input_pdf_path.strip()}. Please try again.")
        input_pdf_path = input("Enter the input PDF path: ")

    pdf_to_excel.pdf_to_excel(input_pdf_path)