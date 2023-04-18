import pytesseract
from PIL import Image, ImageOps
from rembg import remove
import os

#extract text from image
def extract_image_text(image_path=None, lang='eng', save_to_file=False, output_path=None):
    if image_path is None:
        image_path = input("Enter the name of the image file: ")
    # Check that the image file exists
    if not os.path.exists(image_path):
        print(f"Error: {image_path} does not exist")
        return
    # Load the image using Pillow
    try:
        img = Image.open(image_path)
    except OSError as e:
        print(f"Error loading image: {e}")
        return
    # Convert the image to grayscale
    img = img.convert('L')
    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(img, lang=lang)

    # Print or save the extracted text
    if save_to_file:
        if output_path is None:
            output_path = os.path.splitext(image_path)[0] + ".txt"
        with open(output_path, 'w') as f:
            f.write(text)
        print(f"Text saved to {output_path}")
    else:
        print(text)
        
#remove baground
def remove_background(input_path=None, output_path=None):
    if input_path is None:
        input_path = input("Enter the input file name: ")
    if output_path is None:
        output_dir = os.path.dirname(input_path)
        output_filename, output_ext = os.path.splitext(os.path.basename(input_path))
        output_format = output_ext[1:]
        output_path = os.path.join(output_dir, f"{output_filename}_with_no_baground.{output_format}")
    try:
        with Image.open(input_path) as image_input:
            output = remove(image_input)
            output.save(output_path)
        print(f"Background removed successfully")
    except OSError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

#mirror image
def mirror_image(input_path: str, direction: int, output_dir: str = None, output_format: str = 'png') -> None:
    if not os.path.isfile(input_path):
        print(f"Error: {input_path} does not exist")
        return    
    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    output_filename = os.path.splitext(os.path.basename(input_path))[0]
    try:
        with Image.open(input_path) as img:
            if direction == 1:
                mirror_img = ImageOps.mirror(img)
                mirror_output_path = os.path.join(output_dir, f"{output_filename}_mirror.{output_format.lower()}")
                mirror_img.save(mirror_output_path)
                print(f"Image mirrored successfully")
            elif direction == 2:
                mirror_img = ImageOps.flip(img)
                mirror_output_path = os.path.join(output_dir, f"{output_filename}_flip.{output_format.lower()}")
                mirror_img.save(mirror_output_path)
                print(f"Image fliped successfully")
            else:
                print("Invalid direction specified")
                return
    except OSError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

#convert image
def convert_image(input_path: str, output_format: str) -> None:
    if not os.path.exists(input_path):
        print(f"Error: file '{input_path}' does not exist.")
        return
    output_dir = os.path.dirname(input_path)
    output_filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{output_filename}.{output_format.lower()}")
    with Image.open(input_path) as im:
        rgb_im = im.convert('RGB')  # Convert to RGB mode
        rgb_im.save(output_path, format=output_format.upper())
    print(f"Conversion from {os.path.splitext(input_path)[1][1:].upper()} to {output_format.upper()}")
