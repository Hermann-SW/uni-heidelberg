/*
  GPU parallelization of wave/wave_vanilla.cc (with numerous Gemini iterations):
  https://parcomp-git.iwr.uni-heidelberg.de/Teaching/hasc-code

  Simple demo:
  ./wave_cell 514 2000 -100
  Positive last arg for writing "output*.vtk" files for ParaView viewing.

  Build:
  export f=wave_cell
  export CCFLAGSBASE="-O3 -std=c++17"

  # Instinct MI50, Radeon Pro VII, Radeon VII;  RX Vega64, RX Vega56
  hipcc $CCFLAGSBASE --offload-arch=gfx906 --offload-arch=gfx900 $f.cc -o $f

  # Tesla P100 (cuda toolkit 12.9)
  hipcc $CCFLAGSBASE -arch=sm_60 $f.cc -o $f
  # NVIDIA RTX5060
  /usr/local/cuda-12.8/bin/nvcc $CCFLAGSBASE -arch=sm_120 -x cu $f.cc -o $f
  # NVIDIO GTX1660 TI (cuda toolkit 11.8)
  nvcc $CCFLAGSBASE -arch=sm_75 -x cu $f.cc -o $f
  # Tesla K80
  /usr/local/cuda-11.8/bin/nvcc $CCFLAGSBASE -arch=sm_37 -x cu $f.cc -o $f
*/
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include <chrono>
#include <atomic>
#include <cstdlib>
#include <cstdio>


// #include "time_experiment.hh"
#include <chrono>
#include <utility>
//! a function getting current value of high resolution clock
auto get_time_stamp() { return std::chrono::high_resolution_clock::now(); }
// forward declarations for functions at file end
template <typename T> double get_duration_seconds(T start, T stop);
template <typename T> auto time_experiment(const T &experiment, double mintime = 0.5);

// #include "output.hh"
void write_file(int n, std::string basename, int step, double *u, int ofs = 0)
{
  // 1. Define dimensions for the points
  const int NX = n + 1;
  const int NY = n + 1;
  const int NZ = 1; // 2D grids must have 1 point in Z
  const int numPoints = NX * NY * NZ;

  // Calculate total cells: (NX-1) * (NY-1) * 1
  const int numCells = n * n;

  // 2. Open the file stream
  char name[256];
  sprintf(name, "%s_%06d.vtk", basename.c_str(), step);
  std::ofstream vtkFile(name);
  if (!vtkFile.is_open())
  {
    std::cerr << "Error opening file!" << std::endl;
    return;
  }

  // 3. Write the VTK Header
  vtkFile << "# vtk DataFile Version 3.0" << std::endl;
  vtkFile << "2D Structured Mesh with Cell Values" << std::endl;
  vtkFile << "ASCII" << std::endl;
  vtkFile << "DATASET STRUCTURED_GRID" << std::endl;
  vtkFile << "DIMENSIONS " << NX << " " << NY << " " << NZ << std::endl;

  // 4. Write point coordinates (Grid remains the same size)
  vtkFile << "POINTS " << numPoints << " float" << std::endl;
  for (int j = 0; j < NY; ++j)
  {
    for (int i = 0; i < NX; ++i)
    {
      float x = static_cast<float>(i);
      float y = static_cast<float>(j);
      float z = 0.0f;
      vtkFile << x << " " << y << " " << z << std::endl;
    }
  }

  // 5. Write CELL DATA instead of point data
  vtkFile << "CELL_DATA " << numCells << std::endl; // Must match cell count (4)
  vtkFile << "SCALARS u_values float 1" << std::endl;
  vtkFile << "LOOKUP_TABLE default" << std::endl;

  // 6. Write values for each cell block
  // Loop limits are reduced to (NX - 1) and (NY - 1)
  for (int j = 0; j < n; ++j)
  {
    for (int i = 0; i < n; ++i)
    {
      // Example custom value: unique ID or physical value for each cell face
      float val;
      if (std::abs(u[j * (n + 2 * ofs) + i]) < 1e-15)
        val = 0.0;
      else
        val = static_cast<float>(u[j * (n + 2 * ofs) + i]);
      vtkFile << val << std::endl;
    }
  }

  vtkFile.close();
}


