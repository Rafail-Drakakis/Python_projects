from searching import binary_search, linear_search, search_array, finish_time
from sorting import bubble_sort, quick_sort, insertion_sort, selection_sort, merge_sort, sort_array
from fill_list import fill_list
import random

#menu.py
def menu():
    user_choice = int(input("Enter\n1.To search in an array\n2.To sort an array\n3.To operate in an array with random elements: "))

    if user_choice == 1:
        array = fill_list()
        target_number = int(input("Give the target number: "))
        search_algorithm = input("Enter \n1 for binary search\n2 for linear search: ")
        search_array(array, target_number, search_algorithm)

    elif user_choice == 2:
        array = fill_list()
        sort_algorithm = input("Enter \n1 for bubble sort\n2 for quick sort\n3 for insertion sort\n4 for merge sort\n5 for selection sort: ")
        display_sorted_list = input("Display sorted array? [y/n]: ").lower() == "y"
        sort_array(array, sort_algorithm, display_sorted_list)

    elif user_choice == 3:
        array_length = int(input("Enter the length of the random array: "))
        array = [random.randint(0, 100) for _ in range(array_length)]
        print(f"Sorting a random array of {array_length} elements")

        sort_algorithm = input("Enter \n1 for bubble sort\n2 for quick sort\n3 for insertion sort\n4 for merge sort\n5 for selection sort: ")
        display_sorted_array = input("Display sorted array? [y/n]: ").lower() == "y"
        sort_array(array, sort_algorithm, display_sorted_array)

menu()