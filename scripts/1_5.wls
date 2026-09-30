(* inspected and formatted by CodeInspector/CodeFormatter *)

f[u_, v_, w_] :=
    {u^2 + a + u * v + v * w + w * u, (u + v) * (v + w) * (w + u)}

g[x_, y_] :=
    {((x - a) ^ 2 - (b - a) * (c - a)) / (2 * y), ((x - b) ^ 2 - (a -
         b) * (c - b)) / (2 * y), ((x - c) ^ 2 - (a - c) * (b - c)) / (2 * y)
        }

h[u_, v_, w_] :=
    {u^2 + a, u * v * w}

(* test the condition for (x,y) in C *)

fverify[x_, y_] :=
    y^2 == (x - a) * (x - b) * (x - c) && y != 0

(* test the condition for (u,v,w) in B *)

gverify[u_, v_, w_] :=
    u^2 + a == v^2 + b == w^2 + c

(* test the condition for (u,v,w) in C̃ *)

hverify[x_, y_] :=
    y^2 == (x - a) * (x - b) * (x - c)

(* Overload to automatically unpack a list argument *)

f[list_List] :=
    f @@ list

g[list_List] :=
    g @@ list

h[list_List] :=
    h @@ list

fverify[list_List] :=
    fverify @@ list

gverify[list_List] :=
    gverify @@ list

hverify[list_List] :=
    hverify @@ list

Print["=== 1. Proof that f(u, v, w) maps into C ==="]

Print[FullSimplify[fverify[f[u, v, w]], Assumptions -> {u^2 + a == v^
    2 + b, u^2 + a == w^2 + c, a != b, b != c, c != a}]]

Print[""]

Print["=== 2. Proof that g(x, y) maps into B ==="]

Print[FullSimplify[gverify[g[x, y]], Assumptions -> y^2 == (x - a) * 
    (x - b) * (x - c)]]

Print[""]

Print["=== 3. Proof that h(u, v, w) maps into C~ ==="]

Print[FullSimplify[hverify[h[u, v, w]], Assumptions -> {u^2 + a == v^
    2 + b, u^2 + a == w^2 + c, a != b, b != c, c != a}]]

Print[""]

Print["=== 4. Testing f(g(x, y)) ==="]

Print[FullSimplify[f[g[x, y]], Assumptions -> y^2 == (x - a) * (x - b
    ) * (x - c)]]

Print[""]

Print["=== 5. Testing g(f(u, v, w)) ==="]

(* Step 1: Eliminate parameters 'a' and 'c' using set B relations:
   u^2 + a = v^2 + b  =>  a -> v^2 - u^2 + b
   v^2 + b = w^2 + c  =>  c -> v^2 - w^2 + b
*)

(* Pass 1: Apply elimination rules *)

step1 = g[f[u, v, w]] /. {a -> v^2 - u^2 + b, c -> v^2 - w^2 + b};

(* Pass 2: Simplify each component after substitution *)

Print[Map[FullSimplify, step1]]

Print[""]

Print["=== 6. Proof that (h o g)(x, y) == map2P(x, y) ==="]

(* (x-a)(x-b)(x-c) coefficients *)

A = 1;

B = -(a + b + c);

Unprotect[C]; Clear[C](* C reserved for integation constants *)

C = a * b + b * c + c * a;

Unprotect[D]; Clear[D] (* D is differentiation operator *)

D = -a * b * c;

(* Definition of (x3, y3) from §1.2 Formula (1.4) *)

x3[x_, y_] :=
    (1 / (4 * A * y^2)) * (A^2 * x^4 - 2 * A * C * x^2 - 8 * A * D * 
        x + C^2 - 4 * B * D)

y3[x_, y_] :=
    (1 / (8 * A * y^3)) * (A^3 * x^6 + 2 * A^2 * B * x^5 + 5 * A^2 * 
        C * x^4 + 20 * A^2 * D * x^3 + (20 * A * B * D - 5 * A * C^2) * x^2 +
         (8 * B^2 * D - 2 * B * C^2 - 4 * A * C * D) * x + (4 * B * C * D - 8
         * A * D^2 - C^3))

map2P[x_, y_] :=
    {x3[x, y], y3[x, y]}

Print[FullSimplify[h[g[x, y]] == map2P[x, y], Assumptions -> y^2 == (
    x - a) * (x - b) * (x - c)]]

Print[""]
