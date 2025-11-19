
# Analysis 1
https://heico.uni-heidelberg.de/heiCO/ee/ui/ca2/app/desktop/#/slc.tm.cp/student/courses/391025

## MathJax
Einfaches [MathJax](https://www.mathjax.org/) Beispiel für [LaTeX](https://de.wikipedia.org/wiki/LaTeX) Formeln (nicht perfekt) im Browser (unterstützt von [github markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github)):  
<pre>$$\sum\limits_{k=0}^{\infty} \frac{1}{k^2}=\frac{\pi^2}{6}$$</pre>   
$$\sum\limits_{k=0}^{\infty} \frac{1}{k^2}=\frac{\pi^2}{6}$$   

Erstellung/Änderung von MathJax am einfachsten mittels *file edit* auf github.com im browser.  
Öffnen des *Preview* tabs ermöglicht das Beurteilen/Korrigieren vor Speicherung.

## Lemmata, Sätze, Definitionen, ... der Vorlesungen 1-8
(der rein handschriftlichen Vorlesungen, beginnend mit Vorlesung 9 nicht mehr nötig)

[Vorlesung 1]

# 1. Grundlagen

## 1.1. Mengen und Aussagen

### Definition 1.1
(Cantor 1895)
Eine Menge ist eine wohldefinierte Zusammenfassung verschiedener Objekte zu einem Ganzen

### Definition 1.2.
Seien $\mathcal{A}$ und $\mathcal{B}$ Mengen

a) $\mathcal{B}\subset \mathcal{A}$ bedeutet: jedes Element in $\mathcal{B}$ ist auch Element von $\mathcal{A}$; $\mathcal{B}$ ist eine Teilmenge von $\mathcal{A}$

b) Zwei Mengen $\mathcal{A}$ und $\mathcal{B}$ sind gleich ($\mathcal{A}=\mathcal{B}$) falls $\mathcal{A}\subset \mathcal{B}$ und $\mathcal{B}\subset \mathcal{A}$  
($\mathcal{A}\subset \mathcal{B}$ und $\mathcal{B}\subset \mathcal{A}$) $\Longleftrightarrow \mathcal{A}=\mathcal{B}$

c) $\mathcal{B}$ ist eine strikte Teilmenge von $\mathcal{A}$, falls existiert ein Element $a\in \mathcal{A}$ mit $a\notin \mathcal{B}$ (Notation $\subsetneq$)

d) $\emptyset := ${} leere Menge oder Nullmenge  
$\emptyset$ enthält keine Elemente  
Konventionsgemäß $\emptyset \subset \mathcal{A}$ für alle Mengen $\mathcal{A}$

e) $\mathcal{A}\cup \mathcal{B} :=$ { $a \vert a\in \mathcal{A}$ oder $a \in \mathcal{B}$ }  
Vereinigung von $\mathcal{A}$ und $\mathcal{B}$

f) $\mathcal{A}\cap \mathcal{B} :=$ { $a \vert a\in \mathcal{A}$ und $a \in \mathcal{B}$ }  
Schnitt oder Durchschnitt von $\mathcal{A}$ und $\mathcal{B}$

g) $\mathcal{A}\setminus \mathcal{B} :=$ { $a \vert a\in \mathcal{A}$ und $a \notin \mathcal{B}$ }  
Differenz von $\mathcal{A}$ und $\mathcal{B}$

h) $\mathcal{A}\times \mathcal{B} :=$ { $(a,b) \vert a\in \mathcal{A}, b \in \mathcal{B}$ }  
Produktmenge von $\mathcal{A}$ und $\mathcal{B}$

i) $\mathcal{A}$ und $\mathcal{B}$ sind disjunkt, falls gilt $\mathcal{A}\cap\mathcal{B}=\emptyset$

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

a) $f$ heißt injektiv, falls gilt  
$\forall x_1,x_2\in \mathcal{A}: x_1\neq x_2 \implies f(x_1)\neq f(x_2)$  
oder äquivalent  
$\forall x_1,x_2\in \mathcal{A}: f(x_1)=f(x_2) \implies x_1=x_2$  

b) $f$ heißt surjektiv, falls gilt  
$\forall y\in \mathcal{B}: \exists x\in \mathcal{A}$ s.d. $y=f(x)$

b) $f$ heißt bijektiv, falls $f$ injektiv und surjektiv  

[Vorlesung 3]

### Satz 1.7.
Sei $f: \mathcal{A} \to \mathcal{B}$ eine bijektive Abbildung.  
Dann existiert genau eine Abbildung $g: \mathcal{B} \to \mathcal{A}$ mit Eigenschaften  
$\forall x\in \mathcal{A}: (g\circ f)(x) = x$  
$\forall y\in \mathcal{B}: (f\circ g)(y) = y$  
Diese Abbildung $g$ heißt Inverse (oder Umkehrabbildung)  
Notation: $f^{-1}$
