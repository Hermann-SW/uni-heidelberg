[Studying in my 60s](https://github.com/Hermann-SW/Hermann-SW.github.io/tree/master/studying_in_my_60s#studying-in-my-60s) at Heidelberg/Germany University:

- [future lectures](https://stamm-wilbrandt.de/GraphvizFiddle/#_math) currently planned to attend
- [spring 2026](#spring-2026)
- [fall 2025](#fall-2025)

# spring 2026
(6 lectures)

## Linear Algebra 2

Script, recordings and excercises:  
https://scoop.iwr.uni-heidelberg.de/teaching/2026ss/lecture-lineare-algebra/

## Analysis 2

Script and excercises behind VPN on mampf.mathi.uni-heidelberg.de

## Hardware-Aware Scientific Computing

Script behind VPN on moodle.uni-heidelberg.de, but repo accessible:  
https://parcomp-git.iwr.uni-heidelberg.de/Teaching/hasc-code

benchmarking: find nice pointer_chasing diagrams for 6 different CPU with between 4 and 24 cores [here](pointer_chasing.md) 

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

stream.cc was compiled with option -ffreestanding avoiding use of memcpy() for copy operation test. 

From https://blogs.fau.de/hager/archives/8263;  
... , and the output of the benchmark must be corrected by a factor of 1.5 (Scale) or 1.33 (Triad). This line of thinking is what John McCalpin calls “hardware byte counting” [3], and for me it is the only valid option. I want to know how many bytes the memory interface can transfer per second, and if that means I have to account for write-allocates, so be it. ...


So for current measurements that means: since 366×1.5=549 and 422×1.33=561, the true memory bandwidth for Scale and Triad was 549 GByte/s and 561 GByte/s, respectively.

The measurements were done with 8×16GB RAM modules attached to each of the 8 CPUs (64 RAM modules in total) with symmetric 1TB RAM in total. Before the system had 66 RAM modules to allow for a consecutive array of size 1TB; that was a bad idea because the stream measurement for Triad was only 101837.9, less than 25%(!) of current memory bandwidth with 64 RAM modules.

## Randomized Algorithms

Script behind VPN on moodle.uni-heidelberg.de  

## Elementary number theory

Fall 2024 script, recordings and excercises behind VPN on mampf.mathi.uni-heidelberg.de

## Berkeley math 115: Introduction to number theory

- Youtube lecture series [spring 2022](https://www.youtube.com/watch?v=EzE6it9kAsI&list=PL8yHsr3EFj53L8sMbzIhhXSAOpuZ1Fov8&index=1)

- 53 lecture [summaries](markdown/Math155.md)


# fall 2025
(2 lectures)

## Lineare Algebra 1
- [Algebraische Strukturen Diagramm](https://stamm-wilbrandt.de/GraphvizFiddle/2.1.2/#_LA1): Mengen, Halbgruppen, ..., Körper  
-
- [Automatischer Beweis für Lineare Algebra 1 Hausaufgabe 5.2b](markdown/Lineare_Algebra_1.Aufgabe_5.2b.md)
- [Plenarübung 5 Diskussion, automatisch alle Gruppen mit 6 Elementen](markdown/Lineare_Algebra_1.Plenaruebung_Diskussion.md)
- automatisch [alle Gruppen mit 8 Elementen](markdown/Lineare_Algebra_1.G8.md) bestimmen (sehr rechenintensiv)
- 75 Zeilen Skript erzeugt LaTex für 2 Seiten Abgabe von Aufgabe 10.3c.i zur [Rangfaktorisierung](markdown/Lineare_Algebra_1.Rangfaktorisierung.md) 


## Analysis 1
- [Lemmata, Sätze, Definitionen, ... der Vorlesungen 1-8 von Analysis 1, WS25/26](markdown/Analysis_1.WS25_26.md)  
(der rein handschriftlichen Vorlesungen, beginnend mit Vorlesung 9 nicht mehr nötig)
-
- [Automatischer Beweis für Analysis 1 Hausaufgabe 3.3](markdown/Analysis_1.Aufgabe_3.3.md)

