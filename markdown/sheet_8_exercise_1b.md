Sheet 8, exercise 1b: 

Show that system of linear diophantine equations  

$$ 
Ax=b \textrm{ with } A = \begin{pmatrix}
2 & 0 & 1 \\
4 & 5 & 2 \\
3 & 7 & 0
\end{pmatrix} \textrm{ and } b = \begin{pmatrix}
-2 \\
1 \\
7
\end{pmatrix}
$$  

is solvable.

Solution making use of PARI/GP $matsnf()$ to determine Smith normal form (~ is vector/matrix transpose).
Diophantine solution exists because all elementary divisors $D_{i,i}$ divide $(Mb)_i$ ($y_i$ is the quotient):
<table border=1>
<tr><td><pre><code>$ cat ex_8_1_b.gp 
A=[2, 0, 1; 4, 5, 2; 3, 7, 0];
b=[-2, 1, 7];
[M,N,D]=matsnf(A,flag=1);
D==M*A*N
 
D
 
 
 
 
 
y=vector(#D,i,(M*b~)[i]/D[i,i])~
x=N*y
A*x==b~
$
</code></pre>
</td><td>
<pre><code> 
 
 
$ gp -q < ex_8_1_b.gp
1
 
[15 0 0]
 
[ 0 1 0]
 
[ 0 0 1]
 
[-3, 1, 7]~
[0, 1, -2]~
1
$ </code></pre></td></td>
</table>
