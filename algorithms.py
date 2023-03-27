import requests
import time
import matplotlib.pyplot as plt
from itertools import combinations

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
        plot(sequence, number)
        time_function_execution(collatz_function, number)
    else:
        print("Invalid input")
        
#timing.py
def time_function_execution(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken to execute {func.__name__}: {execution_time:.10f} seconds")
    return result

#count_lines.py
def count_lines(filename):
    # Open the file in read mode
    with open(filename, 'r') as f:
        # Read all the lines into a list
        lines = f.readlines()
        # Return the number of lines
        return len(lines)

#lotto_numbers.py
def write_combinations_to_file(filename):
    with open(filename, 'w') as f:
        for combination in combinations(range(1, 50), 6):
            f.write(' '.join(str(n) for n in combination) + '\n')

#get_fact.py
def get_fact(number):
    url = "http://numbersapi.com/{}".format(number)
    r = requests.get(url)
    if r.status_code == 200:
        print(r.text)
    else:
        print("An error occurred, code={}".format(r.status_code))

#collatz.py
def collatz_function(number):
    sequence = [number]
    count = 0
    while number != 1:
        if number % 2 == 0:
            number = number // 2
        else:
            number = 3 * number + 1
        count += 1
        sequence.append(number)
    return sequence, count

def plot(sequence, number):
    x_range = range(len(sequence))
    plt.plot(x_range, sequence, 'b.-')  # Use a blue line with dots for the plot
    plt.xlabel('Step')
    plt.ylabel('Value')
    plt.title(f'Collatz sequence for n = {number}')
    plt.show()
    
#fibonacci.py
def show_fibonacci_range(start, end):
  def fibonacci(n):
    # Base case: return 0 for n = 0 and 1 for n = 1
    if n == 0:
      return 0
    elif n == 1:
      return 1
    # Recursive case: return the sum of the previous two Fibonacci numbers
    else:
      return fibonacci(n - 1) + fibonacci(n - 2)

  def generate_fibonacci_range(start, end):
    # Initialize an empty list to store the Fibonacci numbers
    fib_range = []
    # Generate the Fibonacci numbers in the given range
    for n in range(start, end + 1):
      fib_range.append(fibonacci(n))
    # Return the list
    return fib_range

  def plot_fibonacci_range(fib_range):
    # Get the range of x-values
    x_range = range(len(fib_range))
    # Plot the Fibonacci numbers as a line and a scatter plot
    plt.plot(x_range, fib_range)
    plt.scatter(x_range, fib_range)
    # Add labels to the x- and y-axes
    plt.xlabel("n")
    plt.ylabel("Fibonacci(n)")
    # Show the plot
    plt.show()

  # Generate the Fibonacci numbers in the given range
  fib_range = generate_fibonacci_range(start, end)
  
  # Plot the Fibonacci numbers
  plot_fibonacci_range(fib_range)
  
  # Print the Fibonacci numbers as an array
  print(fib_range)

# Call the main function
main()

