# Analysis 1
https://heico.uni-heidelberg.de/heiCO/ee/ui/ca2/app/desktop/#/slc.tm.cp/student/courses/391025

## MathJax
Einfaches [MathJax](https://www.mathjax.org/) Beispiel für [LaTeX](https://de.wikipedia.org/wiki/LaTeX) Formeln (nicht perfekt) im Browser (unterstützt von [github markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github)). Erstellung/Änderung von MathJax am einfachsten mittels **file edit** auf github.com im browser. Öffnen des **Preview** tabs ermöglicht das Beurteilen/Korrigieren vor Speicherung:
<pre>$$\sum\limits_{k=1}^{\infty} \frac{1}{k^2}=\frac{\pi^2}{6}$$</pre>   
$$\sum\limits_{k=1}^{\infty} \frac{1}{k^2}=\frac{\pi^2}{6}$$   

**Tip:** Ausrechnen dieser Formel mit **WolframAlpha**  
https://www.wolframalpha.com/input?i=sum+1%2Fk%5E2%2C+k%3D1+to+infinity


## Lemmata, Sätze, Definitionen, ... der Vorlesungen 1-8
(der rein handschriftlichen Vorlesungen, beginnend mit Vorlesung 9 nicht mehr nötig)

[Vorlesung 1]

# 1. Grundlagen

## 1.1. Mengen und Aussagen

### Definition 1.1.
(Cantor 1895)
Eine Menge ist eine wohldefinierte Zusammenfassung verschiedener Objekte zu einem Ganzen

### Definition 1.2.
Seien $\mathcal{A}$ und $\mathcal{B}$ Mengen

- a) $\mathcal{B}\subset \mathcal{A}$ bedeutet: jedes Element in $\mathcal{B}$ ist auch Element von $\mathcal{A}$; $\mathcal{B}$ ist eine Teilmenge von $\mathcal{A}$

- b) Zwei Mengen $\mathcal{A}$ und $\mathcal{B}$ sind gleich ($\mathcal{A}=\mathcal{B}$) falls $\mathcal{A}\subset \mathcal{B}$ und $\mathcal{B}\subset \mathcal{A}$  
($\mathcal{A}\subset \mathcal{B}$ und $\mathcal{B}\subset \mathcal{A}$) $\Longleftrightarrow \mathcal{A}=\mathcal{B}$

- c) $\mathcal{B}$ ist eine strikte Teilmenge von $\mathcal{A}$, falls existiert ein Element $a\in \mathcal{A}$ mit $a\notin \mathcal{B}$ (Notation $\subsetneq$)

- d) $\emptyset := ${} leere Menge oder Nullmenge  
$\emptyset$ enthält keine Elemente  
Konventionsgemäß $\emptyset \subset \mathcal{A}$ für alle Mengen $\mathcal{A}$

- e) $\mathcal{A}\cup \mathcal{B} :=$ { $a \vert a\in \mathcal{A}$ oder $a \in \mathcal{B}$ }  
Vereinigung von $\mathcal{A}$ und $\mathcal{B}$

- f) $\mathcal{A}\cap \mathcal{B} :=$ { $a \vert a\in \mathcal{A}$ und $a \in \mathcal{B}$ }  
Schnitt oder Durchschnitt von $\mathcal{A}$ und $\mathcal{B}$

- g) $\mathcal{A}\setminus \mathcal{B} :=$ { $a \vert a\in \mathcal{A}$ und $a \notin \mathcal{B}$ }  
Differenz von $\mathcal{A}$ und $\mathcal{B}$

- h) $\mathcal{A}\times \mathcal{B} :=$ { $(a,b) \vert a\in \mathcal{A}, b \in \mathcal{B}$ }  
Produktmenge von $\mathcal{A}$ und $\mathcal{B}$

- i) $\mathcal{A}$ und $\mathcal{B}$ sind disjunkt, falls gilt $\mathcal{A}\cap\mathcal{B}=\emptyset$

[Vorlesung 2]

## 1.2. Abbildungen

### Definition 1.3.
Seien $\mathcal{A}, \mathcal{B}$ zwei Mengen.  
Eine Abbildung $f: \mathcal{A} \to \mathcal{B}$ ist eine Vorschrift, die jedem Element $x\in \mathcal{A}$ genau ein Element $y\in \mathcal{B}$ zuordnet

### Lemma 1.4.
Es sei $f: \mathcal{A} \to \mathcal{B}$ und Teilmengen $\mathcal{A}_1, \mathcal{A}_2 \subset \mathcal{A}$ gegeben.  
Dann gilt: $f(\mathcal{A}_1\cup\mathcal{A}_2)=f(\mathcal{A}_1)\cup f(\mathcal{A}_2)$

