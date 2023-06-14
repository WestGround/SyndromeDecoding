import time

import numpy as np
import sympy as sp

def standard_isd(H_t: np.ndarray, n: int, k: int, s: np.ndarray, w: int) -> tuple:
    result = None
    gaussian_elim_time = []
    time1 = time.time()
    while not result:
        ### Randomly choose n-k column
        perm = np.random.default_rng().permutation(n)

        ### Apply Gaussian elimination for the chosen columns and s
        ### If fails (i.e., chosen columns are linearly dependent), continue
        time2 = time.time()
        rref_mat = []
        for row_index in range(0, n-k):
            row = []
            for col_index in range(k, n):
                row.append(H_t[perm[col_index]][row_index])
            row.append(s[row_index])
            rref_mat.append(row)
        is_singular, rref_mat = gaussian_elim(rref_mat, n, k)
        time3 = time.time()

        gaussian_elim_time.append(time3-time2)

        if is_singular:
            continue

        ### Calculate the weight of the modified syndrome
        weight = 0
        permuted_error = [0 for _ in range(0, k)]
        for row_index in range(0, n-k):
            if rref_mat[row_index][-1]==1:
                weight += 1
                permuted_error.append(1)
            else:
                permuted_error.append(0)

        if weight>w:
            continue

        ### Calculate the original error occurred
        error = []
        for i in range(0, n):
            if permuted_error[np.where(perm==i)[0][0]]==1:
                error.append(1)
            else:
                error.append(0)

        time4 = time.time()
        return (np.array(error), gaussian_elim_time, time4-time1)

    ### Return the error vector re-permuted with the chosen permutation

def gaussian_elim(M: list, n: int, k: int) -> tuple:
    ### 1. Forward Elimination
    for pivot in range(0, n-k):
        is_singular = True
        for row_index in range(pivot, n-k):
            if M[row_index][pivot]==1:
                is_singular = False
                pivot_th_row = M.pop(row_index)
                M.insert(pivot, pivot_th_row)
                break

        if is_singular:
            return is_singular, None

        for row_index in range(pivot+1, n-k):
            if M[row_index][pivot]==1:
                M[row_index] = binary_vector_addition(M[row_index], M[pivot])

    ### 2. Backward Elimination
    for pivot in range(1, n-k):
        for row_index in range(0, pivot):
            if M[row_index][pivot]==1:
                M[row_index] = binary_vector_addition(M[row_index], M[pivot])

    return is_singular, M

def binary_vector_addition(v1: list, v2: list) -> list:
    assert(len(v1)==len(v2))

    added_vector = []
    for i in range(0, len(v1)):
        added_vector.append(v1[i]^v2[i])

    return added_vector

def binary_vector_inner_prod(v1: list, v2: list) -> int:
    assert(len(v1)==len(v2))

    res = 0
    for i in range(0, len(v1)):
        res += v1[i]&v2[i]
    return res%2

def binary_mat_vec_mult(M, v) -> list:
    res = []
    
    for row in M:
        res.append(binary_vector_inner_prod(row, v))

    return res