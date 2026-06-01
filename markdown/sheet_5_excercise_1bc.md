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

## c) 
Write a small test program that demonstrates that your implementation behaves correctly, e.g.
by checking that no thread proceeds past the barrier before all others have reached it. Then
compare the performance of `wait3` against `wait` and `wait2` for a large number of synchronization
cycles and discuss your observations.
