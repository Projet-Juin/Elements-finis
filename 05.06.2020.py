import numpy as np
from numpy import linalg
from scipy import *
import pandas as pd

def matrice_rigidite_elementaire_poutre_1valeur_de_L(L,EI): #L est une valeur
    k=np.array([[12,6*L,-12,6*L],[0,4*L**2,-6*L,2*L**2],[0,0,12,-6*L],[0,0,0,4*L**2]])
    m=EI/L
    k=[i*m for i in k]
    return k

def ettendre_1ligne_et_1colonne(tableau): #ajouter 1 ligneet 1 colonne a un tableau
    tableau=append(tableau,[zeros(shape(tableau)[0])],axis=0)
    tableau=append(tableau,zeros((shape(tableau)[0],1)),axis=1)
    return tableau

def fonction_matrice_totale_triangulairesup(tableau1,tableau2): #combinaison 2 par 2 de chaque matrice de rigidité elementaire
    resultat=ettendre_1ligne_et_1colonne(ettendre_1ligne_et_1colonne(tableau1))
    lim21=shape(tableau1)[0]-2
    resultat[lim21][lim21]+=tableau2[0][0]
    resultat[lim21][lim21+1]+=tableau2[0][1]
    resultat[lim21+1][lim21+1]+=tableau2[1][1]
    resultat[lim21+2][lim21+2]+=tableau2[2][2]
    resultat[lim21+2][lim21+3]+=tableau2[2][3]
    resultat[lim21+3][lim21+3]+=tableau2[3][3]
    resultat[lim21][lim21+2]+=tableau2[0][2]
    resultat[lim21][lim21+3]+=tableau2[0][3]
    resultat[lim21+1][lim21+2]+=tableau2[1][2]
    resultat[lim21+1][lim21+3]+=tableau2[1][3]
    return resultat #matrice de rigidité globale sans la partie symétrique

def calcul_matrice_triangulaire_sup(tab,EI) :#faire la matrice assemblée : sur une poutre 1 point ne peut avoir au max que 2 points reliés donc en utilisant la matrice triée par ordre croissant des abscisses des noeuds ca s'ajoute toujours comme ca
    for i in range (0,len(tab)-1):
        if i==0:
            f=matrice_rigidite_elementaire_poutre_1valeur_de_L(tab[i+1]-tab[i],EI)
        else :
            f=fonction_matrice_totale_triangulairesup(f,matrice_rigidite_elementaire_poutre_1valeur_de_L(tab[i+1]-tab[i],EI))
    return f

def calcul_matrice_totale(listeabscisses,EI): #ajouter la partie symétrique a la matrice de rigidité
    matriceglobale=calcul_matrice_triangulaire_sup(sorted(listeabscisses),EI)
    matriceglobale=matriceglobale+np.transpose(matriceglobale)-np.diag(np.diag(matriceglobale))
    return matriceglobale



###### le code commence la #####

### pour la matrice de rigidité

print("Combien d'elements? :")
N_element = int(input())
listeabscisse=[]
for i in range(N_element):
    print("***********Element n°",i+1,"**********")
    print("Valeur du noeud :")
    j = float(input()) #Récupération des différentes valeurs des abscisses
    listeabscisse.append(j)
print("Valeur de E*I :")
EI= float(input())
print(calcul_matrice_totale(listeabscisse,EI))
matricerigidite=calcul_matrice_totale(listeabscisse,EI) # pour la suite

### pour la matrice de deplacement
force=[]
deplacement=[] #pour la matrice de deplacements : en considerant qu'il a rentré les noeuds par ordre croissant abscisses
for i in range(N_element):
    print("***********Element n°",i+1,"**********")
    print("type d'appui' (encastrement, rotule ou rien :")
    j = str(input()) # str : pour la chaine de caracteres
    if j=="encastrement": #dy=phi=0
        deplacement.append([0])
        deplacement.append([0])
    elif j=="rotule": #dy=0 et phi =/=0
        deplacement.append([0])
        deplacement.append([1])
        print("moment :")#IL FAUDRA VOIR POUR LES UNITES
        f = float(input())
        force.append(f)
    elif j=="rien": #dy et phi =/=0
        deplacement.append([1])
        deplacement.append([1])
        print("force")
        f = float(input())
        force.append(f)
        print("moment")
        f = float(input())
        force.append(f)
#print(deplacement)
#print(force)

### pour supprimer tout ce qui est inutile pour calculer f dans f=K.u : en considerant qu'il a rentré les noeuds par ordre croissant abscisses
L=[]
for k in range(0,len(deplacement)):
    if deplacement[k]==[0]:
        L.append(k)
#print(L)#donne les colonnes a supprimer
L=list(reversed(L)) #inverse la liste des colonnes a supprimer
for l in range (len(L)):
    matricerigidite=np.delete(matricerigidite, L[l], 1)
    matricerigidite=np.delete(matricerigidite, L[l], 0)
#print(matricerigidite) #matrice rigidité necessaire au calcul


### pour resoudre le système linéaire : a remodifié pour avoir les forces autrement que en demande au moment du choix des appuis
deplacementinconnu=linalg.solve(matricerigidite,force)
#print("deplacement manquant :")
#print(deplacementinconnu)

### pour afficher tous les déplacements :
i=0
for p in range(len(deplacement)) :
    if deplacement[p]==[1]:
        deplacement[p]=deplacementinconnu[i]
        i=i+1

print(deplacement)




