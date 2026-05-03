/*
   Result of a very long session with Google Gemini.

f=avx2_fma_double_openmp
gcc -O3 -mavx2 -mfma -fopenmp $f.c -o $f
objdump -d $f | sed -n "/vfmadd132pd/,/jne/p"
sed -n "/^ .*long i/,/^    }/p" $f.c
echo 0 | sudo tee /proc/sys/kernel/perf_event_paranoid
OMP_NUM_THREADS=192 perf stat -a -e r10c7,cycles,instructions,task-clock ./$f

...
10.240.000.000.000      fp_ret_sse_avx_ops.mac_flops     #   79,001 G/sec
...
       8,118225634 seconds time elapsed
...

10240000000000 / (8.118225634 * 10^9) = 1261 GFLOPS (AMD 7950X)

*/
#include <immintrin.h>
#include <stdio.h>
#include <omp.h>

int main() {
  // We tell OpenMP to parallelize this block across all threads
  #pragma omp parallel
  {
    // 512-bit vectors of doubles (8 doubles per register)
    // We use a multiplier very close to 1, and a tiny increment.
    // Initialize 4 independent accumulators
    __m256d a0 = _mm256_set1_pd(1.0);
    __m256d a1 = _mm256_set1_pd(1.01);
    __m256d a2 = _mm256_set1_pd(1.02);
    __m256d a3 = _mm256_set1_pd(1.03);
    __m256d b = _mm256_set1_pd(0.999999999); 
    __m256d c = _mm256_set1_pd(0.000000001);

    // Theoretical limit: c / (1 - b) = 1.0
    // With 10^10 iterations, it will climb steadily but won't quite hit 1.0
    for (long i = 0; i < 10000000000L; ++i) {
        a0  = _mm256_fmadd_pd(a0,  b, c);
        a1  = _mm256_fmadd_pd(a1,  b, c);
        a2  = _mm256_fmadd_pd(a2,  b, c);
        a3  = _mm256_fmadd_pd(a3,  b, c);
    }

    // a0  = _mm256_fmadd_pd(a0,  b, c); // odd #fma, increase by 2

    double res[4];
    _mm256_storeu_pd(res, a0);
    printf("Results 0-3: %.12f  ", res[0]);
    _mm256_storeu_pd(res, a1);
    printf("%.12f  ", res[0]);
    _mm256_storeu_pd(res, a2);
    printf("%.12f  ", res[0]);
    _mm256_storeu_pd(res, a3);
    printf("%.12f\n", res[0]);
  }
  printf("Finished %d-core AVX2 workload.\n", omp_get_max_threads());

  return 0;
}
