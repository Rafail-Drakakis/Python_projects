import menus

def main():
    try:
        choice = int(input("Menu:\n1. Hide a message in an image\n2. Decode a message from an image\n3. Hide a file in an image\n4. Decode a file from an image\n5. Encrypt a text file\n6. Decrypt a text file\n7. Encrypt text\n8. Decrypt text: "))
        if choice not in [1, 2, 3, 4, 5, 6, 7, 8]:
            print("Invalid choice. Please enter a number from 1 to 8.")
            exit(0)
        if choice == 1:
            menus.hide_message_in_png_menu()
        elif choice == 2:
            menus.decode_message_from_png_menu()
        elif choice == 3:
            menus.hide_file_in_png_menu()
        elif choice == 4:
            menus.decode_file_from_png_menu()
        elif choice == 5:
            menus.encrypt_text_file_menu()
        elif choice == 6:
            menus.decrypt_text_file_menu()
        elif choice == 7:
            menus.encrypt_text_menu()
        elif choice == 8:
            menus.decrypt_text_menu()
    except ValueError:
        print("Invalid choice. Please enter a number from 1 to 8.")
        exit(0)
        
if __name__ == "__main__":
    main()