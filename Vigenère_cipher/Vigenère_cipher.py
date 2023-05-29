def encrypt(plaintext, key):
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

def decrypt(ciphertext, key):
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
    choice = int(input("Press:\n1. To encrypt a message or\n2. To decrypt a message: "))
    file_name = input("Enter the file name: ")
    key = input("Enter the encryption key: ")

    if choice == 1:
        # Encrypt the plaintext
        with open(file_name, "r") as file:
            plaintext = file.read()
        encrypted_text = encrypt(plaintext, key)
        output_file = "encrypted.txt"
        mode = "encrypted"
    elif choice == 2:
        # Decrypt the ciphertext
        with open(file_name, "r") as file:
            ciphertext = file.read()
        decrypted_text = decrypt(ciphertext, key)
        output_file = "decrypted.txt"
        mode = "decrypted"
    else:
        print("Invalid choice. Exiting...")
        return

    with open(output_file, "w") as file:
        file.write(encrypted_text) if mode == "encrypted" else file.write(decrypted_text)

    print(f"File {file_name} {mode} successfully in {output_file}.")

main()