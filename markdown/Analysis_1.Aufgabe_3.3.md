
## Hausaufgabe 3.3

Anstelle eines normalen Beweises dass 𝔽₄ ein Körper ist,  
ein automatischer mittels [PARI/GP](https://pari.math.u-bordeaux.fr) script [F4.gp](scripts/F4.gp):
```
$ gp -q < F4.gp 
0 = 
[Mod(0, 2) Mod(0, 2)]

[Mod(0, 2) Mod(0, 2)]

1 = 
[Mod(1, 2) Mod(0, 2)]

[Mod(0, 2) Mod(1, 2)]

a = 
[Mod(0, 2) Mod(1, 2)]

[Mod(1, 2) Mod(1, 2)]

b = 
[Mod(1, 2) Mod(1, 2)]

[Mod(1, 2) Mod(0, 2)]

{0,1,a,b} ist abgeschlossen unter Matrixaddition ✓
{0,1,a,b} ist abgeschlossen unter Matrixmultiplikation ✓
(A1)✓ (A2)✓ (A3)✓ (A4)✓ (M1)✓ (M2)✓ (M3)✓ (M4)✓ (D)✓
𝔽₄ = ({0,1,a,b}, matrix +, matrix *) ist ein Körper
$
```

