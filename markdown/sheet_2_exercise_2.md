```
Exercise 2 (Peak Performance) shortened:    
…, it is useful to consider additional metrics.  
Two common ones are operation throughput (GFlops/s) and memory bandwidth (GB/s). …  
a) Determine the peak performance of your processor (single-core and all cores) …  
b) Explain where these peak values come from …  
```

Single-core peak performance in 1-core, multi-core peak performance in rightmost column:  

|     |  [GFLOPS] ([GHz])    | units|×counter|       1-core|      4-core  |     8-core   |    16-core   |    22-core  |    24-core  | |  2-socket   | 4-socket    | 8-socket    |
|:---:|:--------------------:|:----:|:------:|:-----------:|:-------------|:------------:|:------------:|:-----------:|:-----------:|-|:-----------:|:-----------:|:-----------:|
| AMD Ryzen |7950X  16C/32T  |AVX512|   1    |   87 (5.54) |       —      |  681  (5.42) |  1261 (4.95) |      —      |      —      | |      —      |      —      |      —      |
| AMD Ryzen |8840HS  8C/16T  |AVX512|   1    |   80 (4.97) |       —      |  531  (4.18) |       —      |      —      |      —      | |      —      |      —      |      —      |
|Intel XEON |8890v4 24C/48T  | AVX2 |   4    |    22 (3.39)|       —      |       —      |       —      |      —      |  396 (2.59) | |  675 (2.59) | 1321 (2.59) |  2632 (2.59)|
|Intel XEON |2696v4 22C/44T  | AVX2 |   4    |    17 (2.80)|       —      |       —      |       —      |  330 (2.80) |      —      | |  631 (2.80) |      —      |      —      |
| ARM Cortex|A76 4C/8T       | NEON |   2    |    12 (3.00)|    48 (3.00) |       —      |       —      |      —      |      —      | |      —      |      —      |      —      |
  
  
[avx512_fma_double_openmp.c](../scripts/avx512_fma_double_openmp.c)  
[avx2_fma_double_openmp.c](../scripts/avx2_fma_double_openmp.c)  
[neon_fma_double_openmp.c](../scripts/neon_fma_double_openmp.c)  

Types of differences:  
```
  gcc -O3 -mavx512f -mfma -fopenmp $f.c -o $f
  gcc -O3 -mavx2 -mfma -fopenmp $f.c -o $f
  gcc -O3 -mcpu=cortex-a76 -ffast-math -fopenmp $f.c -o $f
```
```
  objdump -d $f | sed -n "/vfmadd132pd/,/jne/p"
  objdump -d $f | sed -n "/vfmadd132pd/,/jne/p"
  objdump -d $f | sed -n "/subs/,/b\.ne/p"
```
  
  

AVX512 perf counter "fp_ret_sse_avx_ops.mac_flops" increments by 2×(512/64)=16 for fma (1 multiplication, 1 addition).    
AVX2 perf counter "r10c7" increments by 2 for fma, additional multiply by (256/64)=4 needed.    
NEON perf counter "r74" increments by 1 for fma, additional multiply by (128/64)=2 needed.    
```
  OMP_NUM_THREADS=16 perf stat -e fp_ret_sse_avx_ops.mac_flops,cycles,instructions,task-clock ./$f
  OMP_NUM_THREADS=192 perf stat -a -e r10c7,cycles,instructions,task-clock ./$f
  OMP_NUM_THREADS=4 perf stat -e r74,cycles,instructions,task-clock ./$f
```
```
  #include <immintrin.h>
  #include <immintrin.h>
  #include <arm_neon.h>
```
```
      __m512d a0 = _mm512_set1_pd(1.0);
      __m256d a0 = _mm256_set1_pd(1.0);
      float64x2_t a0 = vdupq_n_f64(1.0);
```
```
          a0  = _mm512_fmadd_pd(a0,  b, c);
          a0  = _mm256_fmadd_pd(a0,  b, c);
          a0  = vfmaq_f64(a0,  b, c);
```
```
      // a0  = _mm512_fmadd_pd(a0,  b, c); // odd #fma, increase by 2*(512/64)
      // a0  = _mm256_fmadd_pd(a0,  b, c); // odd #fma, increase by 2
      // a0  = vfmaq_f64(a0,  b, c); // odd #fma, increase by 1
```
```
      double res[8];
      double res[4];
      double res[2];
```
```
      _mm512_storeu_pd(res, a0);
      _mm256_storeu_pd(res, a0);
      vst1q_f64(res, a0);
```
  
  
Compile:  
```
hermann@7950x:~$ f=avx512_fma_double_openmp
hermann@7950x:~$ gcc -O3 -mavx512f -mfma -fopenmp $f.c -o $f
hermann@7950x:~$ 
```
  
  
Compare innermost loop in assembler and C:  
```
hermann@7950x:~$ objdump -d $f | sed -n "/vfmadd132pd/,/jne/p"
    1240:	62 f2 fd 48 98 e9    	vfmadd132pd %zmm1,%zmm0,%zmm5
    1246:	62 f2 fd 48 98 e1    	vfmadd132pd %zmm1,%zmm0,%zmm4
    124c:	62 f2 fd 48 98 d9    	vfmadd132pd %zmm1,%zmm0,%zmm3
    1252:	62 f2 fd 48 98 d1    	vfmadd132pd %zmm1,%zmm0,%zmm2
    1258:	48 83 e8 01          	sub    $0x1,%rax
    125c:	75 e2                	jne    1240 <main._omp_fn.0+0x70>
hermann@7950x:~$ sed -n "/long i/,/^    }/p" $f.c 
    for (long i = 0; i < 10000000000L; ++i) {
        a0  = _mm512_fmadd_pd(a0,  b, c);
        a1  = _mm512_fmadd_pd(a1,  b, c);
        a2  = _mm512_fmadd_pd(a2,  b, c);
        a3  = _mm512_fmadd_pd(a3,  b, c);
    }
hermann@7950x:~$ 
```
  
  
Execute with 16 threads:  
```
hermann@7950x:~$ echo 0 | sudo tee /proc/sys/kernel/perf_event_paranoid
[sudo] password for hermann: 
0
hermann@7950x:~$ OMP_NUM_THREADS=16 perf stat -e fp_ret_sse_avx_ops.mac_flops,cycles,instructions,task-clock ./$f
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Finished 16-core AVX-512 workload.

 Performance counter stats for './avx512_fma_double_openmp':

10.240.000.000.000      fp_ret_sse_avx_ops.mac_flops     #   79,001 G/sec                     
   641.682.840.447      cycles                           #    4,951 GHz                       
   960.941.039.529      instructions                     #    1,50  insn per cycle            
        129.619,13 msec task-clock                       #   15,966 CPUs utilized             

       8,118225634 seconds time elapsed

     129,618583000 seconds user
       0,000999000 seconds sys


hermann@7950x:~$
```
  
  
Computing 7950X peak performance  with 16 double precison operations per perf counter "fp_ret_sse_avx_ops.mac_flops":  
```
10240000000000 / (8.118225634 * 10^9) = 1261 GFLOPS (AMD 7950X)
```
  
  
Single-core execution runs at 5.538 GHz instead of 4.951 GHz for all 16 cores, resulting in 87 GFLOPS FP64:  
```
hermann@7950x:~$ OMP_NUM_THREADS=1 perf stat -e fp_ret_sse_avx_ops.mac_flops,cycles,instructions,task-clock ./$f
Results 0-3: 1.000000000000  1.000000491214  1.000000940659  1.000001393028
Finished 1-core AVX-512 workload.

 Performance counter stats for './avx512_fma_double_openmp':

   640.000.000.000      fp_ret_sse_avx_ops.mac_flops     #   88,427 G/sec                     
    40.082.548.500      cycles                           #    5,538 GHz                       
    60.067.840.162      instructions                     #    1,50  insn per cycle            
          7.237,62 msec task-clock                       #    1,000 CPUs utilized             

       7,238446712 seconds time elapsed

       7,238086000 seconds user
       0,000000000 seconds sys


hermann@7950x:~$ 
```
  
  
For the other CPUs find peak performances and CPU frequencies in above table.  