// Cross-platform CUDA / ROCm Cooperative Groups & Runtime Bridge
#if defined(__CUDACC__) || defined(__NVCC__)
  #include <cuda_runtime.h>
  #include <cooperative_groups.h>

  #define hipSuccess cudaSuccess
  #define hipError_t cudaError_t
  #define hipGetErrorString cudaGetErrorString
  #define hipStream_t cudaStream_t
  #define hipStreamCreateWithFlags cudaStreamCreateWithFlags
  #define hipStreamNonBlocking cudaStreamNonBlocking
  #define hipStreamSynchronize cudaStreamSynchronize
  #define hipStreamDestroy cudaStreamDestroy
  #define hipHostMalloc(ptr, sz, flags) cudaMallocHost(ptr, sz)
  #define hipHostFree cudaFreeHost
  #define hipMalloc cudaMalloc
  #define hipFree cudaFree
  #define hipMemcpy cudaMemcpy
  #define hipMemcpyHostToDevice cudaMemcpyHostToDevice
  #define hipMemcpyDeviceToHost cudaMemcpyDeviceToHost
  #define hipDeviceGetAttribute cudaDeviceGetAttribute
  #define hipDeviceAttributeCooperativeLaunch cudaDevAttrCooperativeLaunch
  #define hipGetDeviceProperties cudaGetDeviceProperties
  #define hipDeviceProp_t cudaDeviceProp
  #define hipOccupancyMaxActiveBlocksPerMultiprocessor cudaOccupancyMaxActiveBlocksPerMultiprocessor
  #define hipLaunchCooperativeKernel cudaLaunchCooperativeKernel
  #define hipHostMallocCoherent 0
  #define hipHostMallocMapped 0
  #define hipHostMallocDefault 0

  namespace cg = cooperative_groups;
#else
  #include <hip/hip_runtime.h>
  #include <hip/hip_cooperative_groups.h>

  namespace cg = cooperative_groups;
#endif

#if defined(__x86_64__) || defined(_M_X64)
  #include <immintrin.h>
  #include <cpuid.h>

// Executed automatically BEFORE main() and BEFORE ROCm driver initialization
__attribute__((constructor)) static void apply_sdma_workaround_early() {
    unsigned int eax, ebx, ecx, edx;
    char vendor[13];

    __cpuid(0, eax, ebx, ecx, edx);
    *reinterpret_cast<int*>(vendor) = ebx;
    *reinterpret_cast<int*>(vendor + 4) = edx;
    *reinterpret_cast<int*>(vendor + 8) = ecx;
    vendor[12] = '\0';

    bool is_legacy = false;

    if (__get_cpuid(1, &eax, &ebx, &ecx, &edx)) {
        int family = ((eax >> 8) & 0xF) + ((eax >> 20) & 0xFF);
        int model = ((eax >> 4) & 0xF) | ((eax >> 12) & 0xF0);

        std::string vendor_str(vendor);

        // Intel Pre-Ice Lake (Family 6, Skylake/Kaby Lake/Coffee Lake <= 0x9E)
        if (vendor_str == "GenuineIntel" && family == 6 && model <= 0x9E) {
            is_legacy = true;
        }
        // AMD Pre-Zen 3 (Family < 0x19)
        else if (vendor_str == "AuthenticAMD" && family < 0x19) {
            is_legacy = true;
        }
    }

    if (is_legacy) {
        setenv("HSA_ENABLE_SDMA", "0", 1);
        std::fprintf(stderr, "[HIP] Early Init: Legacy CPU detected (%s). Set HSA_ENABLE_SDMA=0.\n", vendor);
    }
}
#endif




#define HIP_CHECK(command) \
    do { \
        hipError_t status = command; \
        if (status != hipSuccess) { \
            std::cerr << "HIP Error: " << hipGetErrorString(status) \
                      << " at line " << __LINE__ << std::endl; \
            exit(status); \
        } \
    } while (0)

enum Command {
    CMD_NONE = 0,
    CMD_START,
    CMD_SET_IC,
    CMD_COMPUTE,
    CMD_READ,
    CMD_QUIT
};

struct ControlBlock {
    int cmd;
    int done;
    int steps_to_run;
    int n;
    double dt;
};

