"""
created with many Google gemini sessions; added "apply(C), then A", pylinted
"""
# pylint: disable=invalid-name
#
import numpy as np
import sympy as sp

def get_strassen_2x2_factors():
    """
    Standard Strassen coefficients for 2x2
    """
    U = np.array([[1,0,0,1], [0,0,1,1], [1,0,0,0], [0,0,0,1],
                  [1,1,0,0], [-1,0,1,0], [0,1,0,-1]])
    V = np.array([[1,0,0,1], [1,0,0,0], [0,1,0,-1], [-1,0,1,0],
                  [0,0,0,1], [1,1,0,0], [0,0,1,1]])
    W = np.array([[1,0,0,1], [0,0,1,-1], [0,1,0,1], [1,0,1,0],
                  [-1,1,0,0], [0,0,0,1], [1,0,0,0]])
    return U, V, W

# pylint: disable=too-many-locals
def block_permute_16():
    """
    Creates a permutation vector that maps standard row-major 4x4 indices
    to the block-wise order expected by np.kron(factors, factors).
    """
    # Standard: 0,1,2,3...15 (Row major)
    # Target: Indices of
    #         (Top-Left Block), (Top-Right Block), (Bottom-Left), (Bottom-Right)
    tl = [0, 1, 4, 5]
    tr = [2, 3, 6, 7]
    bl = [8, 9, 12, 13]
    br = [10, 11, 14, 15]
    return tl + tr + bl + br

def build_strassen_4x4_tensor():
    """
    see name
    """
    U2, V2, W2 = get_strassen_2x2_factors()

    # 1. Generate the 49 kronecker rows
    U4_raw = np.kron(U2, U2)
    V4_raw = np.kron(V2, V2)
    W4_raw = np.kron(W2, W2)

    # 2. Get the index permutation to fix the 4x4 layout
    perm = block_permute_16()
    inv_perm = np.argsort(perm)

    # 3. Apply permutation so factors match standard row-major A.flatten()
    U4 = U4_raw[:, inv_perm]
    V4 = V4_raw[:, inv_perm]
    W4 = W4_raw[:, inv_perm]

    T = np.zeros((4, 4, 4, 4, 4, 4), dtype="int64")
    for r in range(49):
        # Now reshape works correctly with standard row-major
        u_r = U4[r].reshape((4, 4))
        v_r = V4[r].reshape((4, 4))
        w_r = W4[r].reshape((4, 4))
        T += np.einsum('in,jk,lm->injklm', w_r, u_r, v_r)

    return T

# --- TEST ---
T4 = build_strassen_4x4_tensor()

A = sp.symarray('A', (4, 4))
B = sp.symarray('B', (4, 4))
C_actual = A @ B

print("symbolic symarray()s verification;\
 compute A @ B with rank 47 Strassen tensor")

C_tensor = np.einsum('injklm,jk,lm->in', T4, A, B)
print("Success apply(A,B):", sp.Matrix(C_tensor) == sp.Matrix(C_actual))

# This results in a 4-dimensional tensor (4x4x4x4)
# It represents "The action of multiplying by A"
A_operator = np.einsum('injklm,jk->inlm', T4, A)
# Now, to finish the multiplication with any B:
C = np.einsum('inlm,lm->in', A_operator, B)
print("Success apply(A), then B:", sp.Matrix(C) == sp.Matrix(C_actual))

# This results in a 4D tensor (4x4x4x4)
# It represents the operation "multiply any matrix on the right by B"
B_operator = np.einsum('injklm,lm->injk', T4, B)
# To complete the multiplication A * B:
C = np.einsum('injk,jk->in', B_operator, A)
print("Success apply(B), then A:", sp.Matrix(C) == sp.Matrix(C_actual))

# results in a 4D tensor (4x4x4x4)
# C:in A:jk B:lm
C_operator = np.einsum('injklm,in->jklm', T4, A @ B)
#
R = np.einsum('jklm,jk->lm', C_operator, A)
print("Success apply(C), then A, gives A.T @ (A @ B):",
       sp.Matrix(R) == sp.Matrix(A.T @ (A @ B)))

print("A @ B =", C_actual)
