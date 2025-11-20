# pylint: disable=C0103
#                 invalid-name
""" determine all groups on 6 elements """
from itertools import permutations

def pprint(G):
    """ pretty print group """
    for r in G:
        print(*r)
    print()

def inverses(G):
    """ verify all elements have inverse """
    l=len(G)
    return all(
                any(
                     (G[a][r]==0 and G[r][a]==0) for a in range(1,l)
                   ) for r in range(1,l)
              )

def assoziativ(G):
    """ verify associativity """
    l=len(G)
    for a in range(l):
        for b in range(l):
            for c in range(l):
                if G[G[a][b]][c]!=G[a][G[b][c]]:
                    return False
    return True

def abelsch(G):
    """ abelian? """
    l=len(G)
    for a in range(1,l):
        for b in range(a+1,l):
            if G[a][b]!=G[b][a]:
                return False
    return True

def isomorph(U,V):
    """ check two groups being isomorphic """
    l=len(V)
    for P in permutations(range(l)):
        if all(P[V[a][b]]==U[P[a]][P[b]] for a in range(l) for b in range(l)):
            return True
    return False

def non_isomorph_groups(L):
    """ print only groups not isomorphic to all other groups """
    if len(L)==0:
        return
    l=len(L[0])
    pprint(L[0])
    for a in range(1,l):
        if all(not isomorph(L[a],L[b]) for b in range(a)):
            pprint(L[a])

n=6
T=[[row for col in range(n)] for row in range(n)]
T[0]=list(range(n))
S=[[col for col in range(n) if col!=row] for row in range(n)]

A=[]
N=[]

for T[1][1:n+1] in permutations(S[1]):
    if any({len({r[c] for r in T[0:2]}) != 2 for c in range(1,n)}):
        continue
    for T[2][1:n+1] in permutations(S[2]):
        if any({len({r[c] for r in T[0:3]}) != 3 for c in range(1,n)}):
            continue
        for T[3][1:n+1] in permutations(S[3]):
            if any({len({r[c] for r in T[0:4]}) != 4 for c in range(1,n)}):
                continue
            for T[4][1:n+1] in permutations(S[4]):
                if any({len({r[c] for r in T[0:5]}) != 5 for c in range(1,n)}):
                    continue
                for T[5][1:n+1] in permutations(S[5]):
                    if any({len({r[c] for r in T}) != n for c in range(1,n)}):
                        continue
                    if inverses(T):
                        if assoziativ(T):
                            if abelsch(T):
                                A.append([[T[a][b] for b in range(n)] for a in range(n)])
                            else:
                                N.append([[T[a][b] for b in range(n)] for a in range(n)])

print("nichtisomorphe abelsche Gruppen ( von",len(A),")")
non_isomorph_groups(A)

print("nichtisomorphe nicht abelsche Gruppen ( von",len(N),")")
non_isomorph_groups(N)
