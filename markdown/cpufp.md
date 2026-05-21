[cpufp repo](https://github.com/pigirons/cpufp)

| Instruction Set | Vector Length | Core Computation      | Peak Performance |  Peak Performance |  Peak Performance |  Peak Performance |
|-----------------|---------------|-----------------------|------------------| ------------------| ------------------| ------------------|
||||8840HS<BR>8C|7950X<BR>16C|E5-2696v4<BR>2×22C|E7-8890v4<BR>8×24C|
| AVX512_VNNI     | 512b          | DP4A(s32,u8,s8)       | 4.5797 TOPS      |  10.642 TOPS      |                   |                   |
| AVX512_VNNI     | 512b          | DP2A(s32,s16,s16)     | 2.2133 TOPS      |  5.3042 TOPS      |                   |                   |
| AVX512_BF16     | 512b          | DP2A(f32,bf16,bf16)   | 2.1396 TFLOPS    |  5.304 TFLOPS     |                   |                   |
| AVX512F         | 512b          | FMA(f32,f32,f32)      | 1.0786 TFLOPS    |  2.65 TFLOPS      |                   |                   |
| AVX512F         | 512b          | FMA(f64,f64,f64)      | 537.33 GFLOPS    |  1.3176 TFLOPS    |                   |                   |
| AVX512F         | 512b          | ADD(MUL(f32,f32),f32) | 698.66 GFLOPS    |  2.1985 TFLOPS    |                   |                   |
| AVX512F         | 512b          | ADD(MUL(f64,f64),f64) | 435.57 GFLOPS    |  1.0934 TFLOPS    |                   |                   |
|||||||
| AVX512_VNNI     | 256b          | DP4A(s32,u8,s8)       | 4.006 TOPS       |  9.983 TOPS       |                   |                   |
| AVX512_VNNI     | 256b          | DP2A(s32,s16,s16)     | 2.0123 TOPS      |  5.0116 TOPS      |                   |                   |
| AVX512_BF16     | 256b          | DP2A(f32,bf16,bf16)   | 2.0298 TFLOPS    |  5.099 TFLOPS     |                   |                   |
| FMA             | 256b          | FMA(f32,f32,f32)      | 1.0233 TFLOPS    |  2.5488 TFLOPS    |  3.6467 TFLOPS    |  15.807 TFLOPS    |
| FMA             | 256b          | FMA(f64,f64,f64)      | 503.69 GFLOPS    |  1.2666 TFLOPS    |  1.8208 TFLOPS    |  7.8989 TFLOPS    |
| AVX             | 256b          | ADD(MUL(f32,f32),f32) | 958.14 GFLOPS    |  2.3504 TFLOPS    |  1.823 TFLOPS     |  7.8977 TFLOPS    |
| AVX             | 256b          | ADD(MUL(f64,f64),f64) | 460.8 GFLOPS     |  1.1402 TFLOPS    |  912.13 GFLOPS    |  3.9495 TFLOPS    |
|||||||
| AVX512_VNNI     | 128b          | DP4A(s32,u8,s8)       | 2.1142 TOPS      |  5.2004 TOPS      |                   |                   |
| AVX512_VNNI     | 128b          | DP2A(s32,s16,s16)     | 1.0518 TOPS      |  2.5891 TOPS      |                   |                   |
| AVX512_BF16     | 128b          | DP2A(f32,bf16,bf16)   | 1.0305 TFLOPS    |  2.5338 TFLOPS    |                   |                   |
| FMA             | 128b          | FMA(f32,f32,f32)      | 512.41 GFLOPS    |  1.2741 TFLOPS    |  1.8209 TFLOPS    |  7.9004 TFLOPS    |
| FMA             | 128b          | FMA(f64,f64,f64)      | 264.48 GFLOPS    |  644.75 GFLOPS    |  911.58 GFLOPS    |  3.9481 TFLOPS    |
| SSE             | 128b          | ADD(MUL(f32,f32),f32) | 487.75 GFLOPS    |  1.2 TFLOPS       |  982.29 GFLOPS    |  3.9499 TFLOPS    |
| SSE2            | 128b          | ADD(MUL(f64,f64),f64) | 246.46 GFLOPS    |  597.1 GFLOPS     |  491.18 GFLOPS    |  1.9767 TFLOPS    |
------------------------------------------------------------------------------ ------------------- ------------------- -------------------
