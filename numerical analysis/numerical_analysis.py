import numpy as np
import matplotlib.pyplot as plt
import math

#multiply_matrices.py
def multiply_matrices(A, B):
    # Check that matrices can be multiplied
    if len(A[0]) != len(B):
        print("Cannot multiply matrices: dimensions do not match")
        return []
    
    # Create an empty result matrix with appropriate dimensions
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    
    # Multiply the matrices
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]    
    print ("The multiplied matrix is", result)   

    return result
    
#LDU.py
def ldu(A):
    # Declaring the matrices
    n = A.shape[0]
    P = np.eye(n)
    L = np.zeros((n, n))
    U = A.copy()
    D = np.zeros((n, n))
    for k in range(n):
        l = k
        for i in range(k, n):
            if U[i, k] == 0:
                if (k+1) != n:
                    l = k+1
                else:
                    break
        if l != k:
            for j in range(n):
                value = P[k, j]
                P[k, j] = P[l, j]
                P[l, j] = value
                value = U[k, j]
                U[k, j] = U[l, j]
                U[l, j] = value
                value = L[k, j]
                L[k, j] = L[l, j]
                L[l, j] = value
        D[k, k] = U[k, k]
        for i in range(k+1, n):
            L[i, k] = U[i, k] / U[k, k]
            for j in range(k, n):
                U[i, j] = U[i, j] - L[i, k] * U[k, j]
        for i in range(n):
            L[i, i] = 1
    for i in range(n):
        driver = U[i, i]
        if driver != 0:
            for j in range(n):
                U[i, j] = U[i, j] / driver
    print("Matrix P is:\n", P, "\nMatrix L is:\n", L, "\nMatrix D is:\n", D, "\nMatrix U is:\n", U)

    return P, L, D, U