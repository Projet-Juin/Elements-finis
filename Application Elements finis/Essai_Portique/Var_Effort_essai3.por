
   RDM - Ossatures
   Calcul des Structures par la M�thode des �l�ments Finis

   Version  - 6.17 - 29 mars 2011

   Utilisateur : support

$debut du fichier
$version
6.17
$SI unites
$nom du fichier
3.por
$date
22/6/2020
$heure
16/26/58
$ossature
plane
$noeuds ( 4 )
   1  5.00000000000E+00  3.00000000000E+00  0.00000000000E+00
   2  5.00000000000E+00  0.00000000000E+00  0.00000000000E+00
   3  0.00000000000E+00  3.00000000000E+00  0.00000000000E+00
   4  0.00000000000E+00  0.00000000000E+00  0.00000000000E+00
   0
$poutres ( 3 )
   1 RIRI     1    2  0.00000000000E+00  0.00000000000E+00  1.00000000000E+00 11 11
   2 RIRI     3    1  0.00000000000E+00  0.00000000000E+00  1.00000000000E+00 11 11
   3 RIRI     3    4  0.00000000000E+00  0.00000000000E+00  1.00000000000E+00 11 11
   0
$sections
11
TYPE QUELCONQUE
NOM *
DESIGNATION *
LOGO 0
AIRE  1.00000000000E-03
IYY  0.00000000000E+00
IZZ  8.33330000000E-08
alpha  0.00000000000E+00
WPY  0.00000000000E+00
WPZ  0.00000000000E+00
TORSION  0.00000000000E+00
KYY  1.0000000
KZZ  1.0000000
IWW  0.00000000000E+00
YCISAILLEMENT  0.00000000000E+00
ZCISAILLEMENT  0.00000000000E+00
BTY  0.00000000000E+00
BTZ  0.00000000000E+00
BTW  0.00000000000E+00
///
0
$materiaux
11
NOM Acier
MOD  2.100E+11
POI 0.3000
MAS 7800.00
DIL  1.3000E-05
LIM  2.500E+08
///
0
$liaisons ( 2 )
encastrement 4
encastrement 2
///
$gpesanteur
10.000
$cas de charges
1
FUNI    3  0.00000000000E+00  0.00000000000E+00  0.00000000000E+00
FUNI    2  0.00000000000E+00  5.00000000000E+03  0.00000000000E+00
FUNI    1 -3.00000000000E+00  0.00000000000E+00  0.00000000000E+00
fnod    3  5.00000000000E+03  0.00000000000E+00  0.00000000000E+00
////
$modes propres
nombre 1
methode sous_espace
precision 1.00000E-02
decalage_spectral 0.00000E+00
////
$maillage
20
$fin du fichier
