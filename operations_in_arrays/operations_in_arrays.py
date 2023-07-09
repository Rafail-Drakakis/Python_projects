import random
import time

#sorting.py
def sort_array(array, sort_algorithm, display_sorted_list):
    algorithm_map = {'1': ('Bubble Sort', bubble_sort), '2': ('Quick Sort', quick_sort),
                     '3': ('Insertion Sort', insertion_sort), '4': ('Merge Sort', merge_sort),
                     '5': ('Selection Sort', selection_sort)}
    algorithm_name, algorithm_func = algorithm_map.get(sort_algorithm, (None, None))
    if algorithm_name:
        if display_sorted_list:
            finish_time(algorithm_func, algorithm_name, array)
        else:
            start_time = time.time()
            algorithm_func(array)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"The {algorithm_name} algorithm took {execution_time:.6f} seconds for an array of length {len(array)}")

def bubble_sort(array):
  # Set a flag to True to start the loop
  flag = True
  
  # Keep looping until the flag is False
  while flag:
    # Set the flag to False
    flag = False
    
    # Loop through the list and compare adjacent elements
    for i in range(len(array) - 1):
      if array[i] > array[i+1]:
        # Swap the elements if they are in the wrong order
        array[i], array[i+1] = array[i+1], array[i]
        # Set the flag to True to indicate that a swap occurred
        flag = True
 
  # Return the sorted list
  return array

def quick_sort(array):
    stack = [(0, len(array) - 1)]
    while stack:
        low, high = stack.pop()
        if low >= high:
            continue
        pivot = array[high]
        i = low - 1
        for j in range(low, high):
            if array[j] < pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
        array[i+1], array[high] = array[high], array[i+1]
        stack.append((low, i))
        stack.append((i+2, high))
    return array
    
def insertion_sort(array):
  # Traverse through 1 to len(array)
  for i in range(1, len(array)):
      key = array[i]
      # Move elements of array[0..i-1], that are
      # greater than key, to one position ahead
      # of their current position
      j = i - 1
      while j >= 0 and key < array[j]:
        array[j + 1] = array[j]
        j -= 1
      array[j + 1] = key
  return array

def merge_sort(array):
  # If the array has fewer than 2 elements, it is already sorted
  if len(array) < 2:
    return array
  # Split the array into left and right halves
  mid = len(array) // 2
  left = array[:mid]
  right = array[mid:]
  # Recursively sort the two halves
  left = merge_sort(left)
  right = merge_sort(right)
  # Initialize variables to track the current position in each half
  i = j = 0
  # Initialize an empty result array
  result = []
  # While there are still elements in both halves
  while i < len(left) and j < len(right):
    # Compare the elements at the current positions
    # and append the smaller one to the result array
    if left[i] < right[j]:
      result.append(left[i])
      i += 1
    else:
      result.append(right[j])
      j += 1
  # Append any leftover elements from the left half
  result.extend(left[i:])
  # Append any leftover elements from the right half
  result.extend(right[j:])
  # Return the result array
  return result

def selection_sort(array):
  # Traverse through all array elements
  for i in range(len(array)):
    # Find the minimum element in remaining
    # unsorted array
    min_idx = i
    for j in range(i + 1, len(array)):
      if array[min_idx] > array[j]:
        min_idx = j
    # Swap the found minimum element with
    # the first element
    array[i], array[min_idx] = array[min_idx], array[i]
  return array

#searching.py
def finish_time(function, algorithm_name, *positional_args, **keyword_args):
    start_time = time.time()
    result = function(*positional_args, **keyword_args)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The {algorithm_name} algorithm took {execution_time:.6f} seconds \n{algorithm_name}, {result}")
    return result

def search_array(array, target_number, search_algorithm):
    algorithm_map = {'1': ('Binary Search', binary_search), '2': ('Linear Search', linear_search)}
    algorithm_name, algorithm_func = algorithm_map.get(search_algorithm, (None, None))
    if algorithm_name:
        finish_time(algorithm_func, algorithm_name, array, target_number)

def binary_search(array, target_number):
    # Return -1 if the list is empty
    if len(array) == 0:
        return -1
    
    # Find the middle index
    mid = len(array) // 2
    
    # If the middle element is the target_number, return its index
    if array[mid] == target_number:
        return mid
    
    # If the target_number is less than the middle element, search the left half
    elif target_number < array[mid]:
        result = binary_search(array[:mid], target_number)
        # Return the index if the target_number was found
        if result != -1:
            return result
    
    # If the target_number is greater than the middle element, search the right half
    else:
        result = binary_search(array[mid+1:], target_number)
        # Return the index if the target_number was found
        if result != -1:
            return mid + 1 + result
    
    # Return -1 if the target_number was not found
    return -1

def linear_search(array, target_number):
  # Loop through the list and check if the target_number is present
  for i, element in enumerate(array):
    if element == target_number:
      return i
 
  # Return -1 if the target_number was not found
  return -1

#fill_list.py
def fill_list():
  # Create an empty list
  array = []

  # Keep prompting the user for input until they enter a blank line
  while True:
    # Get the user's input
    user_input = input("Enter a value : ")

    # Check if the input is blank
    if not user_input:
      # Exit the loop if the input is blank
      break

    # Convert the input to an integer
    user_input = int(user_input)

    # Append the input to the list if it is not blank
    array.append(user_input)

  # Return the list of input values
  return array

def get_user_choice():
  """
  The function `get_user_choice` prompts the user to enter a choice between 1, 2, or 3, and returns
  the user's choice as an integer.
  :return: the user's choice as an integer.
  """
  try:
    user_choice = int(input("Enter\n1.To search in an array\n2.To sort an array\n3.To operate in an array with random elements: "))
    if user_choice not in [1,2,3]:
      print("Enter 1, 2, or 3")
      exit()
    return user_choice

  except ValueError:
    print("Enter an integer")
    exit(0)

#menu.py
def menu():
    user_choice = get_user_choice()

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

if __name__ == "__main__":
    menu()