### Definition 1.5.
Komposition von Abbildungen $f: \mathcal{A} \to \mathcal{B}, g: \mathcal{B} \to \mathcal{C}$ ist die Abbildung $(g\circ f): \mathcal{A} \to \mathcal{C}$  
$x\mapsto (g\circ f)(x) := g(f(x))$

### Definition 1.6.
Es sei $f: \mathcal{A} \to \mathcal{B}$ eine Abbildung  

- a) $f$ heißt injektiv, falls gilt  
$\forall x_1,x_2\in \mathcal{A}: x_1\neq x_2 \implies f(x_1)\neq f(x_2)$  
oder äquivalent  
$\forall x_1,x_2\in \mathcal{A}: f(x_1)=f(x_2) \implies x_1=x_2$  

- b) $f$ heißt surjektiv, falls gilt  
$\forall y\in \mathcal{B}: \exists x\in \mathcal{A}$ s.d. $y=f(x)$
 
- c) $f$ heißt bijektiv, falls $f$ injektiv und surjektiv  

[Vorlesung 3]

### Satz 1.7.
Sei $f: \mathcal{A} \to \mathcal{B}$ eine bijektive Abbildung.  
Dann existiert genau eine Abbildung $g: \mathcal{B} \to \mathcal{A}$ mit Eigenschaften  
$\forall x\in \mathcal{A}: (g\circ f)(x) = x$  
$\forall y\in \mathcal{B}: (f\circ g)(y) = y$  
Diese Abbildung $g$ heißt Inverse (oder Umkehrabbildung)  
Notation: $f^{-1}$

### Definition 1.8.
Sei $\mathcal{A},\mathcal{B}$ Mengen mit Operationen $\oplus_{\mathcal{A}}$
und $\oplus_{\mathcal{B}}$ (z.B. Addition, Multiplikation)  
Abbildung $f:\mathcal{A}\to\mathcal{B}$ heißt homomorph (strukturerhaltend) wenn gilt:  
$$\forall x_1,x_2 \in\mathcal{A}: f(x_1\oplus_{\mathcal{A}}x_2)=f(x_1)\oplus_{\mathcal{B}}f(x_2)$$

Ein bijektiver Homomorphismus heißt Isomorphismus  
$\mathcal{A}$ und $\mathcal{B}$ mit Struktur heißen isomorph, falls es zwischen $\mathcal{A}$ und $\mathcal{B}$ einen Isomorphismus gibt, dessen Umkehrung ebenfalls Isomorphismus ist.

### Definition 1.9.
- a) &Auml;quivalenzrelation auf einer Menge $\mathcal{A}$ ist eine Beziehung $a\sim b$ zwischen Elementen von $\mathcal{A}$ mit Eigenschaften  
$R_1$: $\forall{a,b}\in \mathcal{A}$ gilt entweder $a\sim b$ oder $a\not\sim b$ (Relation)  
$R_2$: $a\sim a$ (Reflexivit&auml;t)  
$R_3$: $a\sim b \implies b\sim a$ (Symmetrie)  
$R_4$: $a\sim b$, $b\sim c \implies a\sim c$ (Transitivit&auml;t)  

- b) &Auml;quivalenzklassen  
$[a]:=$ { $b\in \mathcal{A}\vert b\sim a$ }    
$a$ heißt Repr&auml;sentant der &Auml;quivalenzklasse $[a]$

## 1.3 Die nat&uuml;rlichen Zahlen. Das Prinzip der vollst&auml;ndigen Induktion

$\mathbb{N}:=$ { $1,2,3,\dots$ }  
$\mathbb{N}_0:=$ { $0,1,2,3,\dots$ } $= \mathbb{N}\cup$ { 0 }

### Axiomensystem der nat&uuml;rlichen Zahlen von Peano (Axiome=Grundannahmen)

1. $1\in\mathbb{N}$
2. $\forall n\in\mathbb{N}\exists!n'\in\mathbb{N}$ als "Nachfolger" von $n$
3. Die Zahl $1$ ist nicht Nachfolger einer nat&uuml;rlichen Zahl
4. $n'=m' \implies n=m$
5. Sei $\mathcal{M}\subset\mathbb{N}$ und $1\in \mathcal{M}$ und $\forall n\in\mathcal{M}: n'\in \mathcal{M}$.  
Dann $\mathcal{M}=\mathbb{N}$

### Vollst&auml;ndige Induktion (Folgerung von Axiom 5)

