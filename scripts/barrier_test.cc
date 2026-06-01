/*
f=barrier_test
g++-14 -O3 -ftree-vectorize -mavx512f -mfma -fopt-info-vec -o $f $f.cc -lm
cpplint --filter=-legal/copyright $f.cc
cppcheck --enable=all --suppress=missingIncludeSystem $f.cc --check-config
*/
#include <unistd.h>
#include <iostream>
#include <thread>  // NOLINT [build/c++11]
#include <vector>
#include <cassert>
#include "./Barrier.hh"

int N = 0;
int cycles = 0;
Barrier *barrier = NULL;

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

int main(int argc, char *argv[]) {
  assert(argc == 4 && "./barrier_test #threads #cycles w  (with w in [[1,3]])");
  N = atoi(argv[1]);
  cycles = atoi(argv[2]);
  int w = atoi(argv[3]);
  assert(!(N & (N - 1)));  // power of 2
  assert(cycles > 0);
  assert(w > 0 && w < 4);

  std::srand(std::time({}));

  barrier = new Barrier(N);

  std::vector<std::thread> th;
  for (int i = 0; i < N; ++i)
    th.push_back(std::thread{f, i, w});
  for (int i = 0; i < N; ++i)
    th[i].join();

  return 0;
}
