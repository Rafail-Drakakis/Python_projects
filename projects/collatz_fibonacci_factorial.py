import matplotlib.pyplot as plt

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
  plt.plot(x_range, fib_range)
  plt.scatter(x_range, fib_range)
  # Add labels to the x- and y-axes
  plt.xlabel("n")
  plt.ylabel("Fibonacci(n)")
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
    plt.plot(x_range, sequence, 'b.-')  # Use a blue line with dots for the plot
    plt.xlabel('Step')
    plt.ylabel('Value')
    plt.title(f'Collatz sequence for n = {number}')
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