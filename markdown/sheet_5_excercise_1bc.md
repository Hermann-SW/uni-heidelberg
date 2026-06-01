This file:
https://github.com/Hermann-SW/uni-heidelberg/blob/main/markdown/sheet_5_excercise_1bc.md

# Exercise 1 (Tree Barrier)
...
## b)
Add a third member function `wait3` to the `Barrier` class that implements a combining tree
barrier. You may base your implementation on either of the existing variants:  
• the condition-variable version `wait` (one mutex/CV pair per inner tree node), or  
• the mutex-free version `wait2` (a pair of atomic counters per inner tree node; remember that the two-counter argument from part a) then applies at every node).  
...   
You may restrict yourself to the case of a binary tree, so that the number of leaves equals the number
of threads (i.e. a power of two).  
...

### solution

New `wait3` is implemented in this diff:  
https://github.com/Hermann-SW/uni-heidelberg/blob/main/scripts/Barrier.hh.diff_5.1b.diff

- based on `wait2`
- uses binary tree
- only works for #threads being power of 2
- that is enforced by new test code [barrier_test.cc](../scripts/barrier_test.cc)

`std::atomic<int> acounter, bcounter` is used by `wait2`.  
`std::vector<std::atomic<int>> actr, bctr` is used by `wait3`.  
The vectors are initialized with size `#threads`, for inner nodes of binary tree (1..P-1) with P:=#threads.
Entry 0 is not used. Leaves are represented by P..2*P-1, or P+threadnum and don't need counters.

`wait2` did increment/decrement counters from 0 up to P and from P downto 0.  
`wait3` does increment/decrement counters from 0 up to 2 and from 2 downto 0 for inner nodes of binary tree.

If something needs to be done, it is always done by the left child.  
```
void wait3 (int n, int p=-1)
{
  if (p==-1)  return wait3(n+P, (n+P)/2);
```
ensures that inition call with threadnum gets converted to call with P+threadnum.
`n` is node in tree, `p` is always its parent node.
Both are needed to decide which call for `p` is from left child.

After `actr[p]` load is at target, the left child does recursive call for parent of `p` if that is not already
the root of binary tree.

Finally
```
+    if (n%2==0) {
+      direction[p] = 1-direction[p]; // reverse direction in next round
+    }
```
ensures that only the left child of `p` does reverse the direction flag after `bctr[p]` load is at target.

## c) 
Write a small test program that demonstrates that your implementation behaves correctly, e.g.
by checking that no thread proceeds past the barrier before all others have reached it. Then
compare the performance of `wait3` against `wait` and `wait2` for a large number of synchronization
cycles and discuss your observations.

### solution

[barrier_test.cc](../scripts/barrier_test.cc) allows to call like this:  
```
./barrier_test #threads #cycles w
```
with w∈{1,2,3} for the performance comparison.

New feature for "checking that no thread proceeds past the barrier before all others have reached it"
is implented into `wait3` in this diff:  
https://github.com/Hermann-SW/uni-heidelberg/blob/main/scripts/Barrier.hh.diff_5.1c.diff

`int last_barrier` is the direction number of last finished barrier. Since directions start with 0,
it is initialized with 1.

This simple addition (for direction 0 case, direction 1 case is done similar) sets 
`last_barrier` to 0 when load of root node reached target (and barrier 0 is complete).
The added `assert` ensures that no thread after `bctr` load at target works before `last_barrier`
has been set. The behavior in case tree-barrier would work incorrectly is just assertion hit:
```
       if (n%2 == 0) {  // left child goes up
         if (p > 1) {
           wait3(p, p/2);
+        } else {  // left child of root declare barrier completed
+          last_barrier = 0;
         }
       }
       bctr[p]++;
       while (bctr[p].load()<2) ;
+      assert(last_barrier == 0);
     }
```

### performance comparisons

