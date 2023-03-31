#searching.py
from timing import finish_time

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

