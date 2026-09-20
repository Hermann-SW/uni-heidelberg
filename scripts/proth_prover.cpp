// NOLINT(legal/copyright)
/*
$ g++ -O3 -std=c++17 proth_prover.cpp -o proth_prover -lgmpxx -lgmp
$ ./proth_prover
Digits of N: 1749
CRT primes set up: 364 primes (Max: 4294967291)
Precomputing Garner CRT coefficients...
Starting modular exponentiation (3^((N-1)/2) mod N)...
Progress: bit 0 / 5807             
  -> Total Exponentiation time: 3054 ms
Comparing result against N - 1...
Success! Result matches N - 1. N is prime!
$ 
*/
#include <gmpxx.h>
#include <iostream>
#include <vector>
#include <chrono>  // NOLINT(build/c++11)
#include <cmath>
#include <cstdint>

// Optimized Garner CRT structure with native precomputed tables
struct GarnerCRT {
    std::vector<uint64_t> primes;
    // inv_table[i][j] stores p_j^{-1} mod p_i
    std::vector<std::vector<uint64_t>> inv_table;
};

GarnerCRT precompute_garner(const std::vector<uint64_t>& primes) {
    size_t k = primes.size();
    GarnerCRT gc;
    gc.primes = primes;
    gc.inv_table.resize(k);

    for (size_t i = 0; i < k; ++i) {
        gc.inv_table[i].resize(i);
        for (size_t j = 0; j < i; ++j) {
            mpz_class inv;
            if (!mpz_invert(inv.get_mpz_t(), mpz_class(primes[j]).get_mpz_t(),
                            mpz_class(primes[i]).get_mpz_t())) {
                std::cerr << "Error: modular inverse failed during"
                          << " Garner precomputation\n";
            }
            gc.inv_table[i][j] = inv.get_ui();
        }
    }
    return gc;
}

// Ultra-fast Garner Reconstruction: ZERO GMP heap allocations in inner loops
mpz_class garner_reconstruct(const std::vector<uint64_t>& residues_C,
                             const GarnerCRT& gc) {
    size_t k = gc.primes.size();
    std::vector<uint64_t> v(k);

    for (size_t i = 0; i < k; ++i) {
        uint64_t vi = residues_C[i];
        uint64_t p_i = gc.primes[i];

        for (size_t j = 0; j < i; ++j) {
            int64_t diff = static_cast<int64_t>(vi)-static_cast<int64_t>(v[j]);
            uint64_t rem;
            if (diff >= 0) {
                rem = diff % p_i;
            } else {
                rem = p_i - ((-diff) % p_i);
            }
            vi = (rem * gc.inv_table[i][j]) % p_i;
        }
        v[i] = vi;
    }

    // Combine mixed-radix digits into final big integer (only once per mult)
    mpz_class X = v[0];
    mpz_class term = 1;
    for (size_t i = 1; i < k; ++i) {
        term *= gc.primes[i - 1];
        X += mpz_class(v[i]) * term;
    }
    return X;
}

// Full RNS multiply + Two-Fold Proth reduction matching PARI/GP's trunc div
mpz_class rns_mul(const mpz_class& A, const mpz_class& B,
                  const GarnerCRT& garner_ctx,
                  const mpz_class& k_inv, const mpz_class& N,
                  const mpz_class& two_n) {
    size_t num_primes = garner_ctx.primes.size();
    std::vector<uint64_t> residues_C(num_primes);

    for (size_t i = 0; i < num_primes; ++i) {
        uint64_t p = garner_ctx.primes[i];
        uint64_t rA = mpz_fdiv_ui(A.get_mpz_t(), p);
        uint64_t rB = mpz_fdiv_ui(B.get_mpz_t(), p);
        residues_C[i] = (rA * rB) % p;
    }

    mpz_class res_v = garner_reconstruct(residues_C, garner_ctx);

    // Fold 1: res_v is >= 0, so floor and truncating are identical
    mpz_class H1 = res_v / two_n;
    mpz_class L1 = res_v % two_n;
    mpz_class d = L1 - H1 * k_inv;

    // Fold 2: d can be negative; use standard C++ truncating div; match PARI/GP
    mpz_class H2 = d / two_n;
    mpz_class L2 = d % two_n;
    mpz_class e = L2 - H2 * k_inv;

    // Final normalization modulo N (exact PARI/GP equivalent)
    mpz_class res = e % N;
    if (res < 0) {
        res += N;
    }
    return res;
}

