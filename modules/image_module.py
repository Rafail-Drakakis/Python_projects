import img2pdf, pytesseract
from PIL import Image
import os

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

    with open(output_file_path, "w") as output_file:
        for entry in os.scandir(os.getcwd()):
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

# testing function (with an existing image.png file)
def test():
    extract_multiple_images_text("text_from_images.txt")
    mirror_image('image.png', direction = 1)
    mirror_image('image.png', direction = 2)
    convert_image('image.png', 'jpeg')