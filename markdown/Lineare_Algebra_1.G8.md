
## Alle Gruppen mit 8 Eelementen

Dies ist ein followup zur [Bestimmung aller Gruppen mit 6 Elementen](./Lineare_Algebra_1.Plenaruebung_Diskussion.md).

Diese Berechung ist sehr zeitintensiv, wird also besser mit C++ als mit Python gemacht. Das C++ Programm [G8.cpp](../scripts/G8.cpp) verwendet ```std::next_permutation``` geschachtelt um alle Sudokukriterium erfüllenden 8×8 Darstellungen von Gruppen zu bestimmen. Nur für die werden dann die Gruppeneigenschaften überprüft.

Gefundene Gruppen werden auf Isomorphie zu schon vorher gefundenen überprüft. Für den Fall einer neuen Gruppe wird diese ausgegeben.

G8 läuft jetzt schon 24.5h mit 5.5GHz auf meinem AMD 7950X CPU PC. Damit man zwischendurch was sieht, wird bei einer neu gefunden Gruppe etwas geloggt, mit timestamp (Zeit seit Programmstart). In den letzten mehr als 8h ist keine neue Gruppe mehr gefunden worden. Das Programm wurde remote mit ```nohup time ./G8``` gestartet:
```
hermann@7950x:~/uni-heidelberg/scripts$ tail nohup.out 
14:59:48  nicht abelsch  3(96) / 2(87)
15:9:15  nicht abelsch  3(96) / 2(88)
15:14:7  nicht abelsch  3(96) / 2(89)
15:16:12  nicht abelsch  3(96) / 2(90)
15:21:27  nicht abelsch  3(96) / 2(91)
15:31:10  nicht abelsch  3(96) / 2(92)
15:36:57  nicht abelsch  3(96) / 2(93)
15:38:17  nicht abelsch  3(96) / 2(94)
15:46:56  nicht abelsch  3(96) / 2(95)
15:52:9  nicht abelsch  3(96) / 2(96)
hermann@7950x:~/uni-heidelberg/scripts$ 
```

Bisher wurden 96 abelsche und 96 nicht abelsche Gruppen gefunden. Jedoch gibt es unter denen nur 3 nichtisomorphe ablesche und 2 nichtisomorphe nichtabelsche Gruppen.

Abelsche Gruppen nach 24.5h:
```
0 1 2 3 4 5 6 7
1 0 3 2 5 4 7 6
2 3 0 1 6 7 4 5
3 2 1 0 7 6 5 4
4 5 6 7 0 1 2 3
5 4 7 6 1 0 3 2
6 7 4 5 2 3 0 1
7 6 5 4 3 2 1 0
```
```
0 1 2 3 4 5 6 7
1 0 3 2 5 4 7 6
2 3 0 1 6 7 4 5
3 2 1 0 7 6 5 4
4 5 6 7 1 0 3 2
5 4 7 6 0 1 2 3
6 7 4 5 3 2 1 0
7 6 5 4 2 3 0 1
```
```
0 1 2 3 4 5 6 7
1 0 3 2 5 4 7 6
2 3 1 0 6 7 5 4
3 2 0 1 7 6 4 5 
4 5 6 7 2 3 1 0 
5 4 7 6 3 2 0 1 
6 7 5 4 1 0 3 2
7 6 4 5 0 1 2 3
```


Nicht abelsch:
```
0 1 2 3 4 5 6 7
1 0 3 2 5 4 7 6
2 3 0 1 6 7 4 5
3 2 1 0 7 6 5 4
4 5 7 6 0 1 3 2
5 4 6 7 1 0 2 3
6 7 5 4 2 3 1 0
7 6 4 5 3 2 0 1
```
```
0 1 2 3 4 5 6 7
1 0 3 2 5 4 7 6
2 3 1 0 6 7 5 4
3 2 0 1 7 6 4 5 
4 5 7 6 1 0 2 3 
5 4 6 7 0 1 3 2 
6 7 4 5 3 2 1 0 
7 6 5 4 2 3 0 1 
```

All diese Gruppen wurden in den ersten 3 Minuten gefunden.

**Wir sind eigentlich schon fertig!**  
Die [Liste aller Gruppen bis Ordnung 24](https://de.wikipedia.org/wiki/Liste_kleiner_Gruppen#Liste_aller_Gruppen_bis_Ordnung_24) zeigt für Ordnung 8 genau 5 verschiedene Gruppen ...

Von einem früheren Lauf der unbeabsichtigt nach fast 48h abgebrochen wurde weiß ich von mehr als 1000 gefunden Gruppen, da war aber noch nicht die Anzahl der nichtisomorphen geloggt worden.

Es war schon wieder was schief gegangen, nach Neustart ist dies der Zwischenstand nach fast 23h — insgesamt 960 Gruppen, aber nur die 5 schon bekannten nichtisomorphen Gruppen:
```
hermann@7950x:~$ tail uni-heidelberg/scripts/nohup.out 
22:50:24  abelsch  3(471) / 2(480)
22:50:25  abelsch  3(472) / 2(480)
22:50:32  abelsch  3(473) / 2(480)
22:50:33  abelsch  3(474) / 2(480)
22:50:35  abelsch  3(475) / 2(480)
22:50:36  abelsch  3(476) / 2(480)
22:50:45  abelsch  3(477) / 2(480)
22:50:47  abelsch  3(478) / 2(480)
22:50:49  abelsch  3(479) / 2(480)
22:50:51  abelsch  3(480) / 2(480)
hermann@7950x:~$ 
```

After 50.39h:
```
hermann@7950x:~$ top -b -n1 | grep G8
  17308 hermann   20   0    7168   3584   3072 R 100,0   0,0     50,39 G8
hermann@7950x:~$ tail uni-heidelberg/scripts/nohup.out 
49:44:11  nicht abelsch  3(740) / 2(552)
49:44:11  abelsch  3(741) / 2(552)
49:44:11  abelsch  3(742) / 2(552)
49:44:11  abelsch  3(743) / 2(552)
49:44:11  abelsch  3(744) / 2(552)
50:9:51  abelsch  3(745) / 2(552)
50:14:46  abelsch  3(746) / 2(552)
50:19:38  abelsch  3(747) / 2(552)
50:30:13  abelsch  3(748) / 2(552)
50:35:0  abelsch  3(749) / 2(552)
hermann@7950x:~$ 
```
