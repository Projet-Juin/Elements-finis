# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:45:48 2020

@author: ombli
"""

import numpy as np
from numpy import linalg
import scipy
from scipy import *
import pandas as pd


##### fonctions utiles par la suite ###

#fonction créant la matrice de rigidité entre 2 noeuds
def matrice_rigidite_elementaire_poutre_1valeur_de_L(L,EI):                     #L est la longueur entre 2 noeuds
    k=np.array([[12,6*L,-12,6*L],[0,4*L**2,-6*L,2*L**2],[0,0,12,-6*L],[0,0,0,4*L**2]]) #matrice  sans EI/L
    m=EI/L                                                                      #constante devant la matrice
    k=[i*m for i in k]                                                          #matrice rigidité finie
    return k

#fonction ajoutant 1 ligne et 1 colonne à un tableau
def ettendre_1ligne_et_1colonne(tableau):
    tableau=append(tableau,[zeros(shape(tableau)[0])],axis=0)
    tableau=append(tableau,zeros((shape(tableau)[0],1)),axis=1)
    return tableau


#fonction combinant les matrices élémentaires 2 par 2 : # on garde la matrice des 2 premiers noeuds et on ajoute les matrices les une après les autres dans le sens croissants des abscisses des noeuds # on obtient à la fin la matrice triangulaire supérieure car la partie inférieure et symétrique
def fonction_matrice_totale_triangulairesup(tableau1,tableau2):
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
    print(resultat)
    return resultat #matrice de rigidité globale sans la partie symétrique

def calcul_matrice_triangulaire_sup(tab,EI) :#faire la matrice assemblée #permet de dire où va le nouveau tableau : il faut bien dire que pour le premier il est en haut à gauche et quand on ajoute ca va sur le bloc en bas a droite
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

print("Combien d'elements? :")                              #nombre de noeuds sur la poutre
N_element = int(input())
listeabscisse=[]
for i in range(N_element):
    print("***********Element n°",i+1,"**********")
    print("Valeur du noeud :")
    j = float(input())                                      #Récupération des différentes valeurs des abscisses des noeuds
    listeabscisse.append(j)
print("Valeur de E*I :")
EI= float(input())
print("***matrice rigidité assemblée : ")
print(calcul_matrice_totale(listeabscisse,EI))
matricerigidite=calcul_matrice_totale(listeabscisse,EI) # pour la suite car sera modifiee
matricerigiditefixe=matricerigidite #ne bougera plus

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
        deplacement[p]=[deplacementinconnu[i]]
        i=i+1
print("***matrice déplacements")
print(deplacement)


### pour afficher la matrice force

force=np.dot(matricerigiditefixe,deplacement)
print("***matrice forces")
print(force)
