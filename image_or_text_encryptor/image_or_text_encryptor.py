from PIL import Image
import numpy as np
import os

def hide_message_in_png(image_filename, message_to_hide, key, encoded_image):
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

def main():
    try:
        choice = int(input("Menu:\n1. Hide a message in an image\n2. Decode a message from an image\n3. Hide a file in an image\n4. Decode a file from an image\n5. Encrypt a text file\n6. Decrypt a text file\n7. Encrypt text\n8. Decrypt text: "))
        if choice not in [1, 2, 3, 4, 5, 6, 7, 8]:
            print("Invalid choice. Please enter a number from 1 to 8.")
            return

        if choice in [1, 3]:
            image_filename = input("Enter the image filename: ")
            if not os.path.isfile(image_filename):
                print("Image file not found.")
                return

        if choice == 1:
            try:
                message_to_hide = input("Enter the message to hide: ")
                key = input("Enter the key: ")
                encoded_image = input("Enter the encoded image filename: ")
                success = hide_message_in_png(image_filename, message_to_hide, key, encoded_image)
                if success:
                    print("Message hidden successfully.")
            except Exception as e:
                print("An error occurred:", str(e))

        elif choice == 2:
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

        elif choice == 3:
            try:
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

        elif choice == 4:
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

        elif choice == 5:
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

        elif choice == 6:
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

        elif choice == 7:
            try:
                plaintext = input("Enter the text to encrypt: ")
                key = input("Enter the encryption key: ")
                encrypted_text = encrypt_text(plaintext, key)
                print("Encrypted text:", encrypted_text)
            except Exception as e:
                print("An error occurred:", str(e))

        elif choice == 8:
            try:
                ciphertext = input("Enter the text to decrypt: ")
                key = input("Enter the decryption key: ")
                decrypted_text = decrypt_text(ciphertext, key)
                print("Decrypted text:", decrypted_text)
            except Exception as e:
                print("An error occurred:", str(e))
    
    except ValueError:
        print("Invalid choice. Please enter a number from 1 to 8.")

main()