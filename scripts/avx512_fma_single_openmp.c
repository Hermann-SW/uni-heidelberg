/*
   Result of a very long session with Google Gemini.

f=avx512_fma_single_openmp
gcc -O3 -mavx512f -mfma -fopenmp $f.c -o $f
objdump -d $f | sed -n "/vfmadd132ps/,/jne/p"
sed -n "/^ .*long i/,/^    }/p" $f.c
echo 0 | sudo tee /proc/sys/kernel/perf_event_paranoid
OMP_NUM_THREADS=16 perf stat -e fp_ret_sse_avx_ops.mac_flops,cycles,instructions,task-clock ./$f

...
20,480,000,000,000      fp_ret_sse_avx_ops.mac_flops     #  160.463 G/sec
...
       7.999684626 seconds time elapsed
...

20480000000000 / (7.999684626 * 10^9) = 2560 GFLOPS (AMD 7950X)

*/
#include <immintrin.h>
#include <stdio.h>
#include <omp.h>

int main() {
  // We tell OpenMP to parallelize this block across all threads
  #pragma omp parallel
  {
    // 512-bit vectors of singles (16 singles per register)
    // We use a multiplier very close to 1, and a tiny increment.
    // Initialize 4 independent accumulators
    __m512 a0 = _mm512_set1_ps(1.0);
    __m512 a1 = _mm512_set1_ps(1.01);
    __m512 a2 = _mm512_set1_ps(1.02);
    __m512 a3 = _mm512_set1_ps(1.03);
    __m512 b = _mm512_set1_ps(0.999999999); 
    __m512 c = _mm512_set1_ps(0.000000001);

    // Theoretical limit: c / (1 - b) = 1.0
    // With 10^10 iterations, it will climb steadily but won't quite hit 1.0
    for (long i = 0; i < 10000000000L; ++i) {
        a0  = _mm512_fmadd_ps(a0,  b, c);
        a1  = _mm512_fmadd_ps(a1,  b, c);
        a2  = _mm512_fmadd_ps(a2,  b, c);
        a3  = _mm512_fmadd_ps(a3,  b, c);
    }

    // a0  = _mm512_fmadd_pd(a0,  b, c); // odd #fma, increase by 2*(512/64)

    float res[16];
    _mm512_storeu_ps(res, a0);
    printf("Results 0-3: %.12f  ", res[0]);
    _mm512_storeu_ps(res, a1);
    printf("%.12f  ", res[0]);
    _mm512_storeu_ps(res, a2);
    printf("%.12f  ", res[0]);
    _mm512_storeu_ps(res, a3);
    printf("%.12f\n", res[0]);
  }
  printf("Finished %d-core AVX-512 workload.\n", omp_get_max_threads());

  return 0;
}
