import os
import PIL.Image
import pytesseract

def extract_text_from_image(image_path, lang='eng'):
    try:
        img = PIL.Image.open(image_path)
    except OSError as e:
        print(f"Error loading image: {e}")
        return None

    img = img.convert('L')
    text = pytesseract.image_to_string(img, lang=lang)
    return text

def write_filenames_to_txt(output_file, directory):
    with open(output_file, "w") as file:
        for entry in os.listdir(directory):
            entry_path = os.path.join(directory, entry)
            if os.path.isdir(entry_path):
                write_filenames_to_txt(output_file, entry_path)
            else:
                file.write(entry + "\n")

def extract_multiple_images_text(choice):
    if choice == 1:
        image_path = input("Enter the filename of the image: ")
        text = extract_text_from_image(image_path)
        if text is not None:
            print(text)
    elif choice == 2:
        filenames_file = "filenames.txt"
        write_filenames_to_txt(filenames_file, os.getcwd())
        with open("text_from_images.txt", "w") as output_file:
            with open(filenames_file, "r") as filenames:
                for filename in filenames:
                    image_path = filename.strip()
                    text = extract_text_from_image(image_path)
                    if text is not None:
                        output_file.write(filename.strip() + "\n")
                        output_file.write(text + "\n")
        print("Text extracted from multiple images and saved to text_from_images.txt file.")
    else:
        print("Invalid choice.")