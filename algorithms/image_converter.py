#file_converter.py
from PIL import Image
import os

def convert_image(input_path: str, output_path: str) -> None:
    with Image.open(input_path) as im:
        rgb_im = im.convert('RGB')  # Convert to RGB mode
        rgb_im.save(output_path)
    print(f"Conversion from {os.path.splitext(input_path)[1]} to {os.path.splitext(output_path)[1]} successful!")


