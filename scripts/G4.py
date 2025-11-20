# pylint: disable=C0103
#                 invalid-name
""" determine all groups on 4 elements """
from itertools import permutations

n=4
T=[[row for col in range(n)] for row in range(n)]
T[0]=list(range(n))
S=[[col for col in range(n) if col!=row] for row in range(n)]

for T[1][1:n+1] in permutations(S[1]):
    for T[2][1:n+1] in permutations(S[2]):
        for T[3][1:n+1] in permutations(S[3]):
            if {len({r[c] for r in T}) == n for c in range(1,n)}=={True}:
                for r in T:
                    print(*r)
                print()