// --- Helper Functions ---

__device__ inline void pick_out(double *q, const double *u, const double *w0, const double *w1, int index) {
    q[0] = u[index];
    q[1] = w0[index];
    q[2] = w1[index];
}

__device__ inline void write_back(const double *q, double *u, double *w0, double *w1, int index) {
    u[index] = q[0];
    w0[index] = q[1];
    w1[index] = q[2];
}

__device__ inline void flip_0(double *qout, const double *qin) {
    qout[0] = qin[0];
    qout[1] = -qin[1];
    qout[2] = qin[2];
}

__device__ inline void flip_1(double *qout, const double *qin) {
    qout[0] = qin[0];
    qout[1] = qin[1];
    qout[2] = -qin[2];
}

__device__ inline void cell_update(double factor, double *qnew, const double *qcenter, 
                                   const double *qleft, const double *qright, 
                                   const double *qbottom, const double *qtop) {
    qnew[0] = 0.0;
    qnew[1] = 0.0;
    qnew[2] = 0.0;

    double l[2] = { qleft[0] - qcenter[0], qleft[1] - qcenter[1] };
    qnew[0] += 0.5 * l[0] + 0.5 * l[1];
    qnew[1] += 0.5 * l[0] + 0.5 * l[1];

    double r[2] = { qright[0] - qcenter[0], qright[1] - qcenter[1] };
    qnew[0] -= -0.5 * r[0] + 0.5 * r[1];
    qnew[1] -=  0.5 * r[0] - 0.5 * r[1];

    double b[3] = { qbottom[0] - qcenter[0], 0.0, qbottom[2] - qcenter[2] };
    qnew[0] += 0.5 * b[0] + 0.5 * b[2];
    qnew[2] += 0.5 * b[0] + 0.5 * b[2];

    double t[3] = { qtop[0] - qcenter[0], 0.0, qtop[2] - qcenter[2] };
    qnew[0] -= -0.5 * t[0] + 0.5 * t[2];
    qnew[2] -=  0.5 * t[0] - 0.5 * t[2];

    qnew[0] = qnew[0] * factor + qcenter[0];
    qnew[1] = qnew[1] * factor + qcenter[1];
    qnew[2] = qnew[2] * factor + qcenter[2];
}

__device__ void compute_cell(int i, int j, int n, double factor,
                             const double *uold, const double *w0old, const double *w1old,
                             double *unew, double *w0new, double *w1new) {
    int index = j * n + i;
    double qcenter[3], qleft[3], qright[3], qbottom[3], qtop[3], qnew[3];

    pick_out(qcenter, uold, w0old, w1old, index);

    if (i > 0)     pick_out(qleft, uold, w0old, w1old, index - 1);
    else           flip_0(qleft, qcenter);

    if (i < n - 1) pick_out(qright, uold, w0old, w1old, index + 1);
    else           flip_0(qright, qcenter);

    if (j > 0)     pick_out(qbottom, uold, w0old, w1old, index - n);
    else           flip_1(qbottom, qcenter);

    if (j < n - 1) pick_out(qtop, uold, w0old, w1old, index + n);
    else           flip_1(qtop, qcenter);

    cell_update(factor, qnew, qcenter, qleft, qright, qbottom, qtop);
    write_back(qnew, unew, w0new, w1new, index);
}

// --- Legacy Single-Step Kernel (For pre-sm_60 GPUs without Cooperative Launch) ---

__global__ void wave_step_kernel(int n, double factor,
                                const double *uold, const double *w0old, const double *w1old,
                                double *unew, double *w0new, double *w1new) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n * n) {
        int j = idx / n;
        int i = idx % n;
        compute_cell(i, j, n, factor, uold, w0old, w1old, unew, w0new, w1new);
    }
}

// --- Persistent Kernel ---

