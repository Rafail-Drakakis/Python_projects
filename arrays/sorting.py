#sorting.py
import time
from timing import finish_time

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
