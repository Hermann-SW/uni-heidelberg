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

public:
  // set up barrier for given number of threads
  Barrier (int P_) : P(P_), count(0), flag(P_,0), cv(P_), direction(P,0)
  {
    acounter.store(0);
    bcounter.store(0);
  }

  // get number of threads
  int nthreads ()
  {
    return P;
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
