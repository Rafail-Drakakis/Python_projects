import image_module 
import os

image_module.extract_image_text('image.png') #Extract text from image.png using the default options and print to terminal

image_module.remove_background(input_path='image.png') #Example usage: remove the background of 'input.png'

image_module.mirror_image('image.png', direction=1)  #for mirror
image_module.mirror_image('image.png', direction=2)  #for flip

image_module.convert_image('image.png', 'jpeg') #convert png file to jpeg

#clean up
os.remove("image.png")
os.remove("image_flip.png")
os.remove("image_mirror.png")
os.remove("image_with_no_background.png")
