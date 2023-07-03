from PIL import Image
import numpy as np
import os

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

def encrypt_text(plaintext, key):
    """
    The `encrypt_text` function takes a plaintext and a key as input, and returns the encrypted text by
    shifting each alphabetic character in the plaintext based on the corresponding character in the key.
    
    :param plaintext: The `plaintext` parameter is the text that you want to encrypt. It can be any
    string of characters, but only alphabetic characters will be encrypted. Any non-alphabetic
    characters will remain unchanged in the encrypted text
    :param key: The "key" parameter is a string that represents the encryption key. It is used to
    determine the shift value for each character in the plaintext. The length of the key determines how
    many characters are shifted before wrapping around the alphabet
    :return: The function `encrypt_text` returns the encrypted text as a string.
    """
    encrypted_text = ""
    key_length = len(key)
    for i, char in enumerate(plaintext):
        if char.isalpha():
            key_char = key[i % key_length]
            key_shift = ord(key_char.lower()) - ord('a')
            encrypted_char = chr((ord(char.lower()) - ord('a') + key_shift) % 26 + ord('a'))
            if char.isupper():
                encrypted_char = encrypted_char.upper()
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text

def encrypt_text_file(file_name, key, output_file):
    """
    The function `encrypt_text_file` reads a text file, encrypts its contents using a given key, and
    writes the encrypted text to an output file.
    
    :param file_name: The name of the input text file that you want to encrypt. This should be a string
    that includes the file extension (e.g., "input.txt")
    :param key: The "key" parameter is the encryption key that will be used to encrypt the text. It is a
    string or a number that determines how the text will be scrambled
    :param output_file: The `output_file` parameter is the name of the file where the encrypted text
    will be written. It is the file that will be created or overwritten with the encrypted text
    :return: the FileNotFoundError exception if the file specified by file_name is not found.
    """
    try:
        with open(file_name, 'r') as file:
            plaintext = file.read()
        encrypted_text = encrypt_text(plaintext, key)
        with open(output_file, 'w') as file:
            file.write(encrypted_text)
        return FileNotFoundError
    except FileNotFoundError:
        print("File not found.")
        return True

def decrypt_text_file(file_name, key, output_file):
    """
    The function `decrypt_text_file` takes a file name, a key, and an output file name as input, reads
    the contents of the input file, decrypts the text using the provided key, and saves the decrypted
    text to the output file.
    
    :param file_name: The name of the text file that you want to decrypt
    :param key: The "key" parameter is the encryption key that is used to decrypt the text file. It is a
    string or a value that is used to reverse the encryption process and obtain the original text
    :param output_file: The `output_file` parameter is the name of the file where the decrypted text
    will be saved
    :return: a string that states the text file has been decrypted and saved as the output file.
    """
    try:
        with open(file_name, 'r') as file:
            ciphertext = file.read()
        decrypted_text = decrypt_text(ciphertext, key)
        with open(output_file, 'w') as file:
            file.write(decrypted_text)
        return f"Text file {file_name} decrypted and saved as {output_file}"
    except FileNotFoundError:
        print("File not found.")
        return None

def decrypt_text(ciphertext, key):
    """
    The `decrypt_text` function takes a ciphertext and a key as input and returns the decrypted text
    using a simple Caesar cipher decryption algorithm.
    
    :param ciphertext: The `ciphertext` parameter is the encrypted text that you want to decrypt. It
    should be a string containing alphabetic characters (both uppercase and lowercase) and possibly
    other non-alphabetic characters
    :param key: The "key" parameter is a string that represents the encryption key used to decrypt the
    ciphertext
    :return: the decrypted text.
    """
    decrypted_text = ""
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            key_char = key[i % key_length]
            key_shift = ord(key_char.lower()) - ord('a')
            decrypted_char = chr((ord(char.lower()) - ord('a') - key_shift) % 26 + ord('a'))
            if char.isupper():
                decrypted_char = decrypted_char.upper()
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

def get_valid_choice():
    """
    The function `get_valid_choice()` prompts the user to enter a number from 1 to 8 and returns the
    choice if it is valid, otherwise it displays an error message and returns None.
    :return: the user's choice as an integer if it is a valid choice (between 1 and 8), and it is
    returning None if the user's input is not a valid choice.
    """
    try:
        choice = int(input("Menu:\n1. Hide a message in an image\n2. Decode a message from an image\n3. Hide a file in an image\n4. Decode a file from an image\n5. Encrypt a text file\n6. Decrypt a text file\n7. Encrypt text\n8. Decrypt text: "))
        if choice not in [1, 2, 3, 4, 5, 6, 7, 8]:
            print("Invalid choice. Please enter a number from 1 to 8.")
            return None
        return choice
    except ValueError:
        print("Invalid choice. Please enter a number from 1 to 8.")
        return None

#Menu functions

def hide_message_in_png_menu():
    """
    The function `hide_message_in_png_menu` prompts the user to enter an image filename, a message to
    hide, a key, and an encoded image filename, and then calls the `hide_message_in_png` function to
    hide the message in the image using steganography.
    :return: nothing.
    """
    try:
        image_filename = input("Enter the image filename: ")
        if not os.path.isfile(image_filename):
            print("Image file not found.")
            return
        message_to_hide = input("Enter the message to hide: ")
        key = input("Enter the key: ")
        encoded_image = input("Enter the encoded image filename: ")
        success = hide_message_in_png(image_filename, message_to_hide, key, encoded_image)
        if success:
            print("Message hidden successfully.")
    except Exception as e:
        print("An error occurred:", str(e))

