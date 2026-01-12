
A=[4,6,11;6,6,15;-2,0,-4;2,6,7];

N=4;

ID()=matrix(N,,i,j,(i==j));
D(i0,a)=matrix(N,,i,j,(i==j)*if(i==i0,a,1));
S(i0,j0,a)=matrix(N,,i,j,(i==j)+a*(i==i0&&j==j0));
T(i0,j0)=matrix(N,,i,j,(i==j&&i!=i0&&j!=j0)+(i==j0&&j==i0)+(i==i0&&j==j0));

header()={
  print("\\documentclass[a4paper,11pt]{article}");
  print("\\usepackage{amsmath, amsfonts, amsthm, amssymb}");
  print("\\begin{document}");
  print("\\begin{eqnarray*}");
}

pmat(A)={
  print1("\\begin{bmatrix}");
  foreach(A~,r,foreach(r,e,print1(e"&"));print("\\\\"));
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
row("T(3,1)","T_{3,1}"); simple_row();
row("S(2,1,3)","S_{2,1}(3)"); simple_row();
row("S(3,1,2)","S_{3,1}(2)"); simple_row();
print("\\end{eqnarray*}\\newpage\\begin{eqnarray*}");
row("S(4,1,1)","S_{4,1}(1)"); simple_row();
row("S(4,2,-1)","S_{4,2}(-1)"); simple_row();
row("S(3,2,-1)","S_{3,2}(-1)"); simple_row();
print("\\end{eqnarray*}Nach streichen der beiden rechten/unteren Spalten/Zeilen");
print("erhalten wir die Rangfaktorisierung mit Rang(A)=2\\begin{eqnarray*}");
B=B[,1..2];
C=C[1..2,];
pmat(A);
simple_row();
footer();
