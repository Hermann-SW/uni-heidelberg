
## Plenarübung 5 Diskussion

In der Pleanrübung wurde diskutiert, ob es neben der symmetrischen Gruppe $\mathcal{S}_3$  
noch andere Gruppen mit 6 Elementen gibt. Das Python script [G6.py](../scripts/G6.py) beantwortet dies.  
Die abelsche Gruppe wird z.B. von der 5 zyklisch erzeugt:  

$$\begin{eqnarray*}
5\stackrel{\circ 5}{\to}2\stackrel{\circ 5}{\to}1\stackrel{\circ 5}{\to}4\stackrel{\circ 5}{\to}3\stackrel{\circ 5}{\to}0\stackrel{\circ 5}{\to}5\stackrel{\circ 5}{\to}\dots
\end{eqnarray*}$$

```
$ python G6.py 
nichtisomorphe abelsche Gruppen ( von 60 )
0 1 2 3 4 5
1 0 3 2 5 4
2 3 4 5 0 1
3 2 5 4 1 0
4 5 0 1 2 3
5 4 1 0 3 2

nichtisomorphe nicht abelsche Gruppen ( von 20 )
0 1 2 3 4 5
1 0 3 2 5 4
2 4 0 5 1 3
3 5 1 4 0 2
4 2 5 0 3 1
5 3 4 1 2 0

$
```
