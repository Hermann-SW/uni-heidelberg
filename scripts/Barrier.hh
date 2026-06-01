#ifndef HASC_BARRIER_HH
#define HASC_BARRIER_HH

#include <vector>
#include <mutex>
#include <condition_variable>
#include <atomic>

// barrier as a class
// it implements two version: with mutexes and without mutexes
class Barrier
{
  int P; // number of threads in barrier
  int count; // count number of threads that arrived at the barrier
  std::vector<int> flag; // flag indicating waiting thread
  std::mutex mx; // mutex for use with the cvs
  std::vector<std::condition_variable> cv; // for waiting
  std::atomic<int> acounter, bcounter; // two counters for mutex-free version
  std::vector<int> direction; // store counting direction in mutex-free version
  std::vector<std::atomic<int>> actr, bctr; // two counters for tree-barrier version

public:
  // set up barrier for given number of threads
  Barrier (int P_) : P(P_), count(0), flag(P_,0), cv(P_), direction(P,0),
                     actr(P_), bctr(P_)
  {
    acounter.store(0);
    bcounter.store(0);
  }

  // get number of threads
  int nthreads ()
  {
    return P;
  }

  // tree-barrier version; excercise 5.1b
  // counters for inner nodes of binary tree (1..P-1)
  // P is power of two
  // leaves are P..2*P-1, or P+threadnum
  void wait3 (int n, int p=-1)
  {
    if (p==-1)  return wait3(n+P, (n+P)/2);

    if (direction[p]==0)
    {
      actr[p]++;
      while (actr[p].load()<2) ;
      if (n%2 == 0) {  // left child goes up
        if (p > 1) {
          wait3(p, p/2);
        }
      }
      bctr[p]++;
      while (bctr[p].load()<2) ;
    }
    else
    {
      actr[p]--;
      while (actr[p].load()>0) ;
      if (n%2 == 0) {  // left child goes up
        if (p > 1) {
          wait3(p, p/2);
        }
      }
      bctr[p]--;
      while (bctr[p].load()>0) ;
    }

    if (n%2==0) {
      direction[p] = 1-direction[p]; // reverse direction in next round
    }
  }

  // mutex-free version; do not mix with other version!
  void wait2 (int i)
  {
    if (direction[i]==0)
    {
      acounter++;
      while (acounter.load()<P) ;
      bcounter++;
      while (bcounter.load()<P) ;
    }
    else
    {
      acounter--;
      while (acounter.load()>0) ;
      bcounter--;
      while (bcounter.load()>0) ;
    }
    direction[i] = 1-direction[i]; // reverse direction in next round
  }

  // mutex-based version
  void wait (int i)
  {
    // sequential case
    if (P==1) return;
    
    std::unique_lock<std::mutex> ul{mx};
    count += 1; // one more
    if (count<P)
      {
        // wait on my cv until all have arrived
        flag[i] = 1; // indicate I am waiting
        cv[i].wait(ul,[i,this]{return this->flag[i]==0;}); // wait
      }
    else
      {
        // I am the last one, lets wake them up
        count = 0; // reset counter for next turn
        for (int j=0; j<P; j++)
          if (flag[j]==1)
            {
              flag[j] = 0; // the event
              cv[j].notify_one(); // wake up
            }
      }
  }
};  

#endif
