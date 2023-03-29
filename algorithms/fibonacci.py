import matplotlib.pyplot as plt

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
