import numpy as np

max_dimension = 100

def checkMagicSquare(dimension, array):
    """
    The function `checkMagicSquare` checks if a given 2D array represents a magic square of a given
    dimension.
    
    :param dimension: The dimension parameter represents the number of rows and columns in the square
    array. It determines the size of the square
    :param array: The array parameter is a 2-dimensional list representing a square matrix. Each element
    in the list represents a number in the matrix. The dimensions of the matrix are specified by the
    dimension parameter
    :return: a boolean value. It returns True if the given array represents a magic square of the given
    dimension, and False otherwise.
    """
    # Check if the number of rows is equal to dimension
    if len(array) != dimension:
        return False

    # Check if all rows have the same length
    for row in array:
        if len(row) != dimension:
            return False

    # Calculate the expected sum of each row, column, and diagonal
    magic_sum = dimension * (dimension**2 + 1) // 2

    # Check the sum of each row
    for row in array:
        if sum(row) != magic_sum:
            return False

    # Check the sum of each column
    for i in range(dimension):
        col_sum = sum(row[i] for row in array)
        if col_sum != magic_sum:
            return False

    # Check the sum of the main diagonal
    main_diag_sum = sum(array[i][i] for i in range(dimension))
    if main_diag_sum != magic_sum:
        return False

    # Check the sum of the secondary diagonal
    sec_diag_sum = sum(array[i][dimension - i - 1] for i in range(dimension))
    if sec_diag_sum != magic_sum:
        return False

    # If all checks passed, it is a magic square
    return True

def createMagicSquare(dimension):
    """
    The function `createMagicSquare` generates a magic square of a given dimension and prints it.
    
    :param dimension: The parameter "dimension" represents the size of the magic square. It determines
    the number of rows and columns in the square
    """
    magic_square = [[0] * dimension for _ in range(dimension)]
    num_cells = dimension * dimension
    row, col = dimension // 2, dimension - 1

    for num in range(1, num_cells + 1):
        magic_square[row][col] = num
        row = (row - 1) % dimension
        col = (col + 1) % dimension
        if magic_square[row][col] != 0:
            row = (row + 1) % dimension
            col = (col - 2) % dimension

    # Print the magic square
    for i in range(dimension):
        for j in range(dimension):
            print(magic_square[i][j], end=" ")
        print()

def input_array(dimension):
    """
    The function `input_array` takes a dimension as input and prompts the user to enter elements for
    each row of a 2D array, validating that the input consists of integer values separated by spaces.
    
    :param dimension: The parameter "dimension" represents the number of rows in the array
    :return: a 2-dimensional array.
    """
    array = []
    for i in range(dimension):
        while True:
            try:
                elements = input(f"Enter the elements for row {i + 1}, separated by spaces: ")
                elements = elements.split()
                elements = [int(element) for element in elements]
                array.append(elements)
                break
            except ValueError:
                print("Invalid input. Please enter integer values separated by spaces.")
    
    return array

def validation_check(dimension, choice):
    """
    The function performs validation checks on a given dimension and choice, raising errors if the
    conditions are not met.
    
    :param dimension: The dimension parameter represents the size or length of something, such as the
    dimensions of a shape or the length of a list
    :param choice: The `choice` parameter is used to determine the type of validation check to perform.
    It is expected to be an integer value
    """
    if dimension <= 0 or dimension > max_dimension:
        print(f"Dimension must be between 1 and {max_dimension}.")
        exit(0)

    if choice == 1 and dimension % 2 == 0:
        print("Dimension must be an odd number.")
        exit(0)

def main():
    """
    The main function allows the user to choose between checking if a square is magic or creating a
    magic square, and then performs the corresponding operation based on the user's choice.
    """
    choice = int(input("Enter\n1 for check if a square is magic\n2.for create a magic square: "))
    if choice == 1:
        dimension = int(input("Enter the size of the magic square: "))
        validation_check(dimension, choice)
        array = np.array(input_array(dimension))
        result = checkMagicSquare(dimension, array)
        
        if result:
            print(array, "is a magic square")
        else:
            print(array, "is not a magic square")
    elif choice == 2:
        dimension = int(input("Enter the size of the magic square: "))
        validation_check(dimension, choice)
        createMagicSquare(dimension)

main()