// NOLINTBEGIN(legal/copyright)
/*
   g++ -Wall -Wextra -pedantic -O3 gcds.cpp -o gcds -lgmp -lgmpxx
*/
#include <time.h>
#include <gmpxx.h>
#include <unistd.h>
#include <cassert>
#include <cstdint>

#include <iostream>

// Struct to configure thousands grouping with a comma
struct comma_punct : std::numpunct<char> {
    char do_thousands_sep() const override { return ','; }
    // groups of 3 digits
    std::string do_grouping() const override { return "\3"; }
};

int main(int argc, char *argv[]) {
  // Create a locale using our custom punctuation rule and imbue it into cout
  std::cout.imbue(std::locale(std::cout.getloc(), new comma_punct));

  mpz_class x, y, r, a = x, b = y;
  uint64_t t0, cnt, N = (argc == 1) ? 3000 : atol(argv[1]);

  mpz_fib2_ui(y.get_mpz_t(), x.get_mpz_t(), N);

  std::cout << strlen(mpz_get_str(NULL, 10, y.get_mpz_t()))
            << "-digit consecutive fibonaci numbers" << std::endl;


  a = x; b = y;
  t0 = clock();
  mpz_gcd(r.get_mpz_t(), a.get_mpz_t(), b.get_mpz_t());
  assert(r == 1);
  std::cerr << "mpz_gcd(): "
            << static_cast<float>(clock()-t0) / CLOCKS_PER_SEC
            << "s" << std::endl;


  a = x; b = y; cnt = 0;
  t0 = clock();
  while (a != 0) {
    r = b % a;
    b = a;
    a = r;
    ++cnt;
  }
  assert(b == 1);
  std::cerr << " loop mod: "
            << static_cast<float>(clock()-t0) / CLOCKS_PER_SEC
            << "s (" << cnt << ")" << std::endl;


  a = x; b = y; cnt = 0;
  while (a%2 == 0) a>>=1;
  while (b%2 == 0) b>>=1;

  t0 = clock();
  while (a != 0 && b != 0) {
    if (a < b) {
      b -= a;
      while (b > 0 && b%2 == 0) b>>=1;
    } else {
      a -= b;
      while (a > 0 && a%2 == 0) a>>=1;
    }
    ++cnt;
  }
  assert((a == 0 && b == 1) || (b == 0 && a == 1));
  std::cerr << " loop sub: "
            << static_cast<float>(clock()-t0) / CLOCKS_PER_SEC
            << "s (" << cnt << ")" << std::endl;

  std::cout << "now both approaches tuned by Gemini" << std::endl;

  a = x; b = y; cnt = 0;
  t0 = clock();
  while (a != 0) {
    // Compute remainder directly into r, avoiding temporary mpz_class creation
    mpz_mod(r.get_mpz_t(), b.get_mpz_t(), a.get_mpz_t());

    // O(1) pointer/metadata swaps; avoids deep-copying multi-precision limbs
    b = std::move(a);
    a = std::move(r);

    ++cnt;
  }
  assert(b == 1);
  std::cerr << " loop mod: "
            << static_cast<float>(clock()-t0) / CLOCKS_PER_SEC
            << "s (" << cnt << ")" << std::endl;


  a = x; b = y; cnt = 0;
  while (a%2 == 0) a>>=1;
  while (b%2 == 0) b>>=1;

  t0 = clock();
  while (a != 0 && b != 0) {
    if (a < b) {
        b -= a;
        if (b > 0) {
            uint64_t shift = mpz_scan1(b.get_mpz_t(), 0);
            if (shift > 0) {
                b >>= shift;  // Shift all trailing zeros away in one go
            }
        }
    } else {
        a -= b;
        if (a > 0) {
            uint64_t shift = mpz_scan1(a.get_mpz_t(), 0);
            if (shift > 0) {
                a >>= shift;
            }
        }
    }
    ++cnt;
  }
  assert((a == 0 && b == 1) || (b == 0 && a == 1));
  std::cerr << " loop sub: "
            << static_cast<float>(clock()-t0) / CLOCKS_PER_SEC
            << "s (" << cnt << ")" << std::endl;

  return 0;
}
