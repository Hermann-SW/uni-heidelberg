// NOLINTNEXTLINE(legal/copyright)
/*
   determine all groups on 8 Elements
   output nonisomorphic representants

   f=G8
   g++ -O3 -Wall -Wextra -pedantic $f.cpp -o $f
   cpplint $f.cpp
*/
#include<iostream>
#include<algorithm>
#include<vector>
#include<ctime>

const int n = 8;
typedef std::vector<std::vector<int>> matrix;

// NOLINTNEXTLINE(runtime/references)
void pprint(matrix& G) {
  for (int r = 0; r < n; ++r) {
    std::for_each(G[r].begin(), G[r].end(), [](auto i)
                    { std::cout << i << " "; });
    std::cout << "\n";
  }
  std::cout << std::endl;
}

// NOLINTNEXTLINE(runtime/references)
bool inverses(matrix& G) {
  for (int r = 1; r < n; ++r) {
    bool found = false;
    for (int c = 1; c < n; ++c) {
      if (G[r][c] == 0 && G[c][r] == 0) {
        found = true;
        break;
      }
    }
    if (!found)  return false;
  }
  return true;
}

// NOLINTNEXTLINE(runtime/references)
bool assoziativ(matrix& G) {
  for (int a = 0; a < n; ++a) {
    for (int b = 0; b < n; ++b) {
      for (int c = 0; c < n; ++c) {
        if (G[G[a][b]][c] != G[a][G[b][c]]) {
          return false;
        }
      }
    }
  }
  return true;
}

// NOLINTNEXTLINE(runtime/references)
bool abelsch(matrix& G) {
  for (int r = 0; r < n; ++r) {
    for (int c = 0; c < n; ++c) {
      if (G[r][c] != G[c][r]) {
        return false;
      }
    }
  }
  return true;
}

// NOLINTNEXTLINE(runtime/references)
bool isomorph(matrix& U, matrix& V) {
  std::vector<int> P({0, 1, 2, 3, 4, 5, 6, 7});
  do {
    bool good = true;
    for (int a = 0; a < n; ++a) {
      for (int b = 0; b < n; ++b) {
        if (P[V[a][b]] != U[P[a]][P[b]]) {
          good = false;
          break;
        }
      }
    }
    if (good)  return true;
  }
  // NOLINTNEXTLINE(whitespace/empty_loop_body)
  while (std::next_permutation(P.begin(), P.end()));
  return false;
}

// NOLINTNEXTLINE(runtime/references)
void non_isomorph_groups(std::vector<matrix>& L) {
  if (L.size() == 0)  return;
  pprint(L[0]);
  for (unsigned a = 1; a < L.size(); ++a) {
    bool good = true;
    for (unsigned b = 0; b < a; ++b) {
      if (isomorph(L[a], L[b])) {
        good = false;
        break;
      }
    }
    if (good)  pprint(L[a]);
  }
}

// NOLINTNEXTLINE(runtime/references)
void non_isomorph_last_group(std::vector<matrix>& L, int& c) {
  if (L.size() == 0)  return;
  int a = L.size()-1;
  bool good = true;
  for (int b = 0; b < a; ++b) {
    if (isomorph(L[a], L[b])) {
      good = false;
      break;
    }
  }
  if (good)  { c+=1; pprint(L[a]); }
}

// NOLINTNEXTLINE(runtime/references)
bool ok1(matrix& G, int r, int c) {
  int b = 0x00;
  for (int i = 0; i <= r; ++i) {
    if (b&(1 << G[i][c]))  return false;
    b|=(1 << G[i][c]);
  }
  return true;
}

// NOLINTNEXTLINE(runtime/references)
bool ok(matrix& G, int r) {
  for (int c = 1; c < n; ++c) {
    if (!ok1(G, r, c)) {
      // guarantee that next std::next_generation will change column c(!)
      std::sort(G[r].begin()+c+1, G[r].end(), std::greater<int>());
      return false;
    }
  }
  return true;
}

int main() {
  matrix G{
      {0, 1, 2, 3, 4, 5, 6, 7},
      {0, 1, 2, 3, 4, 5, 6, 7},
      {0, 1, 2, 3, 4, 5, 6, 7},
      {0, 1, 2, 3, 4, 5, 6, 7},
      {0, 1, 2, 3, 4, 5, 6, 7},
      {0, 1, 2, 3, 4, 5, 6, 7},
      {0, 1, 2, 3, 4, 5, 6, 7},
      {0, 1, 2, 3, 4, 5, 6, 7}
  };
  time_t now, start = time(0);

  for (int r = 0; r < n; ++r) { G[r]=G[0]; G[r][0]=r; G[r][r]=0; }

  std::vector<matrix> A, N;
  int a = 0, n = 0;

  std::sort(G[1].begin()+1, G[1].end());
  do {
    if (!ok(G, 1))  continue;
    std::sort(G[2].begin()+1, G[2].end());
    do {
      if (!ok(G, 2))  continue;
      std::sort(G[3].begin()+1, G[3].end());
      do {
        if (!ok(G, 3))  continue;
        std::sort(G[4].begin()+1, G[4].end());
        do {
          if (!ok(G, 4))  continue;
          std::sort(G[5].begin()+1, G[5].end());
          do {
            if (!ok(G, 5))  continue;
            std::sort(G[6].begin()+1, G[6].end());
            do {
              if (!ok(G, 6))  continue;
              std::sort(G[7].begin()+1, G[7].end());
              do {
                if (!ok(G, 7))  continue;
                if (inverses(G)) {
                  if (assoziativ(G)) {
                    bool abelian = true;
                    if (abelsch(G)) {
                      A.push_back(G);
                    } else {
                      N.push_back(G);
                      abelian = false;
                    }
                    now = time(0)-start;
                    std::cout
                      << now/3600 <<":"<< (now%3600)/60 <<":"<< now%60 << "  "
                      << (abelian?"":"nicht ") << "abelsch  "
                      << a << "(" << A.size() << ") / "
                      << n << "(" << N.size() << ")" << std::endl;
                    non_isomorph_last_group(abelian?A:N, abelian?a:n);
                  }
                }
              }
              // NOLINTNEXTLINE(whitespace/empty_loop_body)
              while (std::next_permutation(G[7].begin()+1, G[7].end()));
            }
            while (std::next_permutation(G[6].begin()+1, G[6].end()));  //NOLINT
          }
          while (std::next_permutation(G[5].begin()+1, G[5].end()));  // NOLINT
        }
        while (std::next_permutation(G[4].begin()+1, G[4].end()));  // NOLINT
      }
      while (std::next_permutation(G[3].begin()+1, G[3].end()));  // NOLINT
    }
    while (std::next_permutation(G[2].begin()+1, G[2].end()));  // NOLINT
  }
  while (std::next_permutation(G[1].begin()+1, G[1].end()));  // NOLINT

  std::cout << a << " nichtisomorphe abelsche Gruppen von " << A.size() << "\n";
  std::cout << n << " nichtisomorphe nicht abelsche Gruppen von "
            << N.size() << std::endl;

  return 0;
}
