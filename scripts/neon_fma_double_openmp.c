/*
   Result of a very long session with Google Gemini.

f=neon_fma_double_openmp
gcc -O3 -mcpu=cortex-a76 -ffast-math -fopenmp $f.c -o $f
objdump -d $f | sed -n "/subs/,/b\.ne/p"
sed -n "/^ .*long i/,/^    }/p" $f.c
echo 0 | sudo tee /proc/sys/kernel/perf_event_paranoid
OMP_NUM_THREADS=4 perf stat -e r74,cycles,instructions,task-clock ./$f

...
10.240.000.000.000      fp_ret_sse_avx_ops.mac_flops     #   79,001 G/sec
...
       8,118225634 seconds time elapsed
...

10240000000000 / (8.118225634 * 10^9) = 1261 GFLOPS (AMD 7950X)

*/
#include <arm_neon.h>
#include <stdio.h>
#include <omp.h>

int main() {
  // We tell OpenMP to parallelize this block across all threads
  #pragma omp parallel
  {
    // 512-bit vectors of doubles (8 doubles per register)
    // We use a multiplier very close to 1, and a tiny increment.
    // Initialize 4 independent accumulators
    float64x2_t a0 = vdupq_n_f64(1.0);
    float64x2_t a1 = vdupq_n_f64(1.01);
    float64x2_t a2 = vdupq_n_f64(1.02);
    float64x2_t a3 = vdupq_n_f64(1.03);
    float64x2_t b = vdupq_n_f64(0.999999999); 
    float64x2_t c = vdupq_n_f64(0.000000001);

    // Theoretical limit: c / (1 - b) = 1.0
    // With 10^10 iterations, it will climb steadily but won't quite hit 1.0
    for (long i = 0; i < 10000000000L; ++i) {
        a0  = vfmaq_f64(a0,  b, c);
        a1  = vfmaq_f64(a1,  b, c);
        a2  = vfmaq_f64(a2,  b, c);
        a3  = vfmaq_f64(a3,  b, c);
    }

    // a0  = vfmaq_f64(a0,  b, c); // odd #fma, increase by 4

    double res[2];
    vst1q_f64(res, a0);
    printf("Results 0-3: %.12f  ", res[0]);
    vst1q_f64(res, a1);
    printf("%.12f  ", res[0]);
    vst1q_f64(res, a2);
    printf("%.12f  ", res[0]);
    vst1q_f64(res, a3);
    printf("%.12f\n", res[0]);
  }
  printf("Finished %d-core neon workload.\n", omp_get_max_threads());

  return 0;
}