__global__ void persistent_wave_kernel(ControlBlock *ctrl, 
                                       double *d_u0, double *d_w0_0, double *d_w1_0,
                                       double *d_u1, double *d_w0_1, double *d_w1_1,
                                       double *d_read_out) {
    cg::grid_group grid = cg::this_grid();
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    int total_threads = gridDim.x * blockDim.x;

    double *p_uold  = d_u0;   double *p_w0old = d_w0_0; double *p_w1old = d_w1_0;
    double *p_unew  = d_u1;   double *p_w0new = d_w0_1; double *p_w1new = d_w1_1;

    volatile int *cmd_ptr  = (volatile int *)&ctrl->cmd;
    volatile int *done_ptr = (volatile int *)&ctrl->done;

    while (true) {
        int command = CMD_NONE;
        if (tid == 0) {
            while ((command = *cmd_ptr) == CMD_NONE) {
                #if defined(__HIP_PLATFORM_AMD__)
                __builtin_amdgcn_s_sleep(10);
                #endif
            }
        }

        grid.sync();
        if (tid != 0) {
            command = *cmd_ptr;
        }

        if (command == CMD_QUIT) {
            break;
        } 
        else if (command == CMD_SET_IC) {
            p_uold  = d_u0;   p_w0old = d_w0_0; p_w1old = d_w1_0;
            p_unew  = d_u1;   p_w0new = d_w0_1; p_w1new = d_w1_1;

            grid.sync();
            if (tid == 0) {
                *cmd_ptr = CMD_NONE;
                __threadfence_system();
                *done_ptr = 1;
                __threadfence_system();
            }
            grid.sync();
        } 
        else if (command == CMD_COMPUTE) {
            int steps = ctrl->steps_to_run;
            int n = ctrl->n;
            double factor = ctrl->dt * n;

            for (int s = 0; s < steps; s++) {
                for (int idx = tid; idx < n * n; idx += total_threads) {
                    int j = idx / n;
                    int i = idx % n;
                    compute_cell(i, j, n, factor, p_uold, p_w0old, p_w1old, p_unew, p_w0new, p_w1new);
                }
                grid.sync();

                double *tmp;
                tmp = p_uold; p_uold = p_unew; p_unew = tmp;
                tmp = p_w0old; p_w0old = p_w0new; p_w0new = tmp;
                tmp = p_w1old; p_w1old = p_w1new; p_w1new = tmp;
                grid.sync();
            }

            if (tid == 0) {
                *cmd_ptr = CMD_NONE;
                __threadfence_system();
                *done_ptr = 1;
                __threadfence_system();
            }
            grid.sync();
        } 
        else if (command == CMD_READ) {
            int n = ctrl->n;
            for (int idx = tid; idx < n * n; idx += total_threads) {
                d_read_out[idx] = p_uold[idx];
            }
            grid.sync();

            if (tid == 0) {
                __threadfence();
                *cmd_ptr = CMD_NONE;
                __threadfence_system();
                *done_ptr = 1;
                __threadfence_system();
            }
            grid.sync();
        }
    }
}

void set_initial_condition(int n, double *u, double *w0, double *w1) {
    for (int k = 0; k < n * n; k++) {
        u[k] = 0.0;
        w0[k] = 0.0;
        w1[k] = 0.0;
    }
    for (int j = n / 5; j < 2 * n / 5; j++)
        for (int i = n / 3; i < 2 * n / 5; i++)
            u[j * n + i] = 1.0;
}

inline void send_command(ControlBlock *ctrl, int cmd) {
    __atomic_store_n(&ctrl->done, 0, __ATOMIC_SEQ_CST);
    __atomic_store_n(&ctrl->cmd, cmd, __ATOMIC_SEQ_CST);
    
    while (__atomic_load_n(&ctrl->done, __ATOMIC_SEQ_CST) == 0) {
        #if defined(__x86_64__) || defined(_M_X64)
        _mm_pause();
        #endif
    }
}