The test code does wait for a random number of microseconds for each thread to simulate work:  
```
void f(int i, int w) {
  for (int j = 0; j < cycles; j++) {
    switch (w) {  // block until all threads arrived
      case 1: barrier->wait(i); break;
      case 2: barrier->wait2(i); break;
      case 3: barrier->wait3(i); break;
    }
    usleep(i+(std::rand()%10000));
  }
}
```

The comparisions were done on [AMD 7950X](https://www.techpowerup.com/cpu-specs/ryzen-9-7950x.c2846) 16C/32T CPU,
with SMT enabled:  
```
hermann@7950x:~/uni-heidelberg/scripts$ nproc
32
hermann@7950x:~/uni-heidelberg/scripts$ 
```


For 16 threads `wait`, `wait2` and `wait3` show same elapsed runtime for 1,000 cycles:  
```
hermann@7950x:~/uni-heidelberg/scripts$ /usr/bin/time ./barrier_test 16 1000 1
0.50user 0.19system 0:09.65elapsed 7%CPU (0avgtext+0avgdata 3584maxresident)k
0inputs+0outputs (0major+181minor)pagefaults 0swaps
hermann@7950x:~/uni-heidelberg/scripts$ /usr/bin/time ./barrier_test 16 1000 2
71.71user 0.09system 0:09.56elapsed 750%CPU (0avgtext+0avgdata 3840maxresident)k
0inputs+0outputs (0major+200minor)pagefaults 0swaps
hermann@7950x:~/uni-heidelberg/scripts$ /usr/bin/time ./barrier_test 16 1000 3
70.69user 0.07system 0:09.51elapsed 743%CPU (0avgtext+0avgdata 3840maxresident)k
0inputs+0outputs (0major+184minor)pagefaults 0swaps
hermann@7950x:~/uni-heidelberg/scripts$ 
```

For 32 threads `wait` stays at roughly the same runtime. Interestingly `wait3`
outperforms `wait2` here a bit:
```
hermann@7950x:~/uni-heidelberg/scripts$ /usr/bin/time ./barrier_test 32 1000 1
0.12user 0.69system 0:09.98elapsed 8%CPU (0avgtext+0avgdata 3840maxresident)k
0inputs+0outputs (0major+218minor)pagefaults 0swaps
hermann@7950x:~/uni-heidelberg/scripts$ /usr/bin/time ./barrier_test 32 1000 2
298.28user 2.08system 0:15.04elapsed 1996%CPU (0avgtext+0avgdata 3584maxresident)k
0inputs+0outputs (0major+217minor)pagefaults 0swaps
hermann@7950x:~/uni-heidelberg/scripts$ /usr/bin/time ./barrier_test 32 1000 3
204.28user 2.46system 0:11.70elapsed 1766%CPU (0avgtext+0avgdata 3840maxresident)k
0inputs+0outputs (0major+218minor)pagefaults 0swaps
hermann@7950x:~/uni-heidelberg/scripts$ 
```

For 64 threads `wait` elapsed time does not really increase.
`wait2` elapsed time increases further, and now `wait3` becomes slower than `wait2`:  
```
hermann@7950x:~/uni-heidelberg/scripts$ /usr/bin/time ./barrier_test 64 1000 1
0.21user 0.99system 0:10.03elapsed 12%CPU (0avgtext+0avgdata 3328maxresident)k
0inputs+0outputs (0major+291minor)pagefaults 0swaps
hermann@7950x:~/uni-heidelberg/scripts$ /usr/bin/time ./barrier_test 64 1000 2
664.17user 2.83system 0:23.70elapsed 2813%CPU (0avgtext+0avgdata 3840maxresident)k
0inputs+0outputs (0major+284minor)pagefaults 0swaps
hermann@7950x:~/uni-heidelberg/scripts$ /usr/bin/time ./barrier_test 64 1000 3
737.52user 2.33system 0:25.79elapsed 2868%CPU (0avgtext+0avgdata 3840maxresident)k
0inputs+0outputs (0major+284minor)pagefaults 0swaps
hermann@7950x:~/uni-heidelberg/scripts$ 
```


