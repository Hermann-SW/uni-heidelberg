[STREAM](https://parcomp-git.iwr.uni-heidelberg.de/Teaching/hasc-code/-/tree/master/stream?ref_type=heads) is the de facto industry standard benchmark for measuring sustained memory bandwidth. Here executed on 8× 24C/48T Intel Xeon E7 8890v4 CPUs in Lenovo x3950-X6 8-socket server:  
```
hermann@x3950-X6:~/hasc-code/stream$ echo off | sudo tee /sys/devices/system/cpu/smt/control
[sudo] password for hermann: 
off
hermann@x3950-X6:~/hasc-code/stream$ nproc
192
hermann@x3950-X6:~/hasc-code/stream$ ./stream 
...
Array size = 100000000 (elements), Offset = 0 (elements)
Memory per array = 762.9 MiB (= 0.7 GiB).
Total memory required = 2288.8 MiB (= 2.2 GiB).
Each kernel will be executed 500 times.
...
Number of Threads requested = 192
Number of Threads counted = 192
...
-------------------------------------------------------------
Function    Best Rate MB/s  Avg time     Min time     Max time
Copy:          386393.7     0.004873     0.004141     0.033827
Scale:         366134.9     0.004823     0.004370     0.030055
Add:           410535.5     0.006594     0.005846     0.026840
Triad:         422387.1     0.006789     0.005682     0.042516
-------------------------------------------------------------
Solution Validates: avg error less than 1.000000e-13 on all three arrays
-------------------------------------------------------------
hermann@x3950-X6:~/hasc-code/stream$
```

stream.c was compiled with option -ffreestanding avoiding use of memcpy() for copy operation test. 

From https://blogs.fau.de/hager/archives/8263:  
... , and the output of the benchmark must be corrected by a factor of 1.5 (Scale) or 1.33 (Triad). This line of thinking is what John McCalpin calls “hardware byte counting” [3], and for me it is the only valid option. I want to know how many bytes the memory interface can transfer per second, and if that means I have to account for write-allocates, so be it. ...


So for current measurements that means: since 366×1.5=549 and 422×1.33=561, the true memory bandwidth for Scale and Triad was 549 GByte/s and 561 GByte/s, respectively.

The measurements were done with 8×16GB RAM modules attached to each of the 8 CPUs (64 RAM modules in total) with symmetric 1TB RAM in total. Before the system had 66 RAM modules to allow for a consecutive array of size 1TB; that was a bad idea because the stream measurement for Triad was only 101837.9, less than 25%(!) of current memory bandwidth with 64 RAM modules.

