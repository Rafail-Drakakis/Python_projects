#main.py
import sub_menu

def menu():
    try:
        choice = int(input("1. Convert Images to Text\n2. Mirror Image\n3. Convert Image to another image format\n4. Convert Images to PDF\n5. Merge PDF Files\n6. Convert PDF to Word \n7. Convert PDF to Images\n8. Split PDF\n9. Convert PDF to Excel\nEnter your choice: "))
        if choice not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            print("Enter a number from 1 to 8")
            exit()

        if choice == 1:
            sub_menu.extract_images_to_text_menu()
        elif choice == 2:
            sub_menu.mirror_image_menu()
        elif choice == 3:
            sub_menu.convert_image_menu()
        elif choice == 4:
            sub_menu.images_to_pdf_menu()
        elif choice == 5:
            sub_menu.merge_pdf_files_menu()
        elif choice == 6:
            sub_menu.pdf_to_word_menu()
        elif choice == 7:
            sub_menu.pdf_to_images_menu()
        elif choice == 8:
            sub_menu.split_pdf_menu()
        elif choice == 9:
            sub_menu.convert_pdf_to_excel_menu()
    except ValueError:
        print("Enter an integer")
        exit(0)

if __name__ == "__main__":
    menu()