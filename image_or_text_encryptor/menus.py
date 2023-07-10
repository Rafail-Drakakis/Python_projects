import image_encryptor
import text_encryptor

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
        success = image_encryptor.hide_message_in_png(image_filename, message_to_hide, key, encoded_image)
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
        decoded_message = image_encryptor.decode_message_from_png(encoded_image, key)
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
        success = image_encryptor.hide_file_in_png(image_filename, hidden_file, key, encoded_image)
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
        success = image_encryptor.decode_file_from_png(encoded_image, decoded_file)
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
        success = text_encryptor.encrypt_text_file(input_file, key, encrypted_output_file)
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
        success = text_encryptor.decrypt_text_file(encrypted_file, key, decrypted_output_file)
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
        encrypted_text = text_encryptor.encrypt_text(plaintext, key)
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
        decrypted_text = text_encryptor.decrypt_text(ciphertext, key)
        print("Decrypted text:", decrypted_text)
    except Exception as e:
        print("An error occurred:", str(e))