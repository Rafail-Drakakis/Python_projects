import pytesseract
from PIL import Image
from rembg import remove
import os
import time

#main menu
def image_processing_menu():
    option = int(input("Enter: \n1.To extract text from an image \n2.To remove baground from an image \n3.To mirror an image \n4.To convert an image: "))
    if option == 1:
        extract_image_text()
    elif option == 2 or option == 3:
        image_processing(option)
    elif option == 4:
        convert_image_format()

#convert image
def convert_image_format():
    input_path = input("Enter the input file name: ")
    output_dir = os.path.dirname(input_path)
    output_filename = os.path.splitext(os.path.basename(input_path))[0]
    convert_output_path = os.path.join(output_dir, f"{output_filename}.jpg")
    convert_image(input_path, convert_output_path)

def convert_image(input_path: str, output_path: str) -> None:
    with Image.open(input_path) as im:
        rgb_im = im.convert('RGB')  # Convert to RGB mode
        rgb_im.save(output_path)
    print(f"Conversion from {os.path.splitext(input_path)[1]} to {os.path.splitext(output_path)[1]} successful!")

#image processing (baground removal and mirroring)
def image_processing(choice):
    input_path = input("Enter the input file name: ")
    if not os.path.isfile(input_path):
        print("Error: Input file does not exist")
        return
    if not input_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        print("Error: Invalid file format. Only JPG, PNG, and BMP files are supported")
        return
	
    output_dir = os.path.dirname(input_path)
    output_filename = os.path.splitext(os.path.basename(input_path))[0]
    
    if choice == 2:
        remove_output_path = os.path.join(output_dir, f"not_{output_filename}.png")
        remove_background(input_path, remove_output_path)
    elif choice == 3:	
        mirror_output_path = os.path.join(output_dir, f"{output_filename}_mirror.png")
        mirror_image(input_path, mirror_output_path)

def remove_background(input_path, output_path):
    try:
        with Image.open(input_path) as image_input:
            output = remove(image_input)
            output.save(output_path)
        print("Background removed successfully")
    except OSError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def mirror_image(input_path, output_path):
    direction = int(input("Enter \n1.For horizontal flip \n2.For vertical flip: "))
    try:
        with Image.open(input_path) as img:
            if direction == 1:
                mirror_img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif direction == 2:
                mirror_img = img.transpose(Image.FLIP_TOP_BOTTOM)
            else:
                print("Invalid direction specified")
            mirror_img.save(output_path)
        print("Image mirrored successfully")
        return True
    except OSError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return False

#extract text from image
def extract_image_text():
    choice = int(input("Enter \n1.For extract a single image to text or \n2.To extract multiple images to text: "))
    if choice == 1:
        one_image()
    elif choice == 2:
        # Prompt the user to enter the number of images
        num_images = int(input("Enter the number of images: "))
        multiple_images(num_images)
        
def one_image():
    # Prompt the user to enter the name of the image
    image_name = input("Enter the name of the image file: ")

    # Load the image using Pillow
    img = Image.open(image_name)

    # Convert the image to grayscale
    img = img.convert('L')

    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(img)

    # Print the extracted text
    print(text)

def multiple_images(num_images):
    with open("output.txt", "w") as f:
        for i in range(num_images):
            # Construct the image name
            image_name = f"image{i+1}.png"

            # Load the image using Pillow
            img = Image.open(image_name)

            # Convert the image to grayscale
            img = img.convert('L')

            # Use pytesseract to extract text from the image
            text = pytesseract.image_to_string(img)

            # Write the extracted text to the output file
            f.write(f"Text from {image_name}:\n")
            f.write(text)
            f.write("\n") # Add a newline after each image's text

    clean_up_output_file()

def clean_up_output_file():
    # Read the contents of the file into a string
    with open("output.txt", "r") as f:
        file_contents = f.read()

    # Clean up the file contents by replacing multiple newlines with a single newline
    file_contents = file_contents.replace("\n\n", "\n")

    # Write the cleaned up contents back to the file
    with open("output.txt", "w") as f:
        f.write(file_contents)
