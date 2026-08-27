I did the GPU implementation with Gemini for these AMD GPUs ...  
- Instinct MI50, Radeon Pro VII, Radeon VII (all gfx906)
- RX Vega64, RX Vega56 (all gfx900)

... and these NVIDIA GPUs ...  
-  Tesla P100 (sm_60), RTX5060 (sm_120), GTX1660 TI (sm_75), Tesla K80 (sm_37)

using HIP. Top comment of [wave_cell.cc](../scripts/wave_cell.cc) has the build instrctions, here for AMD GPUs:  
```
  export f=wave_cell
  export CCFLAGSBASE="-O3 -std=c++17"

  # Instinct MI50, Radeon Pro VII, Radeon VII;  RX Vega64, RX Vega56
  hipcc $CCFLAGSBASE --offload-arch=gfx906 --offload-arch=gfx900 $f.cc -o $f
```

```
usage: wave <cells per direction> <number of time steps> <every>
```

For negative values for "every" no output files get written, and computation speed is maximal:  
```
hermann@Radeon-vii:~/uni-heidelberg/scripts$ ./wave_cell 514 2000 -100
[HIP] Early Init: Legacy CPU detected (GenuineIntel). Set HSA_ENABLE_SDMA=0.
updates=2.64196e+07 elapsed=0.00799 performance=3.30658 giga updates per second
updates=2.64196e+07 elapsed=0.002692 performance=6.56035 giga updates per second
updates=2.64196e+07 elapsed=0.002661 performance=7.68305 giga updates per second
updates=2.64196e+07 elapsed=0.002516 performance=8.38745 giga updates per second
updates=2.64196e+07 elapsed=0.002502 performance=8.82184 giga updates per second
updates=2.64196e+07 elapsed=0.002507 performance=9.10792 giga updates per second
updates=2.64196e+07 elapsed=0.002504 performance=9.31407 giga updates per second
updates=2.64196e+07 elapsed=0.00251 performance=9.46553 giga updates per second
updates=2.64196e+07 elapsed=0.002509 performance=9.58379 giga updates per second
updates=2.64196e+07 elapsed=0.002511 performance=9.67757 giga updates per second
updates=2.64196e+07 elapsed=0.002504 performance=9.75697 giga updates per second
updates=2.64196e+07 elapsed=0.002508 performance=9.82173 giga updates per second
updates=2.64196e+07 elapsed=0.002502 performance=9.87847 giga updates per second
updates=2.64196e+07 elapsed=0.002504 performance=9.92651 giga updates per second
updates=2.64196e+07 elapsed=0.00251 performance=9.96646 giga updates per second
updates=2.64196e+07 elapsed=0.002508 performance=10.0019 giga updates per second
updates=2.64196e+07 elapsed=0.002505 performance=10.034 giga updates per second
updates=2.64196e+07 elapsed=0.002512 performance=10.0608 giga updates per second
updates=2.64196e+07 elapsed=0.002508 performance=10.0857 giga updates per second
updates=2.64196e+07 elapsed=0.002503 performance=10.1092 giga updates per second
hermann@Radeon-vii:~/uni-heidelberg/scripts$ 
```

For positive values of "every" output files for inspection with [ParaView](https://www.paraview.org/) get written as well:  
```
./wave_cell 514 2000 100
```
```
hermann@Radeon-vii:~/uni-heidelberg/scripts$ ls output_0000*
output_000000.vtk  output_000006.vtk  output_000012.vtk  output_000018.vtk
output_000001.vtk  output_000007.vtk  output_000013.vtk  output_000019.vtk
output_000002.vtk  output_000008.vtk  output_000014.vtk  output_000020.vtk
output_000003.vtk  output_000009.vtk  output_000015.vtk
output_000004.vtk  output_000010.vtk  output_000016.vtk
output_000005.vtk  output_000011.vtk  output_000017.vtk
hermann@Radeon-vii:~/uni-heidelberg/scripts$ 
```


Small demonstration of load data, display and play animation with ParaView here:  
[../res/paraview.recording.mp4](../res/paraview.recording.mp4)  

After problems fixed for legacy CPUs, ParaView animation of generated output*.vtk data:  
![../res/acoustic_wave_equation.anim.gif](../res/acoustic_wave_equation.anim.gif)


