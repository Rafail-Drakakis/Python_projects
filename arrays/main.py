import random
import time
from fill_list import fill_list
from searching import binary_search
from searching import linear_search
from sorting import bubble_sort
from sorting import quick_sort
from sorting import insertion_sort
from sorting import merge_sort
from sorting import selection_sort
from timing import finish_time

#main.py
def main():
    user_choice = int(input("Enter\n1.To search in an array\n2.To sort an array\n3.For a random array: "))

    if user_choice == 1:
        array = fill_list()
        target_number = int(input("Give the target number: "))
        search_algorithm_choice = int(input("Enter\n1.For binary search\n2.For linear search: "))
        algorithm_map = {1: ("Binary Search", binary_search), 2: ("Linear Search", linear_search)}
        algorithm_name, algorithm_func = algorithm_map.get(search_algorithm_choice, (None, None))
        if algorithm_name:
            finish_time(algorithm_func, algorithm_name, array, target_number)
    elif user_choice == 2:
        array = fill_list()
    elif user_choice == 3:
        array_length = int(input("Enter the length of the random array: "))
        array = [random.randint(0, 1000) for _ in range(array_length)]
        print(f"Sorting a random array of {array_length} elements")

        sorting_algorithm_choice = int(input("Enter\n1.Bubble sort\n2.Quick sort\n3.Insertion sort\n4.Merge sort\n5.Selection sort: "))
        algorithm_map = {1: ("Bubble Sort", bubble_sort), 2: ("Quick Sort", quick_sort),
                         3: ("Insertion Sort", insertion_sort), 4: ("Merge Sort", merge_sort),
                         5: ("Selection Sort", selection_sort)}
        algorithm_name, algorithm_func = algorithm_map.get(sorting_algorithm_choice, (None, None))
        if algorithm_name:
            if input("Display sorted array? [y/n]: ").lower() == "y":
                finish_time(algorithm_func, algorithm_name, array)
            else:
                start_time = time.time()
                algorithm_func(array)
                end_time = time.time()
                execution_time = end_time - start_time
                print(f"The {algorithm_name} algorithm took {execution_time:.6f} seconds for an array of length {len(array)}")
main()