int main(int argc, char **argv) {
    setenv("HIP_HOST_COHERENT", "1", 1);

    int n, steps, every;
    double Cr = 0.5;

    if (argc == 4) {
        sscanf(argv[1], "%d", &n);
        sscanf(argv[2], "%d", &steps);
        sscanf(argv[3], "%d", &every);
        if (every == 0) {
            std::cout << "<every> is not allowed to be zero" << std::endl;
            return 0;
        }
    } else {
        std::cout << "usage: wave <cells per direction> <number of time steps> <every>" << std::endl;
        return 0;
    }

    bool write_files = true;
    if (every < 0) {
        write_files = false;
        every = -every;
    }

    double dt = Cr / n;
    size_t data_size = n * n * sizeof(double);

    hipStream_t kernel_stream;
    HIP_CHECK(hipStreamCreateWithFlags(&kernel_stream, hipStreamNonBlocking));

    double *h_u, *h_w0, *h_w1;
    HIP_CHECK(hipHostMalloc(&h_u, data_size, hipHostMallocDefault));
    HIP_CHECK(hipHostMalloc(&h_w0, data_size, hipHostMallocDefault));
    HIP_CHECK(hipHostMalloc(&h_w1, data_size, hipHostMallocDefault));

    double *d_u0, *d_w0_0, *d_w1_0;
    double *d_u1, *d_w0_1, *d_w1_1;
    double *d_read_out;

    HIP_CHECK(hipMalloc(&d_u0, data_size));
    HIP_CHECK(hipMalloc(&d_w0_0, data_size));
    HIP_CHECK(hipMalloc(&d_w1_0, data_size));
    HIP_CHECK(hipMalloc(&d_u1, data_size));
    HIP_CHECK(hipMalloc(&d_w0_1, data_size));
    HIP_CHECK(hipMalloc(&d_w1_1, data_size));
    HIP_CHECK(hipMalloc(&d_read_out, data_size));

    set_initial_condition(n, h_u, h_w0, h_w1);

    HIP_CHECK(hipMemcpy(d_u0, h_u, data_size, hipMemcpyHostToDevice));
    HIP_CHECK(hipMemcpy(d_w0_0, h_w0, data_size, hipMemcpyHostToDevice));
    HIP_CHECK(hipMemcpy(d_w1_0, h_w1, data_size, hipMemcpyHostToDevice));

    // Check Cooperative Group support on active device
    int supportsCooperative = 0;
    HIP_CHECK(hipDeviceGetAttribute(&supportsCooperative, hipDeviceAttributeCooperativeLaunch, 0));

    auto start = get_time_stamp();
    double performance_sum = 0.0;

    if (!supportsCooperative) {
        std::cout << "[INFO] GPU lacks Cooperative Launch support. Falling back to iterative single-step kernel launches.\n";

        int blockSize = 256;
        int blocksPerGrid = (n * n + blockSize - 1) / blockSize;

        double *p_uold = d_u0, *p_w0old = d_w0_0, *p_w1old = d_w1_0;
        double *p_unew = d_u1, *p_w0new = d_w0_1, *p_w1new = d_w1_1;
        double factor = dt * n;

        if (write_files) write_file(n, "output", 0, h_u);

        for (int step = every; step <= steps; step += every) {
            for (int s = 0; s < every; s++) {
                wave_step_kernel<<<blocksPerGrid, blockSize, 0, kernel_stream>>>(
                    n, factor, p_uold, p_w0old, p_w1old, p_unew, p_w0new, p_w1new
                );

                std::swap(p_uold, p_unew);
                std::swap(p_w0old, p_w0new);
                std::swap(p_w1old, p_w1new);
            }

            HIP_CHECK(hipStreamSynchronize(kernel_stream));

            auto stop = get_time_stamp();
            double elapsed = get_duration_seconds(start, stop);
            double updates = 1.0 * every * n * n;
            double performance = updates / elapsed / 1e9;
            performance_sum += performance;
            double performance_average = performance_sum / (step / every);

            std::cout << "updates=" << updates << " elapsed=" << elapsed 
                      << " performance=" << performance_average << " giga updates per second" << std::endl;

            if (write_files) {
                HIP_CHECK(hipMemcpy(h_u, p_uold, data_size, hipMemcpyDeviceToHost));
                write_file(n, "output", step / every, h_u);
            }

            start = get_time_stamp();
        }

    } else {
        // Persistent Kernel Path (Cooperative Launch supported)
        ControlBlock *h_ctrl;
        HIP_CHECK(hipHostMalloc(&h_ctrl, sizeof(ControlBlock), hipHostMallocCoherent | hipHostMallocMapped));
        h_ctrl->cmd = CMD_NONE;
        h_ctrl->done = 0;
        h_ctrl->n = n;
        h_ctrl->dt = dt;

        int blockSize = 256;
        int maxBlocksPerSM = 0;
        HIP_CHECK(hipOccupancyMaxActiveBlocksPerMultiprocessor(
            &maxBlocksPerSM, persistent_wave_kernel, blockSize, 0));

        hipDeviceProp_t deviceProp;
        HIP_CHECK(hipGetDeviceProperties(&deviceProp, 0));
        int numBlocks = maxBlocksPerSM * (deviceProp.multiProcessorCount - 1);

        void *args[] = { &h_ctrl, &d_u0, &d_w0_0, &d_w1_0, &d_u1, &d_w0_1, &d_w1_1, &d_read_out };

        HIP_CHECK(hipLaunchCooperativeKernel((void*)persistent_wave_kernel, dim3(numBlocks), dim3(blockSize), args, 0, kernel_stream));

        send_command(h_ctrl, CMD_SET_IC);

        if (write_files) write_file(n, "output", 0, h_u);

        for (int step = every; step <= steps; step += every) {
            h_ctrl->steps_to_run = every;
            send_command(h_ctrl, CMD_COMPUTE);

            auto stop = get_time_stamp();
            double elapsed = get_duration_seconds(start, stop);
            double updates = 1.0 * every * n * n;
            double performance = updates / elapsed / 1e9;
            performance_sum += performance;
            double performance_average = performance_sum / (step / every);

            std::cout << "updates=" << updates << " elapsed=" << elapsed 
                      << " performance=" << performance_average << " giga updates per second" << std::endl;

            if (write_files) {
                send_command(h_ctrl, CMD_READ);
                HIP_CHECK(hipMemcpy(h_u, d_read_out, data_size, hipMemcpyDeviceToHost));
                write_file(n, "output", step / every, h_u);
            }

            start = get_time_stamp();
        }

        __atomic_store_n(&h_ctrl->cmd, CMD_QUIT, __ATOMIC_SEQ_CST);
        HIP_CHECK(hipStreamSynchronize(kernel_stream));
        HIP_CHECK(hipHostFree(h_ctrl));
    }

    HIP_CHECK(hipStreamDestroy(kernel_stream));

    HIP_CHECK(hipFree(d_u0));     HIP_CHECK(hipFree(d_w0_0)); HIP_CHECK(hipFree(d_w1_0));
    HIP_CHECK(hipFree(d_u1));     HIP_CHECK(hipFree(d_w0_1)); HIP_CHECK(hipFree(d_w1_1));
    HIP_CHECK(hipFree(d_read_out));

    HIP_CHECK(hipHostFree(h_u));
    HIP_CHECK(hipHostFree(h_w0));
    HIP_CHECK(hipHostFree(h_w1));

    return 0;
}