def decode_message_from_png_menu():
    """
    The function prompts the user to enter an encoded image filename and a key, then decodes a message
    from the PNG image using the provided key and prints the decoded message.
    :return: nothing.
    """
    try:
        encoded_image = input("Enter the encoded image filename: ")
        if not os.path.isfile(encoded_image):
            print("File not found.")
            return
        key = input("Enter the key: ")
        decoded_message = decode_message_from_png(encoded_image, key)
        print("Decoded message:", decoded_message)
    except Exception as e:
        print("An error occurred:", str(e))

def hide_file_in_png_menu():
    """
    The function `hide_file_in_png_menu` prompts the user to enter an image filename, a file to hide, a
    key, and an encoded image filename, and then calls the `hide_file_in_png` function to hide the file
    in the PNG image using steganography.
    :return: nothing.
    """
    try:
        image_filename = input("Enter the image filename: ")
        if not os.path.isfile(image_filename):
            print("Image file not found.")
            return
        hidden_file = input("Enter the file to hide: ")
        if not os.path.isfile(hidden_file):
            print("File not found.")
            return
        key = input("Enter the key: ")
        encoded_image = input("Enter the encoded image filename: ")
        success = hide_file_in_png(image_filename, hidden_file, key, encoded_image)
        if success:
            print("File hidden successfully.")
    except Exception as e:
        print("An error occurred:", str(e))

def decode_file_from_png_menu():
    """
    The function prompts the user to enter the filenames of an encoded image and a decoded file, then
    attempts to decode the image and save the result as the specified file.
    :return: nothing.
    """
    try:
        encoded_image = input("Enter the encoded image filename: ")
        if not os.path.isfile(encoded_image):
            print("File not found.")
            return
        decoded_file = input("Enter the decoded file filename: ")
        success = decode_file_from_png(encoded_image, decoded_file)
        if success:
            print(f"File decoded and saved as {decoded_file}")
    except Exception as e:
        print("An error occurred:", str(e))

def encrypt_text_file_menu():
    """
    The function `encrypt_text_file_menu()` prompts the user to enter an input file, an output file
    name, and an encryption key, and then calls the `encrypt_text_file()` function to encrypt the input
    file using the provided key and save the encrypted text to the output file.
    :return: nothing.
    """
    try:
        input_file = input("Enter the input file to encrypt: ")
        if not os.path.isfile(input_file):
            print("File not found.")
            return
        encrypted_output_file = input("Enter the encrypted output file filename: ")
        key = input("Enter the encryption key: ")
        success = encrypt_text_file(input_file, key, encrypted_output_file)
        if success:
            print(f"Text file {input_file} encrypted and saved as {encrypted_output_file}")
    except Exception as e:
        print("An error occurred:", str(e))

def decrypt_text_file_menu():
    """
    The function `decrypt_text_file_menu()` prompts the user to enter an encrypted file, a decryption
    key, and a filename for the decrypted output file, and then calls the `decrypt_text_file()` function
    to decrypt the file using the provided key.
    :return: nothing.
    """
    try:
        encrypted_file = input("Enter the encrypted file to decrypt: ")
        if not os.path.isfile(encrypted_file):
            print("File not found.")
            return
        decrypted_output_file = input("Enter the decrypted output file filename: ")
        key = input("Enter the decryption key: ")
        success = decrypt_text_file(encrypted_file, key, decrypted_output_file)
        if success:
            print(f"Text file {encrypted_file} decrypted and saved as {decrypted_output_file}")
    except Exception as e:
        print("An error occurred:", str(e))

def encrypt_text_menu():
    """
    The function `encrypt_text_menu()` prompts the user to enter a plaintext and encryption key, then
    calls the `encrypt_text()` function to encrypt the plaintext using the key, and finally prints the
    encrypted text.
    """
    try:
        plaintext = input("Enter the text to encrypt: ")
        key = input("Enter the encryption key: ")
        encrypted_text = encrypt_text(plaintext, key)
        print("Encrypted text:", encrypted_text)
    except Exception as e:
        print("An error occurred:", str(e))

def decrypt_text_menu():
    """
    The function `decrypt_text_menu` prompts the user to enter a ciphertext and a decryption key, then
    calls the `decrypt_text` function to decrypt the text and prints the decrypted text.
    """
    try:
        ciphertext = input("Enter the text to decrypt: ")
        key = input("Enter the decryption key: ")
        decrypted_text = decrypt_text(ciphertext, key)
        print("Decrypted text:", decrypted_text)
    except Exception as e:
        print("An error occurred:", str(e))

def process_choice(choice):
    """
    The function `process_choice` takes a choice as input and calls the corresponding menu function
    based on the choice.
    
    :param choice: The parameter "choice" is an integer representing the user's choice from a menu
    """
    if choice == 1:
        hide_message_in_png_menu()
    elif choice == 2:
        decode_message_from_png_menu()
    elif choice == 3:
        hide_file_in_png_menu()
    elif choice == 4:
        decode_file_from_png_menu()
    elif choice == 5:
        encrypt_text_file_menu()
    elif choice == 6:
        decrypt_text_file_menu()
    elif choice == 7:
        encrypt_text_menu()
    elif choice == 8:
        decrypt_text_menu()

def main():
    """
    The main function gets a valid choice from the user and processes it.
    """
    choice = get_valid_choice()
    if choice is not None:
        process_choice(choice)

main()