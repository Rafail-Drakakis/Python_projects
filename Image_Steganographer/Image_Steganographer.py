from PIL import Image
import numpy as np

def hide_message_in_png(image_filename, message_to_hide, stop_indicator, encoded_image):
    try:
        image = Image.open(image_filename)
        width, height = image.size
        img_array = np.array(image)

        if image.mode == "P":
            raise ValueError("Indexed color mode (P) is not supported")

        channels = img_array.shape[2]

        pixels = img_array.size // channels

        stop_indicator_length = len(stop_indicator)

        message_to_hide += stop_indicator

        byte_message = ''.join(f"{ord(c):08b}" for c in message_to_hide)
        message_length = len(byte_message)

        if message_length > pixels:
            raise ValueError("Not enough space in the image to hide the message")

        img_array_flat = img_array.reshape(-1, channels)

        index = 0
        for i in range(pixels):
            for j in range(channels):
                if index < message_length:
                    img_array_flat[i][j] = int(bin(img_array_flat[i][j])[2:-1] + byte_message[index], 2)
                    index += 1

        img_array = img_array_flat.reshape(height, width, channels)

        result = Image.fromarray(img_array.astype('uint8'), image.mode)
        result.save(encoded_image)
        print("Message hidden successfully.")
    except FileNotFoundError:
        print("Image file not found.")
    except ValueError as e:
        print(str(e))

def decode_message_from_png(image_filename, stop_indicator):
    try:
        image = Image.open(image_filename)
        img_array = np.array(image)
        channels = img_array.shape[2]
        pixels = img_array.size // channels

        img_array_flat = img_array.reshape(-1, channels)

        secret_bits = [bin(img_array_flat[i][j])[-1] for i in range(pixels) for j in range(channels)]
        secret_bits = [secret_bits[i:i+8] for i in range(0, len(secret_bits), 8)]

        secret_message = [chr(int(''.join(secret_bits[i]), 2)) for i in range(len(secret_bits))]
        secret_message = ''.join(secret_message)

        if stop_indicator in secret_message:
            print(secret_message[:secret_message.index(stop_indicator)])
        else:
            print("Couldn't find the secret message.")
    except FileNotFoundError:
        print("Image file not found.")

def hide_file_in_png(image_filename, file_to_hide, stop_indicator, encoded_image):
    try:
        image = Image.open(image_filename)
        width, height = image.size
        img_array = np.array(image)

        if image.mode == "P":
            raise ValueError("Indexed color mode (P) is not supported")

        channels = img_array.shape[2]

        pixels = img_array.size // channels

        stop_indicator_length = len(stop_indicator)

        with open(file_to_hide, 'rb') as file:
            file_data = file.read()

        byte_message = ''.join(f"{byte:08b}" for byte in file_data)
        message_length = len(byte_message)

        if message_length > pixels:
            raise ValueError("Not enough space in the image to hide the file")

        img_array_flat = img_array.reshape(-1, channels)

        index = 0
        for i in range(pixels):
            for j in range(channels):
                if index < message_length:
                    img_array_flat[i][j] = int(bin(img_array_flat[i][j])[2:-1] + byte_message[index], 2)
                    index += 1

        img_array = img_array_flat.reshape(height, width, channels)

        result = Image.fromarray(img_array.astype('uint8'), image.mode)
        result.save(encoded_image)
        print("File hidden successfully.")
    except FileNotFoundError:
        print("Image file or secret file not found.")
    except ValueError as e:
        print(str(e))

def decode_file_from_png(image_filename, decoded_file):
    try:
        image = Image.open(image_filename)
        img_array = np.array(image)
        channels = img_array.shape[2]
        pixels = img_array.size // channels

        img_array_flat = img_array.reshape(-1, channels)

        secret_bits = [bin(img_array_flat[i][j])[-1] for i in range(pixels) for j in range(channels)]
        secret_bits = [secret_bits[i:i+8] for i in range(0, len(secret_bits), 8)]

        file_data = bytes([int(''.join(bits), 2) for bits in secret_bits])

        with open(decoded_file, 'wb') as file:
            file.write(file_data)

        print(f'File decoded and saved as {decoded_file}')
    except FileNotFoundError:
        print("Image file not found.")

def menu():
    print("1. Hide Secret Message in PNG Image")
    print("2. Decode Secret Message from PNG Image")
    print("3. Hide Secret File in PNG Image")
    print("4. Decode Secret File from PNG Image")

    choice = int(input("Enter your choice: "))
    image_filename = input("Enter the image filename: ")

    if choice == 1:
        stop_indicator = input("Enter your key: ")
        message_to_hide = input("Enter your text: ")
        encoded_image = input("Enter the filename of the encoded image: ")
        hide_message_in_png(image_filename, message_to_hide, stop_indicator, encoded_image)
    elif choice == 2:
        stop_indicator = input("Enter your key: ")
        decode_message_from_png(image_filename, stop_indicator)
    elif choice == 3:
        file_to_hide = input("Enter the filename of the secret file: ")
        encoded_image = input("Enter the filename of the encoded image: ")
        stop_indicator = input("Enter your key: ")
        hide_file_in_png(image_filename, file_to_hide, stop_indicator, encoded_image)
    elif choice == 4:
        decoded_file = input("Enter the output filename: ")
        decode_file_from_png(image_filename, decoded_file)

menu()