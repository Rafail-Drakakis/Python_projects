This project contains several Python files that implement search and sorting algorithms, as well as a command-line interface for testing and comparing the performance of these algorithms on user-defined or randomly generated arrays.

Files List
1.fill_list.py: defines a function fill_list() that prompts the user to enter a list of numbers and returns the resulting list.
2.searching.py: defines two search algorithms, binary_search() and linear_search(), that search a list for a target number and return the index of the target number in the list (or -1 if it is not found).
3.sorting.py: defines several sorting algorithms, including bubble_sort(), quick_sort(), insertion_sort(), merge_sort(), and selection_sort(), that sort a list of numbers in ascending order.
4.timing.py: defines a function finish_time() that measures the execution time of a given function.
5.testing.py: defines a function test_algorithm() that tests the performance of a given sorting algorithm on a given list of numbers.
6.main.py: provides a command-line interface that allows the user to choose between searching and sorting a list of numbers, and prompts them for the necessary input based on their choice.

Usage
To use the command-line interface, simply run the main.py file in your terminal or command prompt. You will be prompted to choose between searching and sorting a list of numbers, and to enter the necessary input based on your choice. The program will then execute the appropriate search or sorting algorithm and display the results.

For searching, you will be prompted to enter a list of numbers, a target number to search for, and a search algorithm to use. For sorting, you can either enter a list of numbers or generate a random list of numbers of a specified length, and then choose a sorting algorithm to use.

Requirements
This project requires Python 3.x to be installed on your system and the time library.
