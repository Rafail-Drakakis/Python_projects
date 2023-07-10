from PIL import Image
import numpy as np

def hide_message_in_png(image_filename, message_to_hide, key, encoded_image):
    """
    The function `hide_message_in_png` takes an image file, a message to hide, a key, and an output file
    name, and encodes the message into the image using the LSB (Least Significant Bit) technique.
    
    :param image_filename: The filename of the image you want to hide the message in
    :param message_to_hide: The `message_to_hide` parameter is a string that represents the message you
    want to hide in the PNG image
    :param key: The "key" parameter is a string that is used to ensure the integrity of the hidden
    message. It is appended to the end of the message before encoding it into the image. The key is
    later used to extract the message from the encoded image
    :param encoded_image: The `encoded_image` parameter is the filename or path where the encoded image
    will be saved. It is the output file that will contain the original image with the hidden message
    :return: a boolean value. It returns True if the message was successfully hidden in the image and
    saved as the encoded image file. It returns False if there was an error, such as the image file not
    being found or not enough space in the image to hide the message.
    """
    try:
        image = Image.open(image_filename)
        width, height = image.size
        img_array = np.array(image)

        if image.mode == "P":
            raise ValueError("Indexed color mode (P) is not supported")

        channels = img_array.shape[2]

        pixels = img_array.size // channels

        key_length = len(key)

        message_to_hide += key

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
        return True
    except FileNotFoundError:
        print("Image file not found.")
        return False
    except ValueError as e:
        print(str(e))
        return False

def decode_message_from_png(image_filename, key):
    """
    The function `decode_message_from_png` takes an image file and a key as input, decodes a hidden
    message from the image, and returns the message up to the occurrence of the key.
    
    :param image_filename: The image_filename parameter is the name or path of the PNG image file from
    which you want to decode the message
    :param key: The `key` parameter in the `decode_message_from_png` function is a string that
    represents the keyword or phrase that you are looking for in the decoded message. It is used to
    determine the portion of the decoded message that should be returned. If the `key` is found in the
    decoded message
    :return: The function `decode_message_from_png` returns either the decoded message (up to the
    occurrence of the key) or the string "Couldn't find the message."
    """
    try:
        image = Image.open(image_filename)
        img_array = np.array(image)
        channels = img_array.shape[2]
        pixels = img_array.size // channels

        img_array_flat = img_array.reshape(-1, channels)

        bits = [bin(img_array_flat[i][j])[-1] for i in range(pixels) for j in range(channels)]
        bits = [bits[i:i+8] for i in range(0, len(bits), 8)]

        message = [chr(int(''.join(bits[i]), 2)) for i in range(len(bits))]
        message = ''.join(message)

        if key in message:
            return message[:message.index(key)]
        else:
            return "Couldn't find the message."
    except FileNotFoundError:
        print("Image file not found.")
        return None

def hide_file_in_png(image_filename, file_to_hide, key, encoded_image):
    """
    The function `hide_file_in_png` takes an image file, a file to hide, a key, and an encoded image
    file as input, and hides the file within the image using steganography techniques.
    
    :param image_filename: The filename of the image in which you want to hide the file
    :param file_to_hide: The `file_to_hide` parameter is the name or path of the file that you want to
    hide within the PNG image
    :param key: The "key" parameter is a string that is used to encode and decode the hidden file in the
    image. It is used as a secret key to ensure that only the intended recipient can access the hidden
    file
    :param encoded_image: The `encoded_image` parameter is the filename of the resulting image file that
    will contain the hidden file
    :return: a boolean value. It returns True if the file hiding process is successful, and False if
    there is an error or exception occurs during the process.
    """
    try:
        image = Image.open(image_filename)
        width, height = image.size
        img_array = np.array(image)

        if image.mode == "P":
            raise ValueError("Indexed color mode (P) is not supported")

        channels = img_array.shape[2]

        pixels = img_array.size // channels

        key_length = len(key)

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
        return True
    except FileNotFoundError:
        print("Image or file not found.")
        return False
    except ValueError as e:
        print(str(e))
        return False

def decode_file_from_png(image_filename, decoded_file):
    """
    The function `decode_file_from_png` decodes a file from a PNG image and saves it as a separate file.
    
    :param image_filename: The image_filename parameter is the name or path of the PNG image file that
    you want to decode
    :param decoded_file: The `decoded_file` parameter is the name or path of the file where the decoded
    data will be saved
    :return: a string that indicates the status of the decoding process. If the decoding is successful
    and the file is saved, the function will return a string that says "File decoded and saved as
    [decoded_file]". If the image file is not found, the function will return None.
    """
    try:
        image = Image.open(image_filename)
        img_array = np.array(image)
        channels = img_array.shape[2]
        pixels = img_array.size // channels

        img_array_flat = img_array.reshape(-1, channels)

        bits = [bin(img_array_flat[i][j])[-1] for i in range(pixels) for j in range(channels)]
        bits = [bits[i:i+8] for i in range(0, len(bits), 8)]

        file_data = bytes([int(''.join(bits), 2) for bits in bits])

        with open(decoded_file, 'wb') as file:
            file.write(file_data)

        return f'File decoded and saved as {decoded_file}'
    except FileNotFoundError:
        print("Image file not found.")
        return None