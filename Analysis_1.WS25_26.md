
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

# 1. Grundlagen

## 1.1. Mengen und Aussagen

### Definition 1.1 (Cantor 1895)
Eine Menge ist eine wohldefinierte Zusammenfassung verschiedener Objekte zu einem Ganzen

### Definition 1.2. Seien $\mathcal{A}$ und $\mathcal{B}$ Mengen
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

