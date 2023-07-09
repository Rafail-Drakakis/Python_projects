import numpy as np

def gauss_elimination_iterative(matrix, verbose):
    """
    The function `gauss_elimination_iterative` performs Gaussian elimination on an augmented matrix to
    solve a system of linear equations iteratively.
    
    :param matrix: The matrix parameter is a numpy array representing the augmented matrix A. It should
    have dimensions (n, n+1), where n is the number of rows in the matrix
    :param verbose: The `verbose` parameter is an integer that determines whether or not to print the
    intermediate steps of the Gauss elimination algorithm. If `verbose` is set to 0, no intermediate
    steps will be printed. If `verbose` is set to 1, the intermediate steps will be printed
    :return: the solution to the system of linear equations, which is the last column of the matrix
    after performing Gauss elimination and backward substitution.
    """
    assert isinstance(matrix, np.ndarray)
    assert isinstance(verbose, int)

    matrix = matrix.copy()

    num_rows, num_cols = matrix.shape

    assert num_rows + 1 == num_cols

    if verbose:
        print("Gauss Elimination (Iterative version)")
        print("Input Augmented Matrix A is:")
        print(matrix)

        print("Beginning Forward Elimination")

    # Forward elimination
    for i in range(num_rows - 1):
        driver = matrix[i, i]
        for j in range(i + 1, num_rows):
            lambda_coeff = matrix[j, i] / driver
            matrix[j, :] = matrix[j, :] - lambda_coeff * matrix[i, :]

            if verbose:
                print(f"Matrix A for driver at position {i+1},{i+1} zeroed element {j+1}, {i+1}")
                print(matrix)

    # At this point, the matrix should be upper triangular

    if verbose:
        print("Beginning Backward Substitution")

    # Backward substitution
    for i in range(num_rows - 1, -1, -1):
        driver = matrix[i, i]
        matrix[i, :] = matrix[i, :] / driver

        if verbose:
            print(f"Matrix A after making the driver at position {i + 1},{i + 1} equal to 1")
            print(matrix)

        for j in range(i - 1, -1, -1):
            lambda_coeff = matrix[j, i]
            matrix[j, :] = matrix[j, :] - lambda_coeff * matrix[i, :]

            if verbose:
                print(f"Matrix A for driver at position {i+1},{i+1} zeroed element {j+1}, {i+1}")
                print(matrix)

    # The solution should be in the last column of the matrix

    return matrix[:, num_rows]

def gauss_elimination_recursive(matrix, verbose):
    """
    The function `gauss_elimination_recursive` performs Gaussian elimination on an augmented matrix
    recursively to solve a system of linear equations.
    
    :param matrix: The matrix parameter is a numpy array representing an augmented matrix. It should
    have dimensions (n, n+1), where n is the number of unknowns in the system of equations
    :param verbose: The `verbose` parameter is an integer that determines whether or not to print
    intermediate steps and results during the execution of the function. If `verbose` is set to 0, no
    output will be printed. If `verbose` is set to 1, the function will print the input augmented matrix
    :return: The function `gauss_elimination_recursive` returns a list of solutions to the system of
    linear equations represented by the input augmented matrix.
    """
    assert isinstance(matrix, np.ndarray)
    assert isinstance(verbose, int)

    matrix = matrix.copy()

    num_rows, num_cols = matrix.shape

    assert num_rows + 1 == num_cols

    if verbose:
        print("Gauss Elimination (Recursive version)")
        print("Input Augmented Matrix A is:")
        print(matrix)

        print("Current Matrix at recursive call is:")
        print(matrix)

    # Step 1: Base case: solving the smallest possible problem directly
    if num_rows == 1:
        solution = [matrix[0, num_rows] / matrix[0, 0]]
        if verbose:
            print(f"Returning solution {solution}")
        return solution

    # Step 2: Reducing the problem to a smaller one or smaller ones

    driver = matrix[0, 0]
    for j in range(1, num_rows):
        lambda_coeff = matrix[j, 0] / driver
        matrix[j, :] = matrix[j, :] - lambda_coeff * matrix[0, :]

        if verbose:
            print(f"Matrix A for driver at position {0 + 1},{0 + 1} zeroed element {j + 1}, {0 + 1}")
            print(matrix)

    # Step 3: Recursively solving the smaller problem or problems

    solution_of_smaller = gauss_elimination_recursive(matrix[1:num_rows, 1:(num_rows + 1)].copy(), verbose)

    # Step 4: Combining the solution of the smaller problem(s) to find the solution to the current problem

    c = 0

    for j in range(0, num_rows - 1):
        c += solution_of_smaller[j] * matrix[0, j + 1]
    first_unknown = (matrix[0, num_rows] - c) / matrix[0, 0]

    solution = [first_unknown] + solution_of_smaller

    if verbose:
        print(f"Returning solution {solution}")

    return solution

def input_array():
    """
    The function `input_array` prompts the user to enter the number of rows for an array and then
    prompts the user to enter the elements for each row, creating a 2D array.
    :return: a NumPy array.
    """
    while True:
        try:
            num_rows = int(input("Enter the number of rows for the array: "))
            if num_rows <= 0:
                raise ValueError("Number of rows must be greater than 0.")
            break
        except ValueError as e:
            print("Invalid input:", str(e))
    
    array = []
    for i in range(num_rows):
        while True:
            try:
                elements = input(f"Enter the elements for row {i + 1}, separated by spaces: ")
                elements = elements.split()
                elements = [int(element) for element in elements]
                array.append(elements)
                break
            except ValueError:
                print("Invalid input. Please enter integer values separated by spaces.")
    
    return np.array(array)

def get_verbose_input():
    """
    The function `get_verbose_input()` prompts the user to enter either 0 or 1, and returns the input as
    an integer if it is valid.
    :return: The function `get_verbose_input` returns the value of the variable `verbose`, which is an
    integer representing the user's choice of verbosity level.
    """
    try:
        verbose = int(input("Press \n0.To see only the result\n1.To see all the steps: "))
        if verbose not in [0,1]:
            print("Enter 0 or 1")
            exit(0)
        return verbose
    except ValueError:
        print("Enter an integer")
        exit(0)

def main():
    verbose = get_verbose_input()
    matrix = input_array()
    print("Gauss-Iterative:", gauss_elimination_iterative(matrix, verbose))
    print("Gauss-Recursive:", gauss_elimination_recursive(matrix, verbose))

if __name__ == "__main__":
    main()