Zu jedem $n\in \mathbb{N}$ sei $\mathcal{E}(n)$ eine Aussage  
Die Aussage $\mathcal{E}(n)$ ist g&uuml;ltig $\forall n\in\mathbb{N}$ falls gilt:
1. Induktionsanfang: Die Aussage $\mathbb{E}(1)$ ist g&uuml;ltig
2. Induktionsschritt: Unter der Annahme, dass $\mathcal{E}(n)$ g&uuml;ltig ist, gilt auch $\mathcal{E}(n+1)$

## 1.4. Elemente der Kombinatorik

Notation: Sei $m,n\in \mathbb{Z}, m\leq n, a_m,\dots,a_n\in\mathbb{R}$.

Wir definieren $\prod_{k=m}^n a_k:=a_m\cdot\dots\cdot{a_n}$. 

Falls $m>n \prod_{k=m}^{n}a_k:=1$.

### Definition 1.10. Fakult&auml;t  

F&uuml;r $n \in \mathbb{N}_0$ ist 

$n! := \prod_{k=1}^{n} k = 1 \cdot 2 \cdot \dots \cdot n$

### Satz 1.11. (Permutation)
Die Anzahl aller Anordnungen (oder Permutationen) von $n\in \mathbb{N}$ Elementen ist $n!$



### Definition 1.12. Binomialkoeffizient
F&uuml;r $n,k\in\mathbb{N}_0$  
$n\geq k\geq 1$

$$\begin{pmatrix} n  \\ 
k  \end{pmatrix} :=\frac{n\cdot (n-1)\dots (n-k+1)}{k!}$$

$k=0$ 

$$\begin{pmatrix}
n \\
0
\end{pmatrix} :=1$$

$n<k$ 

$$\begin{pmatrix}
n \\
0
\end{pmatrix} :=0$$

### Lemma 1.13.

F&uuml;r $n,k\in\mathbb{N}, 0<k<n$, gilt  

$$\begin{pmatrix}
n \\
k
\end{pmatrix} =
\begin{pmatrix}
n-1 \\
k-1\end{pmatrix}
+
\begin{pmatrix}
n-1 \\
k\end{pmatrix}$$


### Satz 1.13.
Sei $a,b\in\mathbb{R}$ und $n\in\mathbb{N}_0$. 

Dann  

$$(a+b)^n=\sum\limits_{k=0}^n \begin{pmatrix}
n \\
k
\end{pmatrix} a^{n-k}b^k $$

bzw.

$$(a+b)^n=\begin{pmatrix}
n \\
0
\end{pmatrix} a^{n} + \begin{pmatrix}
n \\
1
\end{pmatrix} a^{n-1}b + \begin{pmatrix}
n \\
2
\end{pmatrix} a^{n-2}b^2 + \dots + \begin{pmatrix}
n \\
n-1
\end{pmatrix} ab^{n-1} + \begin{pmatrix}
n \\
n
\end{pmatrix} b^{n}
$$

[Vorlesung 4]

## 1.5 Grundlegendes &uuml;ber die Zahlenmengen $\mathbb{Z}$ und $\mathbb{Q}$

Was ist ein K&ouml;rper? mehr in LA1

Sei $K$ eine Menge mit Operationen/Verkn&uuml;pfungen "+" (Addition)
und " $\cdot$ " (Multiplikation) $(a,b)\mapsto a+b, (a,b)\mapsto a\cdot b$
(Abbildungen $K\times K\mapsto K $)  
Operation "+" erf&uuml;llt Axiome der Addition falls  
- (A1) $\forall a,b\in K: a+b=b+a$ (Kommutativit&auml;t)  
- (A2) $\forall a,b,c\in K: (a+b)+c=a+(b+c)$ (Assoziativit&auml;t)  
- (A3) $\exists 0\in K: \forall a\in K: a+0=0+a$ (Neutrales Element/Nullelement der Addition)  
- (A4) $\forall a\in K \exists -a\in K: a+(-a)=(-a)+a=0$ (Additive Inverse)  

Operation " $\cdot$ " erf&uuml;llt Axiome der Multiplikation falls  
- (M1) $\forall a,b\in K: a\cdot b=b\cdot a$ (Kommutativit&auml;t)  
- (M2) $\forall a,b,c\in K: (a\cdot b)\cdot c=a\cdot (b\cdot c)$ (Assoziativit&auml;t)  
- (M3) $\exists 1\in K\setminus\{0\}=:K^* : \forall a\in K: a\cdot 1=1\cdot a = a$ (Neutrales Element/Einselement der Multiplikation)  
- (M4) $\forall a\in K^* \exists a^{-1}\in K^*: a\cdot a^{-1}=a^{-1}\cdot a=1$ (Multiplikative Inverse)  

