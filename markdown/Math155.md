## lecture 1
- primes
  - sieve of Eratosthenes
- infinitely many primes
  - $p_{n+1}=p_1*...*p_n$
  - wrong statement: $p_{n+1}$ is prime
  - if $p_{n+1}$ is not prime, take smallest prime factor of $p_{n+1}$ as $p_{n+1}$
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
 
## lecture 2: Survey

- congruences
- Fermat's theorem
- Euler
- test if big n is prime
- quadratic residue
- quadratic reciprocity
- addititive number theory, every even number is sum of two primes (Goldbach)
- twin prime conjecture, Zheng, Tao
- Dirichlet: a+nb with (a,b)=1 has infinitely many primes 
- recreational number theory
  - perfect numbers 6,28,496
  - amicable numbers 220-284
  - 3n+1
- algebraic number theory
  - m+ni, i=sqrt(-1)
  - Gaussian integers
    - unique factorization
    - 5=(2+i)(2-i)
- combinatorial number theory
  - partition p(n)
  - power series formula
  
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

## lecture 4: More on Euclid's algorithm

- Euclid's algorithm allows to solve ax+by=d with (a,b)=d
- ax+by=c solvable <=> (a,b)|c
- works: polynomial in 1 variable
- fails: for polynomial in 2 variables
- works: in 3 variables
- better euclid, avoid long division
- lcm(a,b)=ab/gcd(a,b)

## lecture 5
