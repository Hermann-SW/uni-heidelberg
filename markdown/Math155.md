## Berkeley math 115: Introduction to number theory

- Youtube lecture series [spring 2022](https://www.youtube.com/watch?v=EzE6it9kAsI&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=1)

Lectures:
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

# [lecture 16](https://www.youtube.com/watch?v=roBKA4adPJE&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=16&pp=iAQB): More numerical calculation 

# [lecture 15](https://www.youtube.com/watch?v=ne0gHR57qUU&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=15&pp=iAQB): Numerical calculation 

- (1) solve ax+by=c  
  (2) Is n prime? Factorize it  
  (3) Solve $f(x)\equiv 0\mod p$; $x^2+1\equiv 0 \mod p$  
  (4) $a^b \mod m$
- O() notation
- Fast Fourier Transform: $O(N\log N)+O(N)+O(N\log N)$  
  FFT (choose $P=2\cdot 3\cdot\dots >mn$)  
  pointwise multiplication (modulo the prime divisors of P)  
  inverse FFT (use C.R.T. to reconstruct $mn \mod P$)
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
 
