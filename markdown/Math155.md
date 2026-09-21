## Berkeley math 115: Introduction to number theory

- Youtube lecture series [spring 2022](https://www.youtube.com/watch?v=EzE6it9kAsI&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=1)

Lectures:  
[53](#lecture-53-three-calculators-for-number-theorists)
[38](#lecture-38-binary-quadratic-forms)
[37](#lecture-37-continued-fractions)
[36](#lecture-36-kronecker-symbol)
[35](#lecture-35-jacobi-symbol)
[34](#lecture-34-gauss-sums)
[33](#lecture-33-quadratic-reciprocity)
[32](#lecture-32-calculation-of-the-legendre-symbol)
[31](#lecture-31-quadratic-residues) 
[30](#lecture-30-fields-in-number-theory) 
[29](#lecture-29-rings-in-number-theory) 
[28](#lecture-28-products-of-groups)  
[27](#lecture-27-groups-and-number-theory) 
[26](#lecture-26-roots-of-polynomials-modulo-a-prime) 
[25](#lecture-25-quadratic-equations-mod-p) 
[24](#lecture-24-primitive-roots-for-prime-powers) 
[23](#lecture-23-primitive-roots)
[22](#lecture-22-chevally-warning-theorem)
[21](#lecture-21-congruences-modulo-a-prime)
[20](#lecture-20-padic-numbers)
[19](#lecture-19-hensel-and-newtons-method)
[18](#lecture-18-cryptography)
[17](#lecture-17-factorization)
[16](#lecture-16-more-numerical-calculation)
[15](#lecture-15-numerical-calculation)
[14](#lecture-14-eulers-phi-totient-function)
[13](#lecture-13-chinese-remainder-theorem)
[12](#lecture-12-wilsons-theorem)
[11](#lecture-11-eulers-theorem)
[10](#lecture-10-fermats-theorem)
[9](#lecture-9-congruences)
[8](#lecture-8-applications-of-binomial-coefficients)
[7](#lecture-7-binomial-coefficients)
[6](#lecture-6-arithmetical-functions)
[5](#lecture-5-primes)
[4](#lecture-4-more-on-euclids-algorithm)
[3](#lecture-3-divisibility-and-euclids-algorithm)
[2](#lecture-2-survey)
[1](#lecture-1)

# [lecture 38](https://www.youtube.com/watch?v=13YcTRHzyDg&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=38): Binary quadratic forms

-

# [lecture 37](https://www.youtube.com/watch?v=MCPn7Bnuh2o&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=37): Continued fractions

- polynomial $f(x,,y,z,\dots)=0$
  - degrees 1/2/3/4 linear/quadratic/cubic/quadric
  - #variables 2/3/... binary/ternary/..
  - quadratic binary form
    - $ax^2+bxy+cy^2+dx+ey+f=0$, strike out dx, ey
    - $ax^2+bxy+cy^2=$ constant
    - Pellian equation: $x^2-Dy^2=1$
    - Brahmagupta 650 AD.
      - $x^2-92y^2=1$, find rational x/y close to $\sqrt{92}$
      - $\pi=\dots$, $\sqrt{23}=4+\frac{1}{1+\frac{1}{3+\frac{1}{1+\frac{1}{8+\dots}}}}$
      - shows how to get solutions with example calculations only
    
# [lecture 36](https://www.youtube.com/watch?v=8jnxAC9E4yE&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=36): Kronecker symbol

- all? a,b
- nonzero b
  - $\left(\frac{a}{b}\right)=$ Legendre, b prime > 0
  - $\left(\frac{a}{2}\right)=+1/-1/0\text{ for }a\equiv \pm 1\mod 8/\pm 3\mod 8/0 \mod 2$
  - $\left(\frac{a}{-1}\right)=+1/-1\text{ for } a\geq 0 / a<0$
  - $\left(\frac{1}{0}\right)=\left(\frac{-1}{0}\right)=\left(\frac{0}{1}\right)=\left(\frac{0}{-1}\right)=1$, $\left(\frac{0}{b}\right)=\left(\frac{a}{0}\right)=0$ otherwise
- properties
  - $\left(\frac{a}{b}\right)=¸pm 1$ if (a,b)=1, 0 if not
  - if $a\equiv 0,1 \mod 4$ then $\left(\frac{a}{b+na}\right)=\left(\frac{a}{b}\right)$  
    $a\equiv 2 \mod 4$: period 4a  
    $a\equiv 3 \mod 4$: mess
  - $\left(\frac{a_1a_2}{b}\right)=\left(\frac{a_1}{b}\right)\left(\frac{a_2}{b}\right)$, for $a,b\neq 0$
  - $\left(\frac{a}{b_1b_2}\right)=\left(\frac{a}{b_1}\right)\left(\frac{a}{b_2}\right)$
  - $\left(\frac{-1}{0}\right)\left(\frac{-1}{-1}\right)\neq\left(\frac{-1}{0\cdot (-1)}\right)$
- quadratic reprocity is mess, best: only for a,b odd > 0
- 2D table demonstrating where Legendre/Jacobi/Kronecker values are
- Dirichlet L series of imaginary quadratic field, $\mathbb{Z}[i]$
  - $$\left(\frac{D}{p}\right)$, discriminant D=0,1 mod 4, p odd primes
    - +1 if p splits as product of 2 distinct primes
    - -1 if p does not split; 3
    - 0 if 0 = square; 2=(1+i)(1-i)
  - $L(s) = \sum_n \left(\frac{D}{n}\right) \frac{1}{n^s}$
  - $L(s)=\frac{1}{1^s}-\frac{1}{3^s}+\frac{1}{5^s}-\frac{1}{7^s}+\dots$  
    $= \frac{1}{1+3^{-s}}\cdot\frac{1}{1-5^{-s}}\cdot\frac{1}{1+7^{-s}}\cdot\frac{1}{1-11^{-s}}\cdot\dots$  
    $=\prod_p \frac{1}{1-\chi(p)p^{-s}}; \chi(p)=\left(\frac{D}{p}\right)=\left(\frac{-4}{p}\right)$  
- application: $L(s)\zeta(s)$, ...

 
# [lecture 35](): Jacobi symbol

- Legendre symbol $\left(\frac{a}{b}\right)$ for b prime
- Jacobi symbol $\left(\frac{a}{b}\right)$ for b odd positive
- Kronecker symbol $\left(\frac{a}{b}\right)$ for all integers a,b
- Jacobi: mutiplicative in a, b; (-1/b), (2/b), (a+nb/b)=(a/b), all easy
- proof for law of reciprocity
- Warning: (a/b)=+1 does NOT imply a square
- No need to factor a for Jacobi reciprocity!
- compute is "Euclid", but take out factors of 2, keep track of signs
- Euclid without division, fast
- application, primality test that is a bit faster
- 1-step definition of Legendre symbol? Yes, Zolotarev, sign of permutation
- cycle of even length, odd permutation
- ...

# [lecture 34](https://www.youtube.com/watch?v=arL7oQV4asY&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=34): Gauss sums

- gauss sum, gamma function, similarity
- another proof of quadratic reciprocity (there are 300 proofs)

# [lecture 33](https://www.youtube.com/watch?v=k8qJaV7qGL4&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=33): Quadratic reciprocity

- $\left(\frac{p}{q}\right)\left(\frac{q}{p}\right)=(-1)^{(p-1)/2\cdot(q-1)/2}$
- example calculation of $\left(\frac{1001}{99991}\right)=+1$, 1001 is square, $38521^2$
- long proof of above

# [lecture 32](https://www.youtube.com/watch?v=MxwdmjtK1BQ&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=32): Calculation of the Legendre symbol

- $\left(\frac{-2}{p}\right)=\left(\frac{-1}{p}\right)\left(\frac{2}{p}\right)$, +1/-1 if p is 1,3/5,7 mod 8
- infinitely many primes $\equiv 7 \mod 8$
- infinitely many primes $\equiv 3 \mod 8$
- infinitely many primes $\equiv 5 \mod 8$, exercise
- $\left(\frac{3}{p}\right)=?$, +1/-1 if p=1,11 / 5,7 mod 12
- application to Fermat numbers:  
  $p=2^{2^n}+1$ is prime $\iff 3^{(p-1)/2}\equiv -1 \mod p$
- $\left(\frac{5}{p}\right)=+1 \iff p=1,9,11,19 \mod 20\iff p=1,4 \mod 5$
- $\left(\frac{5}{p}\right)=+1 \iff p=1,5,19,23 \mod 24$

# [lecture 31](https://www.youtube.com/watch?v=Pz6CL0nRmGQ&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=31): Quadratic residues

- $a\not\equiv0, x^2=a \mod p$ for some x, a is quadratic residue
- $a\not\equiv0, x^2=a \mod p$ no solution, a is quadratic nonresidue

$$
\text{Legendre symbol, p odd prime: } \left(\frac{a}{p}\right)=\begin{cases}
1 & \text{if a quadratic residue}\\
-1 & \text{if a quadratic nonresidue}\\
0 & \text{if }a\equiv 0\end{cases}
$$

- Euler $\left(\frac{a}{p}\right)\equiv a^{(p-1)/2}\mod p$
- $\left(\frac{a}{p}\right)$ is homomorphism $(\mathbb{Z}/p\mathbb{Z})^\times\to \\{-1,1\\}$
- $\left(\frac{-1}{p}\right)= +1/-1$ if $p\equiv 1/3 \mod 4$
- $\left(\frac{2}{p}\right)= +1/-1$ if p= 1,7 / 3,5
- Gauss's lemma:
  - $\left(\frac{a}{p}\right)=(-1)^n$, n #residue classes
  - $1 \equiv a^{(p-1)/2}(-1)^n \mod n$
  - $\left(\frac{2}{p}\right)=(-1)^n -\left[p/4\right]$

# [lecture 53](https://www.youtube.com/watch?v=P1I3_x0tk2A&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=53): Three calculators for number theorists 

- 3 pocket calculators: the Casio fx-300ES PLUS, the SwissMicros DM42, and the HP 50g.
- free simulator for the DM42
- GP / SAGE
  
# [lecture 30](https://www.youtube.com/watch?v=leBH9QpD9PQ&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=30): Fields in number theory

- f(x) coefficients in k, f has $\leq n$ roots ( $n=deg(f)$ )
- p has primitive root g, p prime, g has order p-1 in $(\mathbb{Z}/p\mathbb{Z})^\times$, cyclic
- relation between $\mathbb{Z}$ and $k[x]$
- finite field, of finite order $\mathbb{Z}/p\mathbb{Z}$, $(\mathbb{Z}/p\mathbb{Z})^\times[x]/f$ with f irreducible
- any finite field has order $p^n$, some prime p, $n\geq 1$
- $F^*$ cyclic, so has generator g
- $F^+$ NOT cyclic (unless $F=\mathbb{Z}/p\mathbb{Z}$)
- Fermat: $x^p\equiv x \mod p$
- same for finite fields, order is $p^n$, $x^{p^n}=x$ for all $x\in F$
- $x^{p^n}-x=\prod_{\alpha\in F}(x-\alpha)$ in F[x]; C.R.T.
- Wilson
- $f=x^3+x+1, x^3+x^2+1$ irreducible
- there is exactly one finite field of order $p^n$, any prime p, $n\geq 1$
- (key point: finite field of order $p^n$ is "splitting field" of $x^{p^n}-x$)

# [lecture 29](https://www.youtube.com/watch?v=7IP3YvM1dP0&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=29): Rings in number theory

- ring definition, examples $\mathbb{Z},\mathbb{R},\mathbb{C}$, integers mod n: $\mathbb{Z}/n\mathbb{Z}$
- quotients:
  - Groups: abelian, subgroup, G/H set of equivalence classes
  - Rings: R/I, I need to be IDEAL, R/I is ring, $\mathbb{R}[x]/(f)$
- C.R.T., analog for rings, pick ideals I,J of R, map $R: R/I\times R/J$
- $\mathbb{Z}$ has unique factorization
  - R is euclidean ring if it has division with remainder
  - gaussian integers, subring of complex numbers
  - unique factorization domain
- fields: ring, all nonzero elements have inverse
  - k[x]/(f) with f irreducibel (role of prime numbers)

# [lecture 28](https://www.youtube.com/watch?v=SLONKxYCmiA&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=28): Products of groups

- $G\times H$
- vector space $\mathbb{R}^2$
- $\mathbb{R}$, $\pm 1\times$ positive reals
- C.R.T.
- if G (abelian) has order mn with (m,n)=1  
  $G=A\times B$  
  A=elements a with ma=0   
  B=elements b with nb=0
- an G (finite, abelian) is product of groups of prime power order
- ... is product of cyclic groups
- find smallest integer n such that $x^n\equiv 1\mod 1000000 for (x,1000000)=1$

# [lecture 27](https://www.youtube.com/watch?v=bpzNGhiT4OI&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=27): Groups and number theory

- group definition
- important groups for number theory  
  $\mathbb{Z}/m\mathbb{Z}$  
  $(\mathbb{Z}/m\mathbb{Z})^\times$
- Lagrange: order of subgroup H $\mid$ order of group G
  - coset of $H = aH = \\{ ah_1, ah_2,\dots\\}$
  - 2 cosets have same order (map back by $a^{-1}$ bijection)
  - 2 cosets are same or disjoint
  - G is disjoint union of cosets of same size $\implies$ Lagrange  
- order of $g\in G$ divides order of $G$
- corollary:
  - Fermat $x^{p-1}\equiv 1 \mod p$  
    Group= $(\mathbb{Z}/m\mathbb{Z})^\times$ = integers coprime to p, mod p
  - Euler $x^{\varphi(m)}\equiv 1\mod m$, $(m,x)=1$  
    $\varphi(m)=$ order of group $(\mathbb{Z}/m\mathbb{Z})^\times$
- for abelian groups shorter proof
- group is CYCLIC if it has 1 generator g, all elements ar powers of g
- non obvious cyclic group:
  $(\mathbb{Z}/m\mathbb{Z})^\times$ has generator $\equiv$ primitive root
- isomorphic groups ("really the same")
- Wilsons theorem $(p-1)!\equiv \-1 \mod p$ (p prime)  
  G finite abelian group, product of all elements is
  
$$\\begin{cases} 
  g & (\text{if exactly one element g has order 2})\\  
  1 & (otherwise)
\\end{cases}$$

  $G=(\mathbb{Z}/m\mathbb{Z})^\times$
    
# [lecture 26](https://www.youtube.com/watch?v=GcJImruRSyE&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=26&pp=iAQB): Roots of polynomials modulo p

- Cantor-Zassenhaus  
  (1) Euclid for (a,b), works with poly, fast if deg f,g small  
  (2) Russian-Peasant
- find roots of f


# [lecture 25](https://www.youtube.com/watch?v=H7WFEGrmMEs&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=25&pp=iAQB): Quadratic equtions mod p

- degree 2 congruences  
  $ax^2+bx+c\equiv 0 \mod p$  
  $a(x+b/2)^2\equiv \frac{b^2-4ac}{4a}$, discriminant $b^2-4ac$  
  need /2, p odd OK because p=2 no problem  
  $x^2\equiv d$ ($d\not \equiv 0$)
  check has solution:  
  solution exists $\iff d^\frac{p-1}{2}\equiv 1\mod p$
- solve $x^2\equiv d$  
  method 1: trial and error  
  method 2: polynomial solver $f(x)\equiv 0$ (Berlekamp, Cantor-Zassenhaus)  
  method 3: guess answer, better Ansatz  
- general case:  
  $p-1=2^k\cdot n$, $n$ odd  
  pick g to have order $2^k$, $g=(random)^n$  
  $2^ks+nt=1$ by Euclid  
  $y=y^1=(y^n)^t\times (y^{2^k})^s$  
  order of power of 2, previous method  
  odd order, use method 3
  (divide and conquer)

# [lecture 24](https://www.youtube.com/watch?v=AfRpXi8r0So&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=24&pp=iAQB): Primitive roots for prime powers

- $p^n$, p odd prime, $n>1$
  - $p^2$
  - theorem: if $g$ primitive root mod $p^2$, $p$ odd prime, then primitive root $\mod p^n$ with $n\geq 1$
-  Equivalent  
   (1) m has primitive root  
   (2) m has $\varphi(\varphi(m))$ primitive roots  
   (3) $m=1,2,4,p^n,2p^n$ (p odd prime  
   (4) $x^2\equiv 1 \mod m \implies x\equiv \pm 1 \mod m$  
   (5) Wilson's theorem: $\prod_{(a,m)=1}a\equiv -1 \mod m$
- Mod $2^n$?
- logarithms: indices
- $a\not\equiv 0 \mod p$ is of form $g^n \mod p$; $n=\log_g a$
- p is prime? if we can factor $p-1$, we can find primitive root of $p$, 
  $g$ of order $p-1$, check $g$ not have order dividing $\frac{p-1}{q}$:
  $g^{\frac{p-1}{q}}\not\equiv 1\mod p$ with $q$ prime, $q\mid p-1$

# [lecture 23](https://www.youtube.com/watch?v=E8UTP0DiCCg&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=23&pp=iAQB): Primitive roots

- answer questions:  
  Which numbers have primitive roots? How many? How find?
  (carefully counting)
- Theorem: if $p$ is prime, $p$ has primitive root
- if $a$ is primitive root mod $m$, order of $a$ is $\varphi(m)$.  
  Now: $a^b$ has order $\varphi(m) \iff (b, \varphi(m))=1$  
  primitive roots: $$\\{a^b \mid (b, \varphi(m))=1\\}$$  
  #primitive roots = $\varphi(\varphi(m))$

# [lecture 22](https://www.youtube.com/watch?v=6QZYfpcf79I&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=22&pp=iAQB): Chevalley-Warning theorem

- If $f(x_1,\dots,x_n)$ has degree $d<n$  
  then #solutions to $f(x_1,\dots,x_n)\equiv 0\mod p$ is divisible by $p$
- Useful lemma:
  $0^i+1^i+2^i+\dots+(p-1)^i\equiv 0 \mod p$ if $i<p-1$
- Chevalley-Warning theorem implies that integers mod p are "quasi algebraicly closed"   

# [lecture 21](https://www.youtube.com/watch?v=E-6llnLZ7J8&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=21&pp=iAQB): Congruences modulo a prime

- advantages of p prime:
  - no zero divisors
  - inverses exist
  - polynomials of degree n have $\leq n$v roots
  - Fermat: $x^p\equiv x\mod p$
  - primitive roots exist mod p
- wolstenholme's theorem:  
  $1+\frac{1}{2}+\frac{1}{3}+\dots+\frac{1}{p-1}$, numerator
  is divisible by $p$ if $p>2$
- Given $f(x)\equiv 0 \mod p$, problems:  
  (1) any solutions?  
  (2) how many?  
  (3) find them?
- Euler: (fast, better replace by faster method later [Jacobi symbol])

$$a^{(p-1)/2}\equiv \begin{cases}
+1 & \text{if a is square}\\
-1 & \text{if a is not square}
\end{cases}$$

  - If $d$ divides $p-1$, then $x^d-1\equiv 0 \mod p$ has
    exactly $d$ roots
  

# [lecture 20](https://www.youtube.com/watch?v=1HTq2zq2RtY&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=20&pp=iAQB): p-adic numbers

- what if $f'(x_1)\equiv 0 \mod p$?
- p-adic numbers
  - (informal) number in base p, goes left infinite distance
  - does not converge to real number, but mod p
  - add, multiply p-adic numbers, also subtract
  - division by all numbers $a$ for $p\nmid a$
- which numbers are square? reals, 2-adics, p-adics
  -  square $\iff a\text{ is square }\mod p$
- any for reals has analog for p-adics
- iteration for reals and p-adics

# [lecture 19](https://www.youtube.com/watch?v=nrH2vs04TyQ&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=19&pp=iAQB): Hensel and Newton's method

- $f(x)\equiv 0 \mod m$
- today "Reduce from $p^m$ to $p$
  - stupid method $O(p^m)$
  - not quite so stupid method $O(p*m)$
    - $x^2\equiv 17 \mod 2^10$, problems: not unique, no lifts
  - Hensel's method $O(n)$
    - $f(x_1)\equiv 0 \mod p$, $x_1$ solution
    - Taylor, derivative, key point:
    $$\frac{\left(\frac{d}{dx}\right)^n f(x)}{n!}$$
    has integer solutions  
    we can solve $f(x)\equiv 0 \mod p$ IF:  
    (1) we can solve $f(x_1)\equiv 0 \mod p$  
    (2) $f'(x_1)\not\equiv 0 \mod p$

  - Newton's method (the same)
    - for reals $f(x)=0$ with tangents
    - if $f(x)=0\mod p^n$ and $f'(x)\not\equiv 0 \mod p$  
      then $f(x-\frac{f(x)}{f'(x)})\equiv 0 \mod p^{2n\}$  
      $O(\log n)$ because of doubling

# [lecture 18](https://www.youtube.com/watch?v=16dAteWM5ZA&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=18&pp=iAQB): Cryptography

- Alice, Bob, Eve
  - code book
  - one time pad
  - Enigma
  (share something)
- Diffie Hellman, trapdoor function: easy to compute, inverse hard
- blockchain, each block contains "secure hash" of previous blocks
  - mining bitcoin: find a so that f(a) "nice"
- Rivest/Shamir/Adleman
  - choose large p,q, large int k
  - publish m=pq and k,but not p,q
  - $f(x)=x^k \mod m$ public function
  - easy to find large primes, hard to factorize large numbers
- random
  - never use builtin random number generation
- breaking codes
  - factor m, Shor's algorithm quantum computers
  - decode without factoring?
  - rubber host cryptographie
  - man in the middle attack
  - users do something stupid
  - monitor traffic
  - direction finding
  - Eve can send fake messages to A, B
  - social engineering
  - message padded with junk
  - compressed message
  - extra security

# [lecture 17](https://www.youtube.com/watch?v=Imxx1tFDeSw&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=17&pp=iAQB): Factorization

- Pollard $\rho$ method: find factor p of n  
  expected running time $<\sqrt[4]{n}$
- Pollard's $p-1$ methd  
  good for finding factors p with $p-1$ smooth
- Lenstra's elliptic curve method

# [lecture 16](https://www.youtube.com/watch?v=roBKA4adPJE&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=16&pp=iAQB): More numerical calculation

- how solve $x^2\equiv -1 \mod p$, p prime, $p\equiv 1\mod 4$?
- guess at random, 50% chance to work, repeat
- worst case EXP TIME, average case POLY TIME
- test if x is prime
  - test all factors < $\sqrt{x}$, EXP TIME
  - write as $x=a^2-b^2$, best with $x=ab$ and a,b close
  - test whether $a^{m-1}\equiv 1 \mod m$

# [lecture 15](https://www.youtube.com/watch?v=ne0gHR57qUU&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=15&pp=iAQB): Numerical calculation 

- (1) solve ax+by=c  
  (2) Is n prime? Factorize it  
  (3) Solve $f(x)\equiv 0\mod p$; $x^2+1\equiv 0 \mod p$  
  (4) $a^b \mod m$
- O() notation
- Fast Fourier Transform: $O(N\log N)+O(N)+O(N\log N)$ [7:53min in video]  
  - FFT (choose $P=2\cdot 3\cdot\dots >mn$)  
  - pointwise multiplication (modulo the prime divisors of P)  
  - inverse FFT (use C.R.T. to reconstruct $mn \mod P$)  
  I implemented [proth.gp](../scripts/proth.gp) demo with Gemini, proving 1749 decimal digit Proth number prime
  using "RNS/CRT/folding reduction" multiplication. While ```Mod(3,N)^((N-1)/2)==Mod(-1,N)```
  ([prime proof for Proth number](https://arxiv.org/pdf/0812.2596#page=3) N=k*2^n+1 with k≤n and $3\nmid k$)
  returns 1 in 31ms, the demo did need 19s on AMD 9950X CPU. But it did show all the details,
  including the not mentioned by lecturer folding reductions. Gemini asked whether to port to C++ and we
  did in another very long chat. Down to only 3 seconds now with [proth_prover.cpp](../scripts/proth_prover.cpp)
  based on libgmp and libgmpxx. In later chat about performance improvements,
  new fast Barret reduction and Horner Scheme reduced runtime by 50%:
  ```
  $ ./proth_prover
  Digits of N: 1749
  CRT primes set up: 364 primes (Max: 4294967291)
  Precomputing Garner CRT coefficients...
  Starting modular exponentiation (3^((N-1)/2) mod N)...
  Progress: bit 0 / 5807             
    -> Total Exponentiation time: 1542 ms
  Comparing result against N - 1...
  Success! Result matches N - 1. N is prime!
  $ 
  ``` 
- example: compute determinant of $10\times 10$ matrix of BIG numbers with FFT
- Russian peasant algorithm, bad for multiplication,  
  good for exponentiation $O(N\log N)$
- best possible? NO! $a^{15}$; smallest $l(n)$, $l(191)$
- calculate polynomial; multiplication by Horner's method

## [lecture 14](https://www.youtube.com/watch?v=8I0z_Lobtso&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=14&pp=iAQB0gcJCSQMAYcqIYzv): Euler's $\varphi$ (totient) function

- number of residue classes (mod n) coprime to n
- $\varphi(mn)=\varphi(m)\varphi(n), (m,n)=1$
- $\varphi(n)=\varphi(p_1^{n_1})\varphi(p_2^{n_2})\dots$
- $\varphi(n)=p_1^{n_1-1}(p_1-1)p_2^{n_2-1}(p_2-1)\dots=n(1-\frac{1}{p_1})(1-\frac{1}{p_2})\dots$
- inclusion-exclusion principle
- probability interpretation
- find all numbers n with $\varphi(n)=24$
- Carmichael conjecture: given n, is there $m\neq n$ with $\varphi(n)=\varphi(m)$
- $\varphi(n)=$ power of 2? Construct n-gon
- how big is $\varphi(n)$?
- average value of $\varphi(n)/n$?
- probability m, n coprime is $\frac{\pi^2}{6}$
- generating function
- $\sum_{d\vert n}\varphi(d)=n$

## [lecture 13](https://www.youtube.com/watch?v=q99aBlC5Xfk&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=13&pp=iAQB0gcJCSQMAYcqIYzv): Chinese remainder theorem
- $ax\equiv b \mod m$ solvable iff b divisible by (a,m)
- (a,m)=1 then unique solution, (a,m)>1 then many solutions
- Solve polynomial $f(x)\equiv 0 \mod m$  
  (1) m prime: if $(a,m)=1$, a has inverse or $a\equiv 0$  
  (2) $m=p^n$ prime power, reduce to m=p (later)  
  (3) $m=p_1^{n_1}p_2^{n_2}\dots$, reduce to (2) using C.R.T.
- (3) reduce to (2), ho many solutions?

## [lecture 12](https://www.youtube.com/watch?v=3JBaDZqtgug&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=12&pp=iAQB): Wilsons theorem

- $(p-1)! \mod p$ ?
- $p$ prime implies $\equiv -1 \mod p$
- (useless) test for prime: $p$ is prime $\iff (p-1)! \equiv -1 \mod p$
- application: find $x^2\equiv -1 \mod p$  
  $p\equiv 3 \mod 4$ no solution
- $\left(\frac{p-1}{2}\right)!$ is $\sqrt{-1}$ if $p\equiv 1\mod 4$

$$\prod_{(a,m)=1} a = \begin{cases}
1 & \text{if >2 solutions exist to }x^2=1\\
-1 & \text{if -1 is only solution to }x^2=1\text{ (other than 1)}
\end{cases}$$

## [lecture 11](https://www.youtube.com/watch?v=V4cB7t-zHxE&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=11&pp=iAQB): Euler's theorem

- if $p$ divides $a^q-1$ with $p, q$ prime then either $p\equiv 1 \mod q$ or $a\equiv 1 \mod p$
- $\frac{x^q-1}{x-1}$
- infinitely many primes $\equiv 1 \mod 10$
- $a^x\equiv a^y$
- disjoint union of cycles, same size
- $a^{\varphi(m)}\equiv 1 \mod m, (a,m)=1$
- Lagrange; If $G$ is group, $g\in G$, then $ord(g) \vert \vert G\vert$
- primitive roots
- last two digits of $7^403$
- last digit of $7^{7^{7^7}}$

## [lecture 10](https://www.youtube.com/watch?v=fgHEKAdErbU&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=10&pp=iAQB): Fermat's theorem

- order of $a$ mod $p$, smallest $n>0$ with $a^n\equiv 1 \mod p$
- Fermat prime $2^n+1$, with $n$ power of $2$
- $p|2^{2^n}+1$, then $p\equiv 1 \mod 2^{n+1}$, Euler $641\vert 2^{2^5}+1$
- $a^2\equiv b^2 \mod m$ only if $m$ is prime
- $a^2\equiv b^2 \mod m^2$ implies $a\equiv \pm b \mod m$? No
- 

## [lecture 9](https://www.youtube.com/watch?v=E1tikA1GEVU&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=9&pp=iAQB): Congruences

- $a\equiv b (\mod c)$
- residue classes
- ring, zero divisor
- divisibility by 9, 11
- sum of three or four squares, three cubes
- Fermat: If p is prime, then $a^p\equiv a \mod p$
- fast modular exponentiation
- Carmichael number
- probabilistic prime number test
- if $p\vert n^2+1$, then $p=2$ or $p\equiv 1 \mod 4$

## [lecture 8](https://www.youtube.com/watch?v=KIvuGT5V1Fg&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=8&pp=iAQB): Applications of binomial coefficients

- fractal like pattern for Pascal's triangle "mod 2"
- "mod prime"
- 1000! ends in exactly 249 zeros
- powers of 7 dividing $\binom{100}{40}$ is two
- estimates on binomial size, Stirling formula for factorial
- simple prove of weak version of prime number theorem:   
  $\frac{1}{2}\frac{n}{\log{n}}\leq\pi(x)\leq 2\frac{n}{\log{n}}$
- Catalan numbers $\frac{1}{k+1}\binom{n}{k}$, generating function

## [lecture 7](https://www.youtube.com/watch?v=TBolWCObRgg&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=7&pp=iAQB): Binomial coefficients

- binomial $\binom{n}{k}$
  - $(x+y)^n=\binom{n}{0}x^ny^0+\binom{n}{1}x^{n-1}y^1+\dots$
  - #k-element subsets of n-element set
  - Pascal's triangle
  - $= \frac{n!}{(n-k)!k!}$
  - all four are equivalent
- trinomial
- Pascal's triangle
  - triangular numbers
  - tetrahedral numbers
  - 4-dim tetrahedon numbers
- basic properties of binomials
  - horizontal symmetry of Pascal's triangle
  - row n sum is $2^n$
  - alternating sign horizontal sum is 0 for $n>0$
  - sum of binomial mirror products
  - #ways driving from one point to another on a rectangular grid
  - k people, divide n coins, there are $\binom{n+k-1}{k-1}$ ways

## [lecture 6](https://www.youtube.com/watch?v=skTslDpxeL8&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=6&pp=iAQB): arithmetical functions

- multiplicative functions
  - d(n) #divisors
  - sigma(n) sum of divisors
  - Euler phi(n) #coprime <n
  - $$tau(n) = q (1-q)^{24} (1-q^2)^{24} \dots$$
  - $$mu(n) = (-1)^w(n)$$ if n squarefree and divisible by w(n) primes, 0 otherwise
  - why interesting: $$\frac{1}{zeta(s)} = \frac{1}{1^s} + \frac{mu(2)}{2^s} + \frac{mu(3)}{3^s} \dots$$
  - perfect numbers; Euclid $$n=2^{p-1}(2^p-1)$$ with $$2^p-1$$ prime, then n is perfect number
  - Euler: even perfect numbers are of this form
  - infinitely many even perfect numbers?
  - odd perfect numbers?
  - Landau (infinitely many): 
    - $$2n=p_1+p_2$$? (Goldbach conjecture)
    - $$p_1-p_2=2$$? (twin prime conjectore)
    - $$n^2 < p < (n+1)^2$$?
    - $$n^2+1$$?
    - likely all 4 are yes, but out of reach

## [lecture 5](https://www.youtube.com/watch?v=VRrP4US7idg&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=5&pp=iAQB): Primes

- negative prime: product with unit
- prime test: only primes as divisors, up to sqrt(N)
- fundamental theorem of arithmetic, proof; for poly
- no primes on reals
- no primes on functions of reals
- algebraic numbers m+sqrt(-1) gaussian integers unique factorization
- euclid numbers are not always prime
- Dirichlet: an+b infinitely many primes if (a,b)=1
- $$(2 p_1 p_2 ... p_k)^2+1$$ implies of form $$4n+1 or 2$$, not divisible by $$2, p_1,\dots,p_k$$ => infinitely many primes $$4n+1$$
- no bound on size of gaps between primes ($$n! + 2,3,\dots,n$$ all composite)
 
## [lecture 4](https://www.youtube.com/watch?v=R-O8j7FHEXI&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=4&pp=iAQB): More on Euclid's algorithm

- Euclid's algorithm allows to solve ax+by=d with (a,b)=d
- ax+by=c solvable <=> (a,b)|c
- works: polynomial in 1 variable
- fails: for polynomial in 2 variables
- works: in 3 variables
- better euclid, avoid long division  
  I implemented [gcds.cpp](../scripts/gcds.cpp) to compare ```gcd()```
  implementations using ```modulus``` (with long division)  
  and ```subtraction``` per [lecture 4, 15:45min](https://youtu.be/R-O8j7FHEXI?list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&t=945).
  Nothing can compare to builtin ```mpz_gcd()```,
  but tuned by Gemini implementations show subtraction being $3\times$ better that modulus, confirming lecturer statement:
  ```
  hermann@9950x:~$ ./gcds 5000000
  1,044,938-digit consecutive fibonaci numbers
  mpz_gcd(): 0.192115s
   loop mod: 110.977s (4999998)
   loop sub: 96.6452s (2451621)
  now both approaches tuned by Gemini
   loop mod: 81.1123s (4999998)
   loop sub: 26.2251s (2451621)
  hermann@9950x:~$ 
  ```
- lcm(a,b)=ab/gcd(a,b)

## [lecture 3](https://www.youtube.com/watch?v=pVKhDtOjji8&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=3&pp=iAQB): Divisibility and Euclid's algorithm

- a | b  "divides"
- n(n+1)(n+2)
- Euclid's division algorithm
- different methods to compute gcd
  - stupid, test 1,2,3,...
  - factorize (slow)
  - Euclid's algorithm
  - runtime analysis
    - fibonacci numbers worst case
    - #steps ≤ log(n)
    - formula F_n, guess->Ansatz
    - phi, golden ratio

----
- observation: divisors in Euclid's algorithm determne continued fraction
- Euclid's algorithm finitely many steps implies rational numbers are finite continued fractions

## [lecture 2](https://www.youtube.com/watch?v=mduJOLdKrak&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=2&pp=iAQB): Survey

- congruences
- Fermat's theorem
- Euler
- test if big n is prime
- quadratic residue
- quadratic reciprocity
- addititive number theory   
  - is every even number sum of two primes? (Goldbach)
- twin prime conjecture, Zhang, Tao
- Dirichlet: a+nb with (a,b)=1 has infinitely many primes
- $n^2+1$
  - likely contains infinitely many primes
  - nobody knows how to prove
- recreational number theory
  - perfect numbers 6,28,496
  - amicable numbers 220-284
  - 3n+1 problem
- algebraic number theory
  - m+ni, i=sqrt(-1)
  - Gaussian integers
    - unique factorization
    - 5=(2+i)(2-i)
- combinatorial number theory
  - partition p(n)
  - power series formula
  
## [lecture 1](https://www.youtube.com/watch?v=EzE6it9kAsI&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=1&pp=iAQB)
- primes
  - sieve of Eratosthenes
- infinitely many primes
  - $p_{n+1}=p_1\times\dots\times p_n+1$
  - if $p_{n+1}$ is not prime, take smallest prime factor of $p_{n+1}$ as $p_{n+1}$
  - product of no primes is 1, $1+1=2=p_1$
  - next $2+1=3=p_2$, then $2\times 3+1=7=p_3$, $2\times 3\times 7+1=43=p_4$
  - then $2\times 3\times 7\times 43+1=1807=13\times 139$, so $p_5=13$, $\dots$
- how to find large primes?
  - Mersenne prime $2^n-1$
  - open problem: infinitely many?
- Fermat primes
  - $2^n+1$, n=ab with a odd, divisible by $2^a+1$
  - better $2^{2^n}+1$, only prime for $n<5$
- generate large primes
  - $f(n)=n^2+n+41$, prime for $0≤n≤40$, not prime for $n=41$
  - no polynomial can always produce primes
- $π(n)$ number of primes ≤n, roughly $n/log(n)$
  - problem with infinite sums
- $Li(x) = \int_0^x 1/log(x) dx$
- Riemann: prime powers
  - $p^n$ counts as $1/n$
- $π'(n) = $# $prime powers ≤n$
  - $= Li(x) - \sum_p Li(x^p)$   "zeta function zeros"
- $zeta(2)=\frac{1}{1^2}+\frac{1}{2^2}+\frac{1}{3^2}+... = \frac{π^2}{6}$
  - rho with $zeta(rho)=0$
    - hypothesis: $Re(rho)≤1/2$
 - unique prime factorization
- $\frac{1}{1^s}+\frac{1}{2^s}+\frac{1}{3^s}+\dots = \frac{1}{1-2^{-s}}\frac{1}{1-3^{-s}}\frac{1}{1-5^{-s}}\dots$
- diophantine equations
- $x^n+y^n=z^n$ (Fermat, $n\geq 3$, $x,y,z>0$)
- $x^4+y^4+z^4=t^4$, big solutions
- Hilbert's 10th problem:
  - is there algorithm to solve all diophantine equations?
  - no
- Pell's equation
- $1729$ sum of two cube in two different ways
 