Operationen "+" und " $\cdot$ " erf&uuml;llen Distributivit&auml;t  
- (D) $\forall a,b,c\in K: a\cdot (b+c)=a\cdot b+ a\cdot c$

### Definition 1.14 (K&ouml;rper)
Eine Menge $K$ mit Operationen "+" und " $\cdot$ " (K,+, $\cdot$ ) die Axiome A1-A4, M1-M4 und D erf&uuml;llt heißt K&ouml;rper



### Lemma 1.15.
Sei $(K,+,\cdot)$ ein K&ouml;rper. Die Elemente $0,1\in K$ sind durch die Axiome eindeutig bestimmt. Zu $a\in K$ ist das Inverse der Addition und zu $a\in K^*$ das Inverse der Multiplikation eindeutig bestimmt

### Lemma 1.16.
- a) F&uuml;r $a,b\in K$ hat die Gleichung $a+x=b$ genaus eine L&ouml;sung in $K$. Das ist x=b-a\in K$  
- b) $\forall a\in K; -(-a)=a$  
- c) $\forall a,b\in K$: -(a+b)=-a-b=-a+(-b)$  
- d) $\forall a\in K^* \forall b\in K$ hat die Gleichung $ax=b$ genau eine L&ouml;sung in $K$, das ist $x=a^{-1}b$  
- e) $\forall a,b,c\in K: (a+b)c=ac+bc$  
- f) $\forall a\in K: 0a=a0=0$  
- g) Nullteilerfreiheit $ab=0 \implies a=0$ oder $b=0$  
- h) $\forall a\in K: (-1)a=-a$  
- i) Es gilt $(-1)\cdot(-1)=1$  
- j) $\forall a\in K^* : (a^{-1})^{-1}=a$  
- k) $a,b\in K^* : ab\in K^* \ \text{und}\ (ab)^{-1}=b^{-1}a^{-1}$
$$\stackrel{M1}{=}$$ $a^{-1}b^{-1}$  
- l) $(1)^{-1} = \frac{1}{1}=1$  


### Definition 1.17.
Ein angeordneter K&ouml;rper ist ein K&ouml;rper $K$ zusammen mit einer Teilmenge $P\subset K$, die die Axiome O1 und O2 erf&uuml;llt.  
- (O1) $\forall a\in K$ gilt geneau eine der folgenden Aussagen  
  - i) $a\in P$ Schreibweise $a>0$ Sprich $a$ positiv  
  - ii) $a=0$ Schreibweise $a=0$  
  - iii) $-a\in P$ Schreibweise $-a>0$ Sprich $a$ negativ  
- (O2)

$$
\forall a,b\in P \implies a+b, ab \in P&#8203;&#8203;
a,b>0 \implies  \begin{cases}
    a+b>0 \\ 
    ab>0
\end{cases}
$$

### Definition 1.18. (Positivit&auml;t)
Sei $(K,+,\cdot)$ ein angeordneter K&ouml;rper  
$a\in K$ heißt positiv falls $a>0$; $a\in K$ heißt negativ falls $-a>0$  
$K^+:=$ { $a\in K\vert a>0$ }, $K^-:=$ { $a\in K\vert a<0$ }

### Definition 1.19. (Ordnungsrelation)
Sei $(K,+,\cdot,>)$ ein angeordneter K&ouml;rper, $a,b\in K$. Dann  
- $a<b&#8203;:\iff b-a\in K^+$  
- $a>b&#8203;:\iff b<a$  
- $a\leq b&#8203;:\iff (a<b\ \text{oder}\ a=b)$  
- $a\geq b&#8203;:\iff b\leq a$  


### Definition 1.20. Absolutbetrag
Das Maximum zweier Elemente in $(K,+,\cdot,>)$ ist  

$$
\underbrace{max\lbrace a,b\rbrace}_{\in K} := \begin{cases}
    a & \text{falls } a\geq b \\
    b & \text{falls } a\text{<} b
\end{cases} &#8203; a,b\in K
$$

Der Absolutbetrag eines Elementes in $K$ ist  

$$
\vert a\vert := max\lbrace -a, a\rbrace = \begin{cases}
    a & \text{falls } a\geq b \\
    -a & \text{falls } a\text{<} b
\end{cases}
$$

### Satz 1.21.
Seien $a,b\in K$, $K$ angeordneter K&ouml;rper.  
- a) $\vert a\vert\geq 0, \vert a\vert=0 \iff a=0$ &#8203; Definitheit  
- b) $\vert a\cdot b\vert = \vert a\vert\cdot\vert b\vert$ &#8203; Multiplikativit&auml;t  
- c) $\vert a+b\vert \leq \vert a\vert +\vert b\vert$ &#8203; Dreiecksungleichung

