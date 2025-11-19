\\ verify that 𝔽₄ = ({0,1,a,b}, matrix +, matrix *) is a field
\\
assert(b,s="")={if(!(b),error(Str(s)))};

F4 = { [[0,0;   \\ 0
         0,0],
        [1,0;   \\ 1
         0,1],
        [0,1;   \\ a
         1,1],
        [1,1;   \\ b
         1,0]] * Mod(1,2); }

slF4 = vecsort(lift(F4));
inF4(M)=vecsearch(slF4,lift(M));

{
  F4m0=F4[2..#F4];  \\ Fm0 = F4\{0}
  zero=F4[1];
   one=F4[2];

  printp("0 = ",zero);
  printp("1 = ",one);
  printp("a = ",F4[3]);
  printp("b = ",F4[4]);

  foreach(F4,a,
    foreach(F4,b,
      assert(inF4(a+b),"add not closed")));
  print("{0,1,a,b} ist abgeschlossen unter Matrixaddition ✓");

  foreach(F4,a,
    foreach(F4,b,
      assert(inF4(a*b),"mul not closed")));
  print("{0,1,a,b} ist abgeschlossen unter Matrixmultiplikation ✓");

  foreach(F4,a,
    foreach(F4,b,
      assert(a+b==b+a,"A1")));
  print1("(A1)✓ ");

  foreach(F4,a,
    foreach(F4,b,
      foreach(F4,c,
        assert(a+(b+c)==(a+b)+c,"A2"))));
  print1("(A2)✓ ");

  foreach(F4,a,
    assert(a+zero==a && zero+a==a,"A3"));
  print1("(A3)✓ ");

  foreach(F4,a,
    assert(a+(-a)==zero && (-a)+a==zero,"A4"));
  print1("(A4)✓ ");

  foreach(F4,a,
    foreach(F4,b,
      assert(a*b==b*a,"M1")));
  print1("(M1)✓ ");

  foreach(F4m0,a,
    foreach(F4m0,b,
      foreach(F4m0,c,
        assert(a*(b*c)==(a*b)*c,"M2"))));
  print1("(M2)✓ ");

  foreach(F4,a,
    assert(a*one==a && one*a==a,"M3"));
  print1("(M3)✓ ");

  [a,b] = F4[3..#F4];
  assert(one*(-one)==one && (-one)*one==one,"M4 1");
  assert(a*b==one && b*a==one,"M4 a,b");
  print1("(M4)✓ ");

  foreach(F4,a,
    foreach(F4,b,
      foreach(F4,c,
        assert(a*(b+c)==a*b+a*c,"dist"))));
  print("(D)✓");

  print("𝔽₄ = ({0,1,a,b}, matrix +, matrix *) ist ein Körper");
}
