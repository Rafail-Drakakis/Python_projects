import numpy as np
import matplotlib.pyplot as plt
import math

#logarithm.py
def plot_logarithm(num):
    x = np.linspace(1, num, num)  # Generate x-axis values
    y = np.log10(x)  # Calculate logarithm base 10 of x
    
    for i, j in zip(x, y):
        print(f'({i:.1f}, {j:.2f})')
    
    plt.plot(x, y, 'b-o')  # Plot the graph
    plt.xlabel('Numbers')
    plt.ylabel('Logarithm (base 10)')
    plt.title('Graph of Logarithm')
    plt.grid(True)

    plt.show()

#exponential.py
def plot_exponential(n):
    x = np.linspace(0, n, num=100)  # Generate x values from 0 to n
    y = np.exp(x)                   # Calculate exponential values using numpy's exp function

    # Plot the exponential function with a blue solid line
    plt.plot(x, y, 'b-')

    # Add circle markers at specific x-values
    x_markers = np.arange(1, n + 1)  # x-values for markers
    y_markers = np.exp(x_markers)    # y-values for markers
    plt.plot(x_markers, y_markers, 'bo')  # Plot markers with blue circles

    # Add labels and legend
    plt.xlabel('x')
    plt.ylabel('exponential')
    plt.grid(True)

    # Calculate and print the exponential values
    exp_values = [round(math.exp(i), 2) for i in range(1, n + 1)]
    print(f'exponential values from 1 to {n}: {exp_values}')

    # Show the graph
    plt.show()

#fibonacci.py
def plot_fibonacci(start, end):
    
    def fibonacci_sequence(n):
        fib_sequence = [0, 1]
        if n <= 1:
            return fib_sequence[:n + 1]
        else:
            for i in range(2, n + 1):
                fib_sequence.append(fib_sequence[i - 1] + fib_sequence[i - 2])
            return fib_sequence

    fib_range = fibonacci_sequence(end)
    fib_range = fib_range[start:end + 1]

    x_range = range(start, end + 1)
    plt.plot(x_range, fib_range, 'b-o')
    plt.scatter(x_range, fib_range)
    plt.xlabel("n")
    plt.ylabel("Fibonacci(n)")
    plt.grid(True)
    plt.show()

    print(f'Fibonacci numbers from {start} to {end}: {fib_range}')

#collatz.py
def plot_collatz(number):
    sequence = [number]
    count = 0
    while number != 1:
        if number % 2 == 0:
            number = number // 2
        else:
            number = 3 * number + 1
        count += 1
        sequence.append(number)
    
    print(f'Collatz sequence starting from {number}: ', sequence)
    
    x_range = range(len(sequence))
    plt.plot(x_range, sequence, 'b-o')  # Use a blue line with dots for the plot
    plt.xlabel('Step')
    plt.ylabel('Value')
    plt.title(f'Collatz sequence for n = {count}')
    plt.grid(True)
    plt.show()

#factorial.py
def plot_factorial(n):
    def factorial_number(n):
        if n == 0:
            return 1
        else:
            return n * factorial_number(n - 1)

    numbers = list(range(n+1))
    factorials = [factorial_number(num) for num in numbers]
    
    result = factorial_number(n)
    
    # Displaying the factorial
    print(f"The factorial of {n} is {result}")
    
    # Plotting the factorial graph
    plt.plot(numbers, factorials, 'b-o')
    plt.xlabel('Incrementing Numbers')
    plt.ylabel('Factorial')
    plt.title('Factorial Graph')
    plt.grid(True)
    plt.show()