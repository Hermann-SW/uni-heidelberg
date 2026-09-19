/*
- Proth (k*2^n+1) primality prover for k%3!=0 prototype 
- using "RNS/CRT/folding reduction" multiplication
- result of long chat with Gemini

41 seconds below is loooong compared to same builtin proof ;-)

$ gp -q
? k=5795;n=5795;N=k*2^n+1;#digits(N)
1749
? Mod(3,N)^((N-1)/2)==Mod(-1,N)
1
? ##
  ***   last result: cpu time 31 ms, real time 31 ms.
? 

But prototype fully works with 3500 decimal digits in between:

hermann@9950x:~/uni-heidelberg/scripts$ gp -q < proth.gp 
Digits of N: 1749
CRT primes set up: 1027 primes (Max: 8179)
Starting modular exponentiation (3^((N-1)/2) mod N)...
  -> Total Exponentiation time: 40401 ms
Comparing result against N - 1...
Success! Result matches N - 1. N is prime!
hermann@9950x:~/uni-heidelberg/scripts$ 
*/
k = 5795;
n = 5795;
N = k * 2^n + 1;

if(k%3==0, error("correct only for k%3!=0"));

print("Digits of N: ", #digits(N));

/* 1. Build the prime list for N^2 */
target_log = log(N^2);
primes_list = [];
current_log = 0;
p = 2;
{
while(current_log < target_log,
    primes_list = concat(primes_list, p);
    current_log += log(p);
    p = nextprime(p + 1);
);
}

num_primes = #primes_list;
print("CRT primes set up: ", num_primes, " primes (Max: ", primes_list[num_primes], ")");

/* Precompute k^(-1) mod N for Proth folding */
k_inv = lift(Mod(k, N)^(-1));

/* Helper function: full RNS multiply + Two-Fold Proth reduction */
rns_mul(A, B) = {
    local(res_A, res_B, res_C, res_v, mod_acc, p_prime, c_val, i, L1, H1, d, L2, H2, e);
    
    /* Forward RNS projection */
    res_A = vector(num_primes, i, Mod(A, primes_list[i]));
    res_B = vector(num_primes, i, Mod(B, primes_list[i]));
    
    /* Parallel residue multiplication */
    res_C = vector(num_primes, i, res_A[i] * res_B[i]);
    
    /* CRT Reconstruction */
    res_v = res_C[1];
    mod_acc = primes_list[1];
    for(i = 2, num_primes,
        p_prime = primes_list[i];
        c_val = res_C[i];
        res_v = chinese(res_v + O(mod_acc), c_val + O(p_prime));
        mod_acc *= p_prime;
    );
    res_v = lift(res_v);
    
    /* Proth Folding Reduction (Fold 1) */
    L1 = res_v % (2^n);
    H1 = res_v \ (2^n);
    d = L1 - H1 * k_inv;

    /* Proth Folding Reduction (Fold 2 for remaining high bits) */
    L2 = d % (2^n);
    H2 = d \ (2^n);
    e = L2 - H2 * k_inv;

    /* Final normalization modulo N */
    return (e % N);
};

/* 2. Binary Exponentiation Loop for Proth's Theorem */
exp1 = (N - 1) / 2;
print("Starting modular exponentiation (3^((N-1)/2) mod N)...");

gettime(); \\ reset timer
bits = binary(exp1);
acc = 1;
base_val = 3;

{
for(i = 1, #bits,
    acc = rns_mul(acc, acc);
    if(bits[i] == 1,
        acc = rns_mul(acc, base_val);
    );
);
print("  -> Total Exponentiation time: ", gettime(), " ms");

/* 3. Final Verification */
print("Comparing result against N - 1...");
if(acc == N - 1,
    print("Success! Result matches N - 1. N is prime!"),
    print("Result mismatch: ", acc)
);
}
