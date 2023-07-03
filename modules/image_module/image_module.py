import img2pdf, pytesseract, os, PIL

def extract_images_to_text(image_paths, output_file_path):
    """
    The function `extract_images_to_text` takes a list of image paths, extracts text from each image
    using Tesseract OCR, and writes the extracted text along with the image filename to an output file.
    
    :param image_paths: image_paths is a list of file paths to the images that you want to extract text
    from. Each image should be in a format that can be opened by PIL (Python Imaging Library)
    :param output_file_path: The output_file_path parameter is the path where the extracted text will be
    saved. It should be a string representing the file path, including the file name and extension. For
    example, "C:/output/text.txt" or "output/text.txt"
    :return: the file path of the output file.
    """
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
    """
    The `mirror_image` function takes an input image file, a direction (1 for left-right mirror, 2 for
    top-bottom mirror), and optional output directory and format, and returns the path of the mirrored
    image file.
    
    :param input_path: The path to the input image file that you want to mirror
    :param direction: The `direction` parameter specifies the type of mirror image transformation to be
    applied. It can take one of the following values:
    :param output_dir: The `output_dir` parameter is an optional parameter that specifies the directory
    where the mirrored image will be saved. If no `output_dir` is provided, the function will use the
    directory of the input image as the output directory
    :param output_format: The `output_format` parameter specifies the format of the output image file.
    By default, it is set to 'png', but you can change it to any supported image format such as 'jpg',
    'jpeg', 'gif', etc, defaults to png (optional)
    :return: the path of the mirrored image if successful, or an error message if there is an issue with
    the input file or the mirroring process.
    """
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
    """
    The function `convert_image` takes an input image file path and an output format, converts the image
    to the specified format, and returns the output file path.
    
    :param input_path: The input_path parameter is the path to the image file that you want to convert.
    It should be a string representing the file path, including the file name and extension. For
    example, "C:/images/image.jpg" or "/home/user/images/image.png"
    :param output_format: The `output_format` parameter is a string that specifies the desired format of
    the output image. It can be any valid image format supported by the PIL library, such as "JPEG",
    "PNG", "BMP", etc
    :return: the output path of the converted image.
    """
    if not os.path.exists(input_path):
        return f"Error: file '{input_path}' does not exist."
    output_dir = os.path.dirname(input_path)
    output_filename = input("Enter the output filename: ")
    output_path = os.path.join(output_dir, f"{output_filename}.{output_format.lower()}")
    with PIL.Image.open(input_path) as im:
        rgb_im = im.convert('RGB')
        rgb_im.save(output_path, format=output_format.upper())
    return output_path

def images_to_pdf(images, pdf_name):
    """
    The function `images_to_pdf` converts a list of images into a PDF file.
    
    :param images: A list of file paths to the images that you want to convert to a PDF
    :param pdf_name: The name of the PDF file that will be created
    """
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
    """
    The main function performs various image processing tasks such as extracting text from images,
    mirroring images, converting image formats, and creating PDFs from images.
    """
    extract_images_to_text(["image.png"], 'output.txt')
    mirror_image('image.png', direction=1)
    mirror_image('image.png', direction=2)
    convert_image('image.png', 'jpeg')
    images_to_pdf(["image.png"], 'output.pdf')
    
main()