// Single-round Miller-Rabin test using GMP modular exponentiation
inline bool miller_rabin_test(uint32_t n, uint32_t a, uint32_t d, int s) {
    mpz_class base(a), exp(d), mod(n), x;

    // x = (a^d) % n
    mpz_powm(x.get_mpz_t(), base.get_mpz_t(), exp.get_mpz_t(), mod.get_mpz_t());

    if (x == 1 || x == n - 1) return true;

    for (int r = 1; r < s; r++) {
        // x = (x^2) % n
        mpz_powm_ui(x.get_mpz_t(), x.get_mpz_t(), 2, mod.get_mpz_t());
        if (x == n - 1) return true;
    }
    return false;
}

// 100% Deterministic Miller-Rabin Primality Test for N < 2^32
// proof of correctness:  https://gist.github.com/Hermann-SW/5ffc3bbe45c59130f0fb05caf674d441
inline bool is_prime_u32(uint32_t n) {
    if (n < 2) return false;
    if (n == 2 || n == 3 || n == 5 || n == 7) return true;
    if (n % 2 == 0 || n % 3 == 0 || n % 5 == 0) return false;

    uint32_t d = n - 1;
    int s = 0;
    while (d % 2 == 0) {
        d /= 2;
        s++;
    }

    // Proven base set for n < 2^32 (Jaeschke, 1993)
    static const uint32_t bases[] = {2, 7, 61};

    for (uint32_t a : bases) {
        if (n <= a) break;
        if (!miller_rabin_test(n, a, d, s)) return false;
    }

    return true;
}

int main() {
    mpz_class k = 5795;
    mpz_class n = 5795;
    mpz_class two_n;
    mpz_ui_pow_ui(two_n.get_mpz_t(), 2, n.get_ui());
    mpz_class N = k * two_n + 1;

    if (k % 3 == 0) {
        std::cerr << "error: correct only for k%3!=0\n";
        return 1;
    }

    std::cout << "Digits of N: " << mpz_sizeinbase(N.get_mpz_t(), 10)
              << std::endl;

    // 1. Build the prime list downwards from prime 4294967291
    double target_log = 2.0 * mpz_sizeinbase(N.get_mpz_t(), 2) * log(2.0);
    std::vector<uint64_t> primes_list;
    double current_log = 0.0;

    uint32_t p = UINT_MAX;
    while (current_log < target_log) {
        while (!is_prime_u32(p)) {
            p -= 2;
        }
        primes_list.push_back(p);
        p -= 2;
        current_log += log(p);
    }

    std::cout << "CRT primes set up: " << primes_list.size()
              << " primes (Max: " << primes_list.front() << ")" << std::endl;

    std::cout << "Precomputing Garner CRT coefficients..." << std::endl;
    GarnerCRT garner_ctx = precompute_garner(primes_list);

    mpz_class k_inv;
    if (!mpz_invert(k_inv.get_mpz_t(), k.get_mpz_t(), N.get_mpz_t())) {
        std::cerr << "Error: k is not invertible mod N\n";
        return 1;
    }

    // 2. Binary Exponentiation Loop
    mpz_class exp1 = (N - 1) / 2;
    std::cout << "Starting modular exponentiation (3^((N-1)/2) mod N)..."
              << std::endl;

    auto t1 = std::chrono::high_resolution_clock::now();

    mpz_class acc = 1;
    mpz_class base_val = 3;
    uint32_t bit_len = mpz_sizeinbase(exp1.get_mpz_t(), 2);

    for (int32_t i = bit_len - 1; i >= 0; --i) {
        acc = rns_mul(acc, acc, garner_ctx, k_inv, N, two_n);
        if (mpz_tstbit(exp1.get_mpz_t(), i)) {
            acc = rns_mul(acc, base_val, garner_ctx, k_inv, N, two_n);
        }

        if (i % 500 == 0) {
            std::cout << "\rProgress: bit " << i << " / "
                      << bit_len << std::flush;
        }
    }
    std::cout << "\rProgress: bit 0 / " << bit_len
              << "             " << std::endl;


    auto t2 = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>
                        (t2 - t1).count();
    std::cout << "  -> Total Exponentiation time: " << duration
              << " ms" << std::endl;

    // 3. Final Verification
    std::cout << "Comparing result against N - 1..." << std::endl;
    if (acc == N - 1) {
        std::cout << "Success! Result matches N - 1. N is prime!" << std::endl;
    } else {
        std::cout << "Result mismatch: " << acc << std::endl;
    }

    return 0;
}
