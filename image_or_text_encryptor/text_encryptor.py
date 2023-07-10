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