import numpy as np
import matplotlib.pyplot as plt
import math

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

    plot_choice = input("Do you want to test the ploting functions? (yes/no): ")
    
    if plot_choice == "yes":
        plot_logarithm(num)
        plot_fibonacci(verbose, num)    
        plot_exponential(num)
        plot_collatz(num)
        plot_fibonacci(0, num)
        plot_factorial(num)
    
    math_choice = input("Do you want to test the mathematical functions? (yes/no): ")
    
    if math_choice == "yes":    
        gauss_elimination_recursive(A, verbose)
        gauss_elimination(A, verbose)
        multiply_matrices(A, B)
        ldu(A)

menu()