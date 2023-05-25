import numpy as np
import matplotlib.pyplot as plt
import math

#Gauss_elimination.py
def gauss_elimination(A, verbose):

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