import math, numpy as np, matplotlib.pyplot as plt

#Gauss_elimination.py
def gauss_elimination_iterative(A, verbose):

    # Practice DEFENSIVE PROGRAMMING
    # DEFEND against all possible problems that may occur when a user calls this function

    # Check if the parameters have the correct type
    assert type(A) is np.ndarray
    assert type(verbose) == int

    # Copy the A array so that the function has no SIDE EFFECTS.
    # If you do not do this then this function will change the matrix A for the caller of the function!
    # It is VERY important to create functions/procedures with NO SIDE EFFECTS
    A = A.copy()

    # Get the number of ROWS.
    # The number of columns of unknowns is also m, and the last column is
    # the right hand side, i.e. vector b.
    m = A.shape[0]

    # Check if A has the correct dimensions
    assert A.shape[0]+1 == A.shape[1]

    if verbose:
        print("Gauss Elimination (Iterative version)")
        print("Input Augmented Matrix A is:")
        print(A)

    if verbose:
        print("Beginning Forward Elimination")

    # Forward elimination
    # Repeat for every row

    for i in range(m-1):
        # Repeat for every column, except for the last, which corresponds to the right
        # hand side
        driver = A[i, i]
        for j in range(i + 1, m):
            # You should check if this is zero or even CLOSE to zero
            # How close to zero? Dividing by the driver should not cause an overflow or underflow
            # If this is indeed close to zero, you should try to permute the rows and find another driver
            # If no non-zero driver can be found, there is no solution and you should raise an error
            # If there are possible underflows or overflows you should raise a warning

            lambda_coeff = A[j, i] / driver
            A[j, :] = A[j, :] - lambda_coeff * A[i, :]

            if verbose:
                # In the output, I use the numbering convention where the matrix rows go from 1 to m, and same for the
                # columns, so I add one to the indexes before printing.
                print(f"Matrix A for driver at position {i+1},{i+1} zeroed element {j+1}, {i+1}")
                print(A)


    # At this point, the matrix A should be upper triangular

    if verbose:
        print("Beginning Backward Substitution")

    # This is the reverse substitution part
    for i in range(m-1, -1, -1):
        # Make all the drivers equal to 1, by dividing the whole row with the driver
        driver = A[i,i]
        A[i, :] = A[i, :] / driver

        if verbose:
            print(f"Matrix A after making the driver at position {i + 1},{i + 1} equal to 1")
            print(A)

        # In Python, the range command from start (first argument) to stop (second argument) NOT included
        for j in range(i-1, -1, -1):
            # No need to divide with the driver now, because all drivers are now equal to 1
            lambda_coeff = A[j, i]
            A[j, :] = A[j, :] - lambda_coeff * A[i, :]

            if verbose:
                print(f"Matrix A for driver at position {i+1},{i+1} zeroed element {j+1}, {i+1}")
                print(A)

    # The solution should be in the last column of the matrix

    return A[:, m]

def gauss_elimination_recursive(A, verbose):
    # Practice DEFENSIVE PROGRAMMING
    # DEFEND against all possible problems that may occur when a user calls this function

    # Check if the parameters have the correct type
    assert type(A) is np.ndarray
    assert type(verbose) == int

    # Copy the A array so that the function has no SIDE EFFECTS.
    # If you do not do this then this function will change the matrix A for the caller of the function!
    # It is VERY important to create functions/procedures with NO SIDE EFFECTS
    A = A.copy()

    # Get the number of ROWS.
    # The number of columns of unknowns is also m, and the last column is
    # the right hand side, i.e. vector b.
    m = A.shape[0]

    # Check if A has the correct dimensions
    assert A.shape[0] + 1 == A.shape[1]

    if verbose:
        print("Gauss Elimination (Recursive version)")
        print("Input Augmented Matrix A is:")
        print(A)

    if verbose:
        print("Current Matrix at recursive call is:")
        print(A)

    # Step 1: Base case: solving the smallest possible problem DIRECTLY
    if m == 1:
        solution = [A[0, 1] / A[0, 0]]
        if verbose:
            print(f"Returning solution {solution}")
        return solution

    # Step 2: Reducing the problem to a smaller one or smaller ones

    # Eliminates the elements below the first column of the first row (i.e., eliminates elements from row 2 onwards)
    # by subtracting a factor of the first row from each of these rows.
    # This should be exactly like the Forward Elimination phase, but only for the first driver.
    driver = A[0, 0]
    for j in range(1, m):
        lambda_coeff = A[j, 0] / driver
        A[j, :] = A[j, :] - lambda_coeff * A[0, :]

        if verbose:
            print(f"Matrix A for driver at position {0 + 1},{0 + 1} zeroed element {j + 1}, {0 + 1}")
            print(A)

    # Step 3: Recursively solving the smaller problem or problems

    # At this point A's first equation has the first unknown but all other
    # equations do not contain the first unknown.
    solutionofsmaller = gauss_elimination_recursive(A[1:m, 1:(m + 1)], verbose)

    # Step 4: Combing the solution of the smaller problem(s) to find the solution to the current problem

    c = 0

    # Now just plug in the solution of all other unknowns except the first and
    # then solve for the first unknown quantity
    for j in range(0, m-1):
        c = c + solutionofsmaller[j] * A[0, j+1]
    firstunknown = (A[0, m] - c) / A[0, 0]

    # The addition APPENDS the two vectors
    solution = [firstunknown] + solutionofsmaller

    if verbose:
        print(f"Returning solution {solution}")

    return solution

def input_array():
    while True:
        try:
            dimensions = int(input("Enter the number of dimensions for the array: "))
            if dimensions <= 0:
                raise ValueError("Number of dimensions must be greater than 0.")
            break
        except ValueError as e:
            print("Invalid input:", str(e))
    
    array = []
    for i in range(dimensions):
        while True:
            try:
                elements = input(f"Enter the elements for dimension {i + 1}, separated by spaces: ")
                elements = elements.split()
                elements = [int(element) for element in elements]
                array.append(elements)
                break
            except ValueError:
                print("Invalid input. Please enter integer values separated by spaces.")
    
    return array

def main():
    A = np.array(input_array())
    print("Gauss-Iterative", gauss_elimination_iterative(A,0))
    print("Gauss-Recursive", gauss_elimination_recursive(A,0))

main()