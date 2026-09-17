## Berkeley math 115: Introduction to number theory

- Youtube lecture series [spring 2022](https://www.youtube.com/watch?v=EzE6it9kAsI&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=1)

[9](#lecture-9-congruences)
[8](#lecture-8-applications-of-binomial-coefficients)
[7](#lecture-7-binomial-coefficients)
[6](#lecture-6-arithmetical-functions)
[5](#lecture-5-primes)
[4](#lecture-4-more-on-euclids-algorithm)
[3](#lecture-3-divisibility-and-euclids-algorithm)
[2](#lecture-2-survey)
[1](#lecture-1)

## lecture 9: Congruences

-

## lecture 8: Applications of binomial coefficients

- fractal like pattern for Pascal's triangle "mod 2"
- "mod prime"
- 1000! ends in exactly 249 zeros
- powers of 7 dividing $\binom{100}{40}$ is two
- estimates on binomial size, Stirling formula for factorial
- simple prove of weak version of prime number theorem:   
  $\frac{1}{2}\frac{n}{\log{n}}\leq\pi(x)\leq 2\frac{n}{\log{n}}$
- Catalan numbers $\frac{1}{k+1}\binom{n}{k}$, generating function

## lecture 7: Binomial coefficients

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

## lecture 6: arithmetical functions

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

## lecture 5: Primes

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
 
## lecture 4: More on Euclid's algorithm

- Euclid's algorithm allows to solve ax+by=d with (a,b)=d
- ax+by=c solvable <=> (a,b)|c
- works: polynomial in 1 variable
- fails: for polynomial in 2 variables
- works: in 3 variables
- better euclid, avoid long division
- lcm(a,b)=ab/gcd(a,b)

## lecture 3: Divisibility and Euclid's algorithm

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

## lecture 2: Survey

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
  
## lecture 1
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
 
