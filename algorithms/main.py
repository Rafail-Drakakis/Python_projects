from collatz import collatz_function
from collatz import collatz_plot
from count_lines import count_lines
from fibonacci import show_fibonacci_range
from get_fact import get_fact
from lotto_numbers import write_combinations_to_file
from timing import time_function_execution

#main.py  
def main():
    choice = int(input("Enter \n1.For count lines in a file \n2.For write all the lotto numbers in a text file \n3.For get a fact for a number \n4.For print the plot in Fibonacci sequence \n5.For print the plot for collatz function "))
    if choice == 1:
        file_name = input("Enter the file name: ")
        num_lines = count_lines(file_name)
        print(f"Number of lines in the file: {num_lines}")
        time_function_execution(count_lines, file_name)
    elif choice == 2:
        time_function_execution(write_combinations_to_file, "combinations.txt")
    elif choice == 3:
        number = int(input("Enter a number: "))
        time_function_execution(get_fact, number)
    elif choice == 4:
        first = 2
        last = int(input("Give the last number of the range: "))
        time_function_execution(show_fibonacci_range, first, last + 1)
    elif choice == 5:
        number = int(input("Give a number: "))
        sequence, count = collatz_function(number)
        collatz_plot(sequence, number)
        time_function_execution(collatz_function, number)
    else:
        print("Invalid input")
        
main()
