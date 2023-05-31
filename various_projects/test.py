import image_module, pdf_module, excel_module
import plot, Gauss_elimination, Gauss_elimination_recursive, numerical_analysis
import os, numpy as np

def test():
    #Arrays for testing
    A = np.array([[1, 2, 3], [4, 5, 6]])
    B = np.array([[7, 8], [9, 10], [11, 12]])
    #Variables for testing
    verbose = 1
    num = 5
        
    choice = int(input("Please choose an option\n1. Test the plotting functions\n2. Test the mathematical functions\n3. Test image module\n4. Test pdf module\n5. Test excel module\n6. Exit: "))
    
    if choice == 1:
        print("\n=== Plotting Functions ===\n1. Plot logarithm\n2. Plot Fibonacci\n3. Plot exponential\n4. Plot Collatz\n5. Plot Fibonacci\n6. Plot factorial: ")
        
        plot_choice = int(input("Enter the function number to test (1-6): "))
        try:
            plot_choice = int(plot_choice)
            if plot_choice == 1:
                plot.plot_logarithm(num)
            elif plot_choice == 2:
                plot.plot_fibonacci(verbose, num)
            elif plot_choice == 3:
                plot.plot_exponential(num)
            elif plot_choice == 4:
                plot.plot_collatz(num)
            elif plot_choice == 5:
                plot.plot_fibonacci(0, num)
            elif plot_choice == 6:
                plot.plot_factorial(num)
        except ValueError:
            print("Invalid input!")
    
    elif choice == 2:
        print("\n=== Mathematical Functions ===\n1. Gauss elimination (recursive)\n2. Gauss elimination\n3. Multiply matrices\n4. LDU decomposition")
        math_choice = int(input("Enter the function number to test (1-4): "))
        try:
            math_choice = int(math_choice)
            if math_choice == 1:
                Gauss_elimination_recursive.gauss_elimination_recursive(A, verbose)
            elif math_choice == 2:
                Gauss_elimination.gauss_elimination(A, verbose)
            elif math_choice == 3:
                numerical_analysis.multiply_matrices(A, B)
            elif math_choice == 4:
                numerical_analysis.ldu(A)
        except ValueError:
            print("Invalid input!")
    
    elif choice == 3:
        image_module.extract_multiple_images_text("text_from_images.txt")
        image_module.mirror_image('image.png', direction=1)
        image_module.mirror_image('image.png', direction=2)
        image_module.convert_image('image.png', 'jpeg')

        os.remove("image.jpeg")
        os.remove("image_flip.png")
        os.remove("image_mirror.png")
        os.remove("text_from_images.txt")
    
    elif choice == 4:
        pdf_module.pdf_to_word("sample.pdf")
        pdf_module.pdf_to_images("sample.pdf")
        pdf_module.collect_pdf_filenames(os.getcwd())
        pdf_module.merge_pdfs('merged.pdf')
        pdf_module.split_pdf("sample.pdf", [7, "2-5"])

        os.remove("sample_pages_7_2_3_4_5.pdf")
        os.remove("sample.docx")
        for index in range(1, 11):
            os.remove(f'page_{index}.jpg')
        os.remove("merged.pdf")
        os.remove("pdf_filenames.txt")

    elif choice == 5:
        excel_module.process_pdf("table.pdf")
        os.remove("table.xlsx")

    elif choice == 6:
        print("Exiting the menu...")

test()