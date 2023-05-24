from itertools import combinations
import requests, time, matplotlib.pyplot as plt, numpy as np

#count_lines.py
def count_lines(filename):
    # Open the file in read mode
    with open(filename, 'r') as f:
        # Read all the lines into a list
        lines = f.readlines()
        # Return the number of lines
        print(f'{len(lines)} lines in the file ')

#count_words.py
def count_words(filename):
    with open(filename, "r") as f:
        all_words = []
        for line in f:
            # split each line into words and add them to the list
            all_words.extend(line.split())  
        # create a dictionary to keep track of the word counts and first occurrences
        word_counts = {}
        first_occurrences = {}
        for i, word in enumerate(all_words):
            if word not in word_counts:
                # add the word to the dictionary with a count of 1 and the current index as its first occurrence
                word_counts[word] = 1
                first_occurrences[word] = i
            else:
                # increment the word count
                word_counts[word] += 1
        # print each word and its count
        print("Unique words in the file: ")
        for word in word_counts:
            print(word, word_counts[word])

#get_fact.py
def get_fact(number):
    # create a URL string by formatting the input number into the URL
    url = "http://numbersapi.com/{}".format(number)
    
    # send an HTTP GET request to the URL
    r = requests.get(url)
    
    # if the request is successful (status code 200), print the response text, otherwise, print an error message with the status code
    if r.status_code == 200:
        print(r.text)
    else: 
        print("An error occurred, code={}".format(r.status_code))

#lotto_numbers.py
def time_function_execution(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Time taken to execute {func.__name__}: {execution_time:.10f} seconds")
    return result

def write_combinations_to_file(filename):
    with open(filename, 'w') as f:
        for combination in combinations(range(1, 50), 6):
            f.write(' '.join(str(n) for n in combination) + '\n')

#fibonacci.py
def fibonacci_sequence(start, end):
  # Generate the Fibonacci numbers in the given range
  fib_range = generate_fibonacci_range(start, end)
  
  # Plot the Fibonacci numbers
  plot_fibonacci_range(fib_range)
  
  # Print the Fibonacci numbers as an array
  print(f'Fibonacci numbers from {start} to {end}: ', fib_range)

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
  plt.plot(x_range, fib_range, 'b-o')
  plt.scatter(x_range, fib_range)
  # Add labels to the x- and y-axes
  plt.xlabel("n")
  plt.ylabel("Fibonacci(n)")
  plt.grid(True)
  # Show the plot
  plt.show()

#collatz.py
def collatz_sequence(number):
  sequence = collatz(number)
  print(f'Collatz sequence starting from {number}: ', sequence)
  plot_collatz_range(sequence, number)

def collatz(number):
    sequence = [number]
    count = 0
    while number != 1:
        if number % 2 == 0:
            number = number // 2
        else:
            number = 3 * number + 1
        count += 1
        sequence.append(number)
    return sequence

def plot_collatz_range(sequence, number):
    x_range = range(len(sequence))
    plt.plot(x_range, sequence, 'b-o')  # Use a blue line with dots for the plot
    plt.xlabel('Step')
    plt.ylabel('Value')
    plt.title(f'Collatz sequence for n = {number}')
    plt.grid(True)
    plt.show()

#factorial.py
def factorial_number(n):
    if n == 0:
        return 1
    else:
        return n * factorial_number(n - 1)

def plot_factorial(n):
    numbers = list(range(n+1))
    factorials = [factorial_number(num) for num in numbers]
    plt.plot(numbers, factorials, 'b-o')
    plt.xlabel('Incrementing Numbers')
    plt.ylabel('Factorial')
    plt.title('Factorial Graph')
    plt.grid(True)
    plt.show()

def factorial_sequence(n):
  result = factorial_number(n)
  # Displaying the factorial
  print(f"The factorial of {n} is {result}")
  # Plotting the factorial graph
  plot_factorial(n)

def main():
	collatz_sequence(5)
	fibonacci_sequence(1, 5)
	factorial_sequence(5)
	count_lines("test.txt")
	count_words("test.txt")
	get_fact(5)
    '''
	import lotto_numbers
	lotto_numbers.time_function_execution(lotto_numbers.write_combinations_to_file, "combinations.txt")
	os.remove("combinations.txt")
    '''
    
main()