// compute difference of two time stamps in seconds
// the data type T is that returned by get_time_stamp
template <typename T>
double get_duration_seconds(T start, T stop)
{
  auto duration = stop - start;
  auto dcast = std::chrono::duration_cast<std::chrono::microseconds>(duration).count();
  return dcast / 1e6;
}

/*! \brief time an experiment
 * This function template takes an experiment, which is a class with a method
 * void run () {} and measures the time that it takes to execute that function.
 * To make timings accurate it repeats the experiment by running run() several
 * times such that the total execution time takes at least a given time. This is
 * the second, optional parameter.
 * The result of the function is a std::pair where the first component is an integer
 * holding the number of repetitions of the experiment and the second component is the
 * total execution time for these repetitions in microseconds.
 *
 * \param experiment an experiment with a run method
 * \param mintime minimum total runtime (given in microseconds)
 *
 */
template <typename T>
auto time_experiment(const T &experiment, double mintime)
{
  auto start = get_time_stamp();
  auto stop = start;
  auto duration = get_duration_seconds(start,stop);
  std::pair<long, double> rv;
  long rep = 1;
  while (duration < mintime && rep < 1000000000)
  {
    start = get_time_stamp();
    for (long k = 0; k < rep; k++)
      experiment();
    stop = get_time_stamp();
    duration = get_duration_seconds(start,stop);
    // std::cout << " rep=" << rep << " d=" << dcast << std::endl;
    rv.first = rep;
    rv.second = duration;
    rep *= 2;
  }
  return rv;
}
