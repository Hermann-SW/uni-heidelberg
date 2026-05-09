Code uses symarrays for 4x4 matrices A and B to verify symbolically that all computations are correct. These are the scenarios for applying to Strassen tensor of demo:
- apply A and B (to Strassen tensor, in order to compute A@B)
- apply A to compute A_operator, then B (to compute A@B)
- apply B to compute B_operator, then A (to compute A@B)
- apply C((!), which is normally the result) to compute C_operator, then A (that computes Aᵀ@(A@B))
- output A@B demonstrating the symbolic matrix-matrix product A@B.  
Especially the C_operator computation is interesting. For orthonormal matrix A, AᵀA=id and the computation would result in B. If A represents linear function f:V->W, the Aᵀ represents f*:W*->V*
```
pi@raspberrypi5:~/uni-heidelberg/scripts $ ~/venv/bin/python strassen.4x4.py 
symbolic symarray()s verification; compute A @ B with rank 47 Strassen tensor
Success apply(A,B): True
Success apply(A), then B: True
Success apply(B), then A: True
Success apply(C), then A, gives A.T @ (A @ B): True
A @ B = [[A_0_0*B_0_0 + A_0_1*B_1_0 + A_0_2*B_2_0 + A_0_3*B_3_0
  A_0_0*B_0_1 + A_0_1*B_1_1 + A_0_2*B_2_1 + A_0_3*B_3_1
  A_0_0*B_0_2 + A_0_1*B_1_2 + A_0_2*B_2_2 + A_0_3*B_3_2
  A_0_0*B_0_3 + A_0_1*B_1_3 + A_0_2*B_2_3 + A_0_3*B_3_3]
 [A_1_0*B_0_0 + A_1_1*B_1_0 + A_1_2*B_2_0 + A_1_3*B_3_0
  A_1_0*B_0_1 + A_1_1*B_1_1 + A_1_2*B_2_1 + A_1_3*B_3_1
  A_1_0*B_0_2 + A_1_1*B_1_2 + A_1_2*B_2_2 + A_1_3*B_3_2
  A_1_0*B_0_3 + A_1_1*B_1_3 + A_1_2*B_2_3 + A_1_3*B_3_3]
 [A_2_0*B_0_0 + A_2_1*B_1_0 + A_2_2*B_2_0 + A_2_3*B_3_0
  A_2_0*B_0_1 + A_2_1*B_1_1 + A_2_2*B_2_1 + A_2_3*B_3_1
  A_2_0*B_0_2 + A_2_1*B_1_2 + A_2_2*B_2_2 + A_2_3*B_3_2
  A_2_0*B_0_3 + A_2_1*B_1_3 + A_2_2*B_2_3 + A_2_3*B_3_3]
 [A_3_0*B_0_0 + A_3_1*B_1_0 + A_3_2*B_2_0 + A_3_3*B_3_0
  A_3_0*B_0_1 + A_3_1*B_1_1 + A_3_2*B_2_1 + A_3_3*B_3_1
  A_3_0*B_0_2 + A_3_1*B_1_2 + A_3_2*B_2_2 + A_3_3*B_3_2
  A_3_0*B_0_3 + A_3_1*B_1_3 + A_3_2*B_2_3 + A_3_3*B_3_3]]
pi@raspberrypi5:~/uni-heidelberg/scripts $ 
```
