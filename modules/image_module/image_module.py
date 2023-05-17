import pytesseract
import PIL
import rembg
import os

def extract_multiple_images_text(filenames_file):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    with open(filenames_file, "w") as output_file:
        for entry in os.scandir(os.getcwd()):
            if entry.is_file() and any(entry.name.lower().endswith(ext) for ext in image_extensions):
                image_path = entry.path
                try:
                    img = PIL.Image.open(image_path)
                    img = img.convert('L')
                    text = pytesseract.image_to_string(img, lang='eng')
                    output_file.write(entry.name + "\n")
                    output_file.write(text + "\n")
                except (OSError, pytesseract.TesseractError) as e:
                    print(f"Error processing image {entry.name}: {e}")

    print(f'Text extracted and saved to {filenames_file} file.')
        
def remove_background(input_path=None, output_path=None):
    if input_path is None:
        input_path = input("Enter the input file name: ")
    if output_path is None:
        output_dir = os.path.dirname(input_path)
        output_filename, output_ext = os.path.splitext(os.path.basename(input_path))
        output_format = output_ext[1:]
        output_path = os.path.join(output_dir, f"{output_filename}_with_no_background.{output_format}")
    try:
        with PIL.Image.open(input_path) as image_input:
            image_rgba = image_input.convert("RGBA")
            rgba_data = image_rgba.load()
            width, height = image_rgba.size
            for y in range(height):
                for x in range(width):
                    r, g, b, a = rgba_data[x, y]
                    if a == 0:
                        rgba_data[x, y] = (255, 255, 255, 255)
            output = PIL.Image.alpha_composite(PIL.Image.new('RGBA', image_rgba.size, (255, 255, 255, 255)), image_rgba)
            output = output.convert("RGB")
            output.save(output_path, format=output_format)
        print("Background removed successfully.")
    except OSError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def mirror_image(input_path: str, direction: int, output_dir: str = None, output_format: str = 'png') -> None:
    if not os.path.isfile(input_path):
        print(f"Error: {input_path} does not exist")
        return    
    if output_dir is None:
        output_dir = os.path.dirname(input_path)
    output_filename = os.path.splitext(os.path.basename(input_path))[0]
    try:
        with PIL.Image.open(input_path) as img:
            if direction == 1:
                mirror_img = PIL.ImageOps.mirror(img)
                mirror_output_path = os.path.join(output_dir, f"{output_filename}_mirror.{output_format.lower()}")
                mirror_img.save(mirror_output_path)
                print(f"Image mirrored successfully")
            elif direction == 2:
                mirror_img = PIL.ImageOps.flip(img)
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

def convert_image(input_path: str, output_format: str) -> None:
    if not os.path.exists(input_path):
        print(f"Error: file '{input_path}' does not exist.")
        return
    output_dir = os.path.dirname(input_path)
    output_filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{output_filename}.{output_format.lower()}")
    with PIL.Image.open(input_path) as im:
        rgb_im = im.convert('RGB')  # Convert to RGB mode
        rgb_im.save(output_path, format=output_format.upper())
    print(f"Conversion from {os.path.splitext(input_path)[1][1:].upper()} to {output_format.upper()}")
 
def main():
    extract_multiple_images_text("text_from_images.txt")
    remove_background('image.png') # Remove the background of 'image.png'
    mirror_image('image.png', direction = 1) # Mirror the image horizontally
    mirror_image('image.png', direction = 2) # Flip the image vertically
    convert_image('image.png', 'jpeg') # Convert png file to jpeg
    os.remove("image.jpeg") 
    os.remove("image_flip.png") 
    os.remove("image_mirror.png")
    os.remove("image_with_no_background.png")
    os.remove("text_from_images.txt")
    
main() # Test function