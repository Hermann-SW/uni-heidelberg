#include <stdio.h>
#include <stdlib.h>
#include <CL/opencl.h>

int main() {
    cl_int err;
    cl_platform_id platform;
    clGetPlatformIDs(1, &platform, NULL);
    cl_device_id device;
    clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, NULL);

    cl_context context = clCreateContext(NULL, 1, &device, NULL, NULL, &err);
    cl_queue_properties props[] = { CL_QUEUE_PROPERTIES, CL_QUEUE_PROFILING_ENABLE, 0 };
    cl_command_queue queue = clCreateCommandQueueWithProperties(context, device, props, &err);

const char* source = R"(
#pragma OPENCL EXTENSION cl_khr_fp64 : enable
__attribute__((amdgpu_flat_work_group_size(64, 64)))
__kernel void max_tflops_burn(__global double* seeds, __global double* out) {
    double b = seeds[0]; 
    double c = seeds[1];

    // 16 accumulators to ensure we fully saturate the 4-cycle latency
    double a0=1.0, a1=1.1, a2=1.2, a3=1.3, a4=1.4, a5=1.5, a6=1.6, a7=1.7;
    double a8=1.8, a9=1.9, a10=2.0, a11=2.1, a12=2.2, a13=2.3, a14=2.4, a15=2.5;

    // 1 Billion Iterations
    for (long i = 0; i < 1000000000L; i++) {
        // Cross-dependency: a0 affects b, and a8 affects c.
        // This makes it mathematically impossible to skip steps.
        b += (a0 * 1e-18);
        c += (a8 * 1e-18);

        a0=fma(a0,b,c); a1=fma(a1,b,c); a2=fma(a2,b,c); a3=fma(a3,b,c);
        a4=fma(a4,b,c); a5=fma(a5,b,c); a6=fma(a6,b,c); a7=fma(a7,b,c);
        a8=fma(a8,b,c); a9=fma(a9,b,c); a10=fma(a10,b,c); a11=fma(a11,b,c);
        a12=fma(a12,b,c); a13=fma(a13,b,c); a14=fma(a14,b,c); a15=fma(a15,b,c);
    }

    out[get_global_id(0)] = a0 + a8 + a15;
}
)";
    cl_program program = clCreateProgramWithSource(context, 1, &source, NULL, &err);

// Remove -cl-fast-relaxed-math
clBuildProgram(program, 1, &device, "-cl-std=CL2.0", NULL, NULL);
    
    // 1. FIXED: Match the kernel name in the source string
    cl_kernel kernel = clCreateKernel(program, "max_tflops_burn", &err);

// 1. Create the seeds buffer with some random data
double h_seeds[16];
for(int i=0; i<16; i++) h_seeds[i] = 1.0 + (i * 0.01);
cl_mem d_seeds = clCreateBuffer(context, CL_MEM_READ_ONLY | CL_MEM_COPY_HOST_PTR, 16 * sizeof(double), h_seeds, &err);

// 60 CUs on a Radeon Pro VII. 
// We want at least one wavefront (64 threads) per CU to keep it busy.
size_t global_size = 64 * 60 * 4; // 4 wavefronts per CU
size_t local_size = 64;
// 2. Create the output buffer
cl_mem d_out = clCreateBuffer(context, CL_MEM_WRITE_ONLY, global_size * sizeof(double), NULL, &err);

// 3. Set the arguments in the correct order
clSetKernelArg(kernel, 0, sizeof(cl_mem), &d_seeds); // __global double* seeds
clSetKernelArg(kernel, 1, sizeof(cl_mem), &d_out);   // __global double* out

    // 2. FIXED: Removed all clSetKernelArg calls because max_tflops_burn takes no arguments

cl_event event;
cl_int run_err = clEnqueueNDRangeKernel(queue, kernel, 1, NULL, &global_size, &local_size, 0, NULL, &event);
    if (run_err != CL_SUCCESS) {
        printf("Kernel Launch Failed with Error: %d\n", run_err);
        return 1;
    }
    clWaitForEvents(1, &event);

    cl_ulong start, end;
    clGetEventProfilingInfo(event, CL_PROFILING_COMMAND_START, sizeof(start), &start, NULL);
    clGetEventProfilingInfo(event, CL_PROFILING_COMMAND_END, sizeof(end), &end, NULL);
    
    // 3. FIXED: Proper calculation for this specific synthetic loop
// 18 Ops * 2 (FLOPs/Op) * 1,000,000,000 Iterations * 3840 threads
double total_flops = 18.0 * 2.0 * 1000000000.0 * (64.0 * 60.0);
double seconds = (double)(end - start) * 1.0e-9;
double tflops = (total_flops / seconds) / 1e12;

printf("MI50 Steady-State Peak: %.2f TFLOPS\n", tflops);
printf("Execution time: %.2f seconds\n", seconds);

    clReleaseKernel(kernel); clReleaseProgram(program);
    clReleaseCommandQueue(queue); clReleaseContext(context);
    return 0;
}
