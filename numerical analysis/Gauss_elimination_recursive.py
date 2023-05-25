import numpy as np
import matplotlib.pyplot as plt
import math

#Gauss_elimination_recursive.py
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