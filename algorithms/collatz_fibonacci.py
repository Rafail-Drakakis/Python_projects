import matplotlib.pyplot as plt

#fibonacci.py
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

def fibonacci_sequence():
  start = int(input("Give the first number of the range: "))
  end = int(input("Give the last number of the range: "))
  
  # Generate the Fibonacci numbers in the given range
  fib_range = generate_fibonacci_range(start, end)
  
  # Plot the Fibonacci numbers
  plot_fibonacci_range(fib_range)
  
  # Print the Fibonacci numbers as an array
  print(fib_range)


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

def collatz_plot(sequence, number):
    x_range = range(len(sequence))
    plt.plot(x_range, sequence, 'b.-')  # Use a blue line with dots for the plot
    plt.xlabel('Step')
    plt.ylabel('Value')
    plt.title(f'Collatz sequence for n = {number}')
    plt.show()
    
def collatz_function_menu():
    number = int(input("Give a number: "))
    sequence, count = collatz_function(number)
    collatz_plot(sequence, number)
    
#main menu
def collatz_fibonacci_menu():
	choice = int(input("Enter\n1.For Collatz sequence \n2.For Fibonacci sequence: "))
	if choice == 1:
		print("Collatz sequence:")
		collatz_function_menu()
	elif choice == 2:
		print("Fibonacci sequence:")
		fibonacci_sequence()
