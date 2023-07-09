#image_module.py

import os
import pytesseract
import PIL
from PIL import Image

def extract_images_to_text(image_paths, output_file_path):
    texts = []
    for image_path in image_paths:
        try:
            with PIL.Image.open(image_path).convert('L') as img:
                text = pytesseract.image_to_string(img, lang='eng')
                if text:
                    texts.append(os.path.basename(image_path) + "\n" + text + "\n")
        except (OSError, pytesseract.TesseractError) as e:
            texts.append(f"Error processing image {os.path.basename(image_path)}: {e}\n")

    with open(output_file_path, "w") as output_file:
        output_file.writelines(texts)

    return output_file_path

def mirror_image(input_path, direction, output_dir=None, output_format='png'):
    if not os.path.isfile(input_path):
        return f"Error: {input_path} does not exist"
    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    output_filename = os.path.splitext(os.path.basename(input_path))[0]
    try:
        with PIL.Image.open(input_path) as img:
            if direction == 1:
                mirror_img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                mirror_output_path = os.path.join(output_dir, f"{output_filename}_mirror.{output_format.lower()}")
                mirror_img.save(mirror_output_path)
                return mirror_output_path
            elif direction == 2:
                mirror_img = img.transpose(PIL.Image.FLIP_TOP_BOTTOM)
                mirror_output_path = os.path.join(output_dir, f"{output_filename}_flip.{output_format.lower()}")
                mirror_img.save(mirror_output_path)
                return mirror_output_path
            else:
                return "Invalid direction specified"
    except OSError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"

def convert_image(input_path, output_path):
    try:
        # Open the image file
        image = Image.open(input_path)

        # Convert the image to the RGB mode
        image = image.convert("RGB")

        # Create a temporary path to save the image in PNG format
        temp_path = "temp.png"

        # Save the image in PNG format
        image.save(temp_path, "PNG")

        # Load the temporary image
        temp_image = Image.open(temp_path)

        # Save the temporary image in the desired output format with specified quality
        temp_image.save(output_path, quality=95)

        # Remove the temporary image file
        os.remove(temp_path)
    except FileNotFoundError:
        print("Input file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def images_to_pdf(images, pdf_name):
    try:
        # create a new pdf file
        pdf_images = []
        for image in images:
            img = PIL.Image.open(image)
            pdf_images.append(img)

        if pdf_images:
            pdf_images[0].save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=pdf_images[1:])
        else:
            print("Error: No images found.")
    except Exception as e:
        print("Error: Failed to convert images to PDF.\nError:", str(e))