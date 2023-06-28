import img2pdf, pytesseract, os, PIL

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

def main():
    extract_images_to_text(["image.png"], 'output.pdf')
    mirror_image('image.png', direction=1)
    mirror_image('image.png', direction=2)
    convert_image('image.png', 'jpeg')
    images_to_pdf(["image.png"], 'output.pdf')
    
main()