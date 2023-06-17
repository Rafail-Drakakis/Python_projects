import img2pdf
import pytesseract
import os
import PIL
import tkinter
from tkinter import filedialog, messagebox

def extract_multiple_images_text():
    image_paths = filedialog.askopenfilenames(title="Select Image (or images)")
    if image_paths:
        for image_path in image_paths:
            input_ext = os.path.splitext(image_path)[1][1:].lower()
            if input_ext not in ['png', 'jpg', 'jpeg', 'gif']:
                messagebox.showerror("Error", f"Invalid image file: {image_path}")
                return

        output_file_path = filedialog.asksaveasfilename(title="Save Text", defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if output_file_path:
            with open(output_file_path, "w") as output_file:
                for image_path in image_paths:
                    image_filename = os.path.basename(image_path)
                    with PIL.Image.open(image_path).convert('L') as img:
                        text = pytesseract.image_to_string(img, lang='eng')
                        output_file.write(image_filename + '\n')
                        output_file.write(text + '\n')
                messagebox.showinfo("Conversion complete")

def convert_image():
    input_path = filedialog.askopenfilename(title="Select Image")
    if input_path:
        input_ext = os.path.splitext(input_path)[1][1:].lower()
        if input_ext not in ['png', 'jpg', 'jpeg', 'gif']:
            messagebox.showerror("Error", f"Invalid output format: {input_ext}")
            return
        output_file_path = filedialog.asksaveasfilename(title="Save Converted Image", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("GIF Files", "*.gif")])
        if output_file_path:
            output_format = os.path.splitext(output_file_path)[1][1:].lower()
            if output_format not in ['png', 'jpg', 'jpeg', 'gif']:
                messagebox.showerror("Error", f"Invalid output format: {output_format}")
                return
            try:
                with PIL.Image.open(input_path) as im:
                    rgb_im = im.convert('RGB')
                    rgb_im.save(output_file_path, format=output_format)
                    messagebox.showinfo("Conversion complete")
            except PIL.UnidentifiedImageError:
                messagebox.showerror("Error", "Invalid image file")
                return

def mirror_image():
    input_path = filedialog.askopenfilename(title="Select Image")
    if input_path:
        try:
            with PIL.Image.open(input_path) as img:
                direction = "horizontal"  # Specify "horizontal" or "vertical"
                output_dir = filedialog.askdirectory(title="Select Output Directory")
                output_filename = os.path.splitext(os.path.basename(input_path))[0]
                output_format = os.path.splitext(os.path.basename(input_path))[1][1:].lower()
                mirror_img = img.transpose(PIL.Image.FLIP_LEFT_RIGHT)
                mirror_output_path = os.path.join(output_dir, f"{output_filename}_mirror.{output_format}")
                mirror_img.save(mirror_output_path)
                messagebox.showinfo("Conversion complete")
                return mirror_output_path
        except PIL.UnidentifiedImageError:
            messagebox.showerror("Error", "Invalid image file")

def flip_image():
    input_path = filedialog.askopenfilename(title="Select Image")
    if input_path:
        try:
            with PIL.Image.open(input_path) as img:
                direction = "vertical"  # Specify "horizontal" or "vertical"
                output_dir = filedialog.askdirectory(title="Select Output Directory")
                output_filename = os.path.splitext(os.path.basename(input_path))[0]
                output_format = os.path.splitext(os.path.basename(input_path))[1][1:].lower()
                flip_img = img.transpose(PIL.Image.FLIP_TOP_BOTTOM)
                flip_output_path = os.path.join(output_dir, f"{output_filename}_flip.{output_format}")
                flip_img.save(flip_output_path)
                messagebox.showinfo("Conversion complete")
                return flip_output_path
        except PIL.UnidentifiedImageError:
            messagebox.showerror("Error", "Invalid image file")

# The app frame
app = tkinter.Tk()
app.geometry("520x300")
app.title("Image Operator")

# Extract text from multiple images button
extract_multiple_images_text_button = tkinter.Button(app, text="Extract text from multiple images", command=extract_multiple_images_text)
extract_multiple_images_text_button.pack(padx=10, pady=10)

# Mirror image button
mirror_image_button = tkinter.Button(app, text="Mirror image", command=mirror_image)
mirror_image_button.pack(padx=10, pady=10)

# Flip image button
flip_image_button = tkinter.Button(app, text="Flip image", command=flip_image)
flip_image_button.pack(padx=10, pady=10)

# Convert image button
convert_image_button = tkinter.Button(app, text="Convert image", command=convert_image)
convert_image_button.pack(padx=10, pady=10)

app.mainloop()