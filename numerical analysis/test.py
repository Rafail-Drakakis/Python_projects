import numpy as np
from plot import plot_logarithm, plot_fibonacci, plot_exponential, plot_collatz, plot_fibonacci, plot_factorial
from Gauss_elimination import gauss_elimination
from Gauss_elimination_recursive import gauss_elimination_recursive
from numerical_analysis import multiply_matrices, ldu

#test.py
def variables():
    #Arrays for testing
    A = np.array([[1, 2, 3], [4, 5, 6]])
    B = np.array([[7, 8], [9, 10], [11, 12]])
    #Variables for testing
    verbose = 1
    num = 5
    return A, B, verbose, num

def menu():
    A, B, verbose, num = variables()
    
    choice = int(input("Please choose an option\n1. Test the plotting functions\n2. Test the mathematical functions\n3. Exit: "))
    
    if choice == 1:
        print("\n=== Plotting Functions ===\n1. Plot logarithm\n2. Plot Fibonacci\n3. Plot exponential\n4. Plot Collatz\n5. Plot Fibonacci\n6. Plot factorial: ")
        
        plot_choice = int(input("Enter the function number to test (1-6): "))
        try:
            plot_choice = int(plot_choice)
            if plot_choice == 1:
                plot_logarithm(num)
            elif plot_choice == 2:
                plot_fibonacci(verbose, num)
            elif plot_choice == 3:
                plot_exponential(num)
            elif plot_choice == 4:
                plot_collatz(num)
            elif plot_choice == 5:
                plot_fibonacci(0, num)
            elif plot_choice == 6:
                plot_factorial(num)
        except ValueError:
            print("Invalid input!")
    
    elif choice == 2:
        print("\n=== Mathematical Functions ===\n1. Gauss elimination (recursive)\n2. Gauss elimination\n3. Multiply matrices\n4. LDU decomposition")
        math_choice = int(input("Enter the function number to test (1-4): "))
        try:
            math_choice = int(math_choice)
            if math_choice == 1:
                gauss_elimination_recursive(A, verbose)
            elif math_choice == 2:
                gauss_elimination(A, verbose)
            elif math_choice == 3:
                multiply_matrices(A, B)
            elif math_choice == 4:
                ldu(A)
        except ValueError:
            print("Invalid input!")
    
    elif choice == 3:
        print("Exiting the menu...")
    
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

menu()