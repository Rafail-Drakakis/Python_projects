import img2pdf, pytesseract, os, PIL

def extract_image_text(image_path):
    try:
        with PIL.Image.open(image_path).convert('L') as img:
            text = pytesseract.image_to_string(img, lang='eng')
            return text
    except (OSError, pytesseract.TesseractError) as e:
        return f"Error processing image {os.path.basename(image_path)}: {e}"
        return None

def extract_multiple_images_text(output_file_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    texts = []
    for entry in os.scandir(os.getcwd()):
        if entry.is_file() and any(entry.name.lower().endswith(ext) for ext in image_extensions):
            text = extract_image_text(entry.path)
            if text is not None:
                texts.append(os.path.basename(entry.path) + "\n" + text + "\n")

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

def convert_image(input_path, output_format):
    if not os.path.exists(input_path):
        return f"Error: file '{input_path}' does not exist."
    output_dir = os.path.dirname(input_path)
    output_filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{output_filename}.{output_format.lower()}")
    with PIL.Image.open(input_path) as im:
        rgb_im = im.convert('RGB')
        rgb_im.save(output_path, format=output_format.upper())
    return output_path

def main():
    #extract_multiple_images_text("text_from_images.txt")
    #mirror_image('image.png', direction=1)
    #mirror_image('image.png', direction=2)
    #convert_image('image.png', 'jpeg')

main()