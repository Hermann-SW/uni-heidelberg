[avx512_fma_double_openmp.c](../scripts/avx512_fma_double_openmp.c)

```
hermann@7950x:~$ f=avx512_fma_double_openmp
hermann@7950x:~$ gcc -O3 -mavx512f -mfma -fopenmp $f.c -o $f
hermann@7950x:~$ 
```

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

Computing GFLOPS with 16 double precison operations per perf counter "fp_ret_sse_avx_ops.mac_flops":  
10240000000000 * 16 / (8.118225634 * 10^9) = 20181 GFLOPS (AMD 7950X) = 20.18 TFLOPS FP64

Single core execution runs at 5.538 GHz instead of 4.951 GHz for all 16 cores, resulting in 1.41 TFLOPS FP64:  
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

Doing same runs on 8C/16T AMD 8840HS laptop processor shows 8.49 TFLOPS / 1.26 TFLOPS when running with all 8 cores / single core (at 4.18 GHz / 4.97 GHz).
