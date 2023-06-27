from PIL import Image
import numpy as np
import io

# Inject the Secret Message into an Image (PNG)
def png_image_injector(image_filename):
    message_to_hide = "This is my secret message!"
    image = Image.open(image_filename)
    width, height = image.size
    img_arr = np.array(list(image.getdata()))

    if image.mode == "P":
        print("Not supported")
        exit()

    channels = 4 if image.mode == 'RGBA' else 3

    pixels = img_arr.size // channels

    stop_indicator = "$NEURAL$"
    stop_indicator_length = len(stop_indicator)

    message_to_hide += stop_indicator

    byte_message = ''.join(f"{ord(c):08b}" for c in message_to_hide)
    bits = len(byte_message)

    if bits > pixels:
        print("Not enough space")
    else:
        index = 0
        for i in range(pixels):
            for j in range(0, 3):
                if index < bits:
                    img_arr[i][j] = int(bin(img_arr[i][j])[2:-1] + byte_message[index], 2)
                    index += 1

    img_arr = img_arr.reshape((height, width, channels))
    result = Image.fromarray(img_arr.astype('uint8'), image.mode)
    result.save('encoded.png')

# Decoding the Secret Message from an Image (PNG format)
def png_message_decoder(image_filename):
    image = Image.open(image_filename)
    img_arr = np.array(list(image.getdata()))
    channels = 4 if image.mode == 'RGBA' else 3
    pixels = img_arr.size // channels

    secret_bits = [bin(img_arr[i][j])[-1] for i in range(pixels) for j in range(0, 3)]
    secret_bits = [secret_bits[i:i+8] for i in range(0, len(secret_bits), 8)]

    secret_message = [chr(int(''.join(secret_bits[i]), 2)) for i in range(len(secret_bits))]
    secret_message = ''.join(secret_message)

    stop_indicator = "$NEURAL$"

    if stop_indicator in secret_message:
        print(secret_message[:secret_message.index(stop_indicator)])
    else:
        print("Couldn't find secret message")

# Inject the Secret File into an Image (PNG)
def png_file_injector(image_filename, file_to_hide):
    image = Image.open(image_filename)
    width, height = image.size
    img_arr = np.array(list(image.getdata()))

    if image.mode == "P":
        print("Not supported")
        exit()

    channels = 4 if image.mode == 'RGBA' else 3

    pixels = img_arr.size // channels

    stop_indicator = "$NEURAL$"
    stop_indicator_length = len(stop_indicator)

    # Read the contents of the file
    with open(file_to_hide, 'rb') as file:
        file_data = file.read()

    # Convert file data to binary
    byte_message = ''.join(f"{byte:08b}" for byte in file_data)
    bits = len(byte_message)

    if bits > pixels:
        print("Not enough space")
    else:
        index = 0
        for i in range(pixels):
            for j in range(0, 3):
                if index < bits:
                    img_arr[i][j] = int(bin(img_arr[i][j])[2:-1] + byte_message[index], 2)
                    index += 1

    img_arr = img_arr.reshape((height, width, channels))
    result = Image.fromarray(img_arr.astype('uint8'), image.mode)
    result.save('encoded.png')

# Decoding the Secret File from an Image (PNG format)
def png_file_decoder(image_filename):
    image = Image.open(image_filename)
    img_arr = np.array(list(image.getdata()))
    channels = 4 if image.mode == 'RGBA' else 3
    pixels = img_arr.size // channels

    secret_bits = [bin(img_arr[i][j])[-1] for i in range(pixels) for j in range(0, 3)]
    secret_bits = [secret_bits[i:i+8] for i in range(0, len(secret_bits), 8)]

    # Convert binary data to bytes
    file_data = bytes([int(''.join(bits), 2) for bits in secret_bits])

    with open('decoded.txt', 'wb') as file:
        file.write(file_data)

    print("File decoded and saved as 'decoded.txt'")

def secret_message_menu():
    print("==== Secret Message Menu ====")
    print("1. Hide Secret Message in Image (PNG)")
    print("2. Decode Secret Message from Image (PNG)")
    print("3. Hide Secret File in Image (PNG)")
    print("4. Decode Secret File from Image (PNG)")
    print("5. Exit")

    choice = int(input("Enter your choice (1-4): "))

    if choice == 1:
        image_filename = input("Enter the image filename: ")
        png_image_injector(image_filename)
    elif choice == 2:
        image_filename = input("Enter the image filename: ")
        png_message_decoder(image_filename)
    elif choice == 3:
        image_filename = input("Enter the image filename: ")
        file_to_hide = input("Enter the filename of the secret file: ")
        png_file_injector(image_filename, file_to_hide)
    elif choice == 4:
        image_filename = input("Enter the image filename: ")
        png_file_decoder(image_filename)

# Call the function to start the menu
secret_message_menu()