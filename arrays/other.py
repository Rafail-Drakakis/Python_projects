import time

#timing.py
def finish_time(function, algorithm_name, *positional_args, **keyword_args):
    start_time = time.time()
    result = function(*positional_args, **keyword_args)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"The {algorithm_name} algorithm took {execution_time:.6f} seconds \n{algorithm_name}, {result}")
    return result
    
#testing.py
def test_algorithm(algorithm_name, algorithm_func, array, *args):
    result = finish_time(algorithm_func, algorithm_name, array, *args)
    return result

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
