import matplotlib.pyplot as plt

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
