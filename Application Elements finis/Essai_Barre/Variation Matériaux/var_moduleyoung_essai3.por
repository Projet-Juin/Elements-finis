
   RDM - Ossatures
   Calcul des Structures par la M�thode des �l�ments Finis

   Version  - 7.04 - 5 mars 2020

   Utilisateur : Lansana

$debut du fichier
$version
7.04
$SI unites
$nom du fichier
var_moduleyoung_essai3.por
$date
21/6/2020
$heure
19/47/53
$ossature
plane
$noeuds ( 3 )
   1  0.00000000000E+000  0.00000000000E+000  0.00000000000E+000
   2 -4.00000000000E+000  3.00000000000E+000  0.00000000000E+000
   3 -4.00000000000E+000  0.00000000000E+000  0.00000000000E+000
   0
$poutres ( 2 )
   1 RIRI     1    2  0.00000000000E+000  0.00000000000E+000  1.00000000000E+000 51 11
   2 RIRI     1    3  0.00000000000E+000  0.00000000000E+000  1.00000000000E+000 51 11
   0
$sections
51
TYPE QUELCONQUE
NOM *Quelconque
DESIGNATION *
LOGO 0
AIRE  6.00000000000E-004
IYY  0.00000000000E+000
IZZ  1.00000000000E-008
alpha  0.00000000000E+000
WPY  0.00000000000E+000
WPZ  0.00000000000E+000
TORSION  0.00000000000E+000
KYY  1.0000000
KZZ  1.0000000
IWW  0.00000000000E+000
YCISAILLEMENT  0.00000000000E+000
ZCISAILLEMENT  0.00000000000E+000
BTY  0.00000000000E+000
BTZ  0.00000000000E+000
BTW  0.00000000000E+000
///
0
$materiaux
11
NOM Essai3
MOD  2.500E+010
POI 0.3000
MAS 7800.00
DIL  1.3000E-005
LIM  2.500E+008
///
0
$liaisons ( 2 )
encastrement 2
encastrement 3
///
$gpesanteur
10.000
$cas de charges
1
fnod    1 -1.00000000000E+006  0.00000000000E+000  0.00000000000E+000
////
$modes propres
nombre 1
methode sous_espace
precision 1.00000E-002
decalage_spectral 0.00000E+000
////
$maillage
20
$fin du fichier
