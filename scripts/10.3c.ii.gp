
A=[Mod(0,2),Mod(1,2),Mod(1,2);Mod(1,2),Mod(0,2),Mod(1,2);Mod(1,2),Mod(1,2),Mod(0,2)];

N=3;
U=["\\bot","\\top"];

ID()=matrix(N,,i,j,Mod((i==j),2));
D(i0,a)=matrix(N,,i,j,Mod((i==j)*if(i==i0,a,1),2));
S(i0,j0,a)=matrix(N,,i,j,Mod((i==j)+a*(i==i0&&j==j0),2));
T(i0,j0)=matrix(N,,i,j,Mod((i==j&&i!=i0&&j!=j0)+(i==j0&&j==i0)+(i==i0&&j==j0),2));

header()={
  print("\\documentclass[a4paper,11pt]{article}");
  print("\\usepackage{amsmath, amsfonts, amsthm, amssymb}");
  print("\\begin{document}");
  print("\\begin{eqnarray*}");
}

pmat(A)={
  print1("\\begin{bmatrix}");
  foreach(A~,r,foreach(r,e,print1(U[1+lift(e)]"&"));print("\\\\"));
  print1("\\end{bmatrix}");
};

footer()={
print("\\end{eqnarray*}");
  print("\\end{document}");
}
\\print(S(4,3,1,3));
\\	print(S(4,3,1,3)^-1);

B=ID();
C=A;

simple_row()={
  print("&=&");
  pmat(B);
  pmat(C);
  print("\\\\");
}

row(f,s)={
  M=eval(f);
  print("&=&");
  print("\\left(");
  pmat(B);
  print("\\underset{"s"^{-1}}{\\underbrace{");
  pmat(M^-1);
  print("}}\\right)");
  print("\\left(");
  print("\\underset{"s"}{\\underbrace{");
  pmat(M);
  print("}}");
  pmat(C);
  print("\\right)");
  print("\\\\");
  B=B*M^-1;
  C=M*C;
}

header();
pmat(A); simple_row();
row("T(2,1)","T_{2,1}"); simple_row();
row("S(3,1,1)","S_{3,1}(1)"); simple_row();
row("S(3,2,1)","S_{3,2}(1)"); simple_row();
\\print("\\end{eqnarray*}\\newpage\\begin{eqnarray*}");
\\row("S(4,1,1)","S_{4,1}(1)"); simple_row();
\\row("S(4,2,-1)","S_{4,2}(-1)"); simple_row();
\\row("S(3,2,-1)","S_{3,2}(-1)"); simple_row();
print("\\end{eqnarray*}Nach streichen der rechten/unteren Spalte/Zeile");
print("erhalten wir die Rangfaktorisierung mit Rang(A)=2\\begin{eqnarray*}");
B=B[,1..2];
C=C[1..2,];
pmat(A);
simple_row();
footer();
