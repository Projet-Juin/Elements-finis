import numpy
import math
import pandas
import pandas as pd
from numpy import linalg
import numpy as np
import scipy
from scipy import *


def nommage_matrice_portique_colonnes(listnoeud):
        # Ici on créer une chaine composé des noms des colonnes des matrices barres
        A = []
        for i in range(len(listnoeud)):
            A.append("u" + str(listnoeud[i])+ "°")
            A.append("v" + str(listnoeud[i])+ "°")
            A.append("theta" + str(listnoeud[i]))
        return A

def nommage_matrice_portique_lignes(listnoeud):
        # Ici on créer une chaine composé des noms des lignes des matrices barres
        A = []
        for i in range(len(listnoeud)):
            A.append("u" + str(listnoeud[i])+ "°")
            A.append("v" + str(listnoeud[i])+ "°")
            A.append("theta" + str(listnoeud[i]))
        return A

def __matrice_locale_portique_ko(self, C, S, K, A,E,I,L):
    kro = numpy.array([[0 for i in range(5)] for i in range(5)])
    K=A*E/L
    kro[0][0] = C ** 2 * K
    kro[3][3] = C ** 2 * K
    kro[1][1] = S ** 2 * K
    kro[4][4] = S ** 2 * K
    kro[0][1] = C * S * K
    kro[1][0] = kro[0][1]
    kro[3][4] = C * S * K
    kro[4][3] = kro[3][4]
    kro[0][3] = - C ** 2 * K
    kro[3][0] = kro[0][3]
    kro[1][4] = - S ** 2 * K
    kro[4][1] = kro[1][4]
    kro[0][4] = - C * S * K
    kro[1][3] = - C * S * K
    kro[3][1] = kro[1][3]
    kro[4][0] = kro[0][4]
    kk= numpy.array([[0 for i in range(6)] for i in range(6)])
    P=E*I  #a modifier avec les classes
    kk[0][0] = P*12*(s**2)/(L**3)
    kk[0][1] = P*12*c*(s**2)/(L**3)
    kk[0][2] = P*6*s/(L**2)
    kk[0][3] =-P*12*(s**2)/(L**3)
    kk[0][4] = P*12*c*(s**2)/(L**3)
    kk[0][5] = P*6*s/(L**2)
    kk[1][0] = kk[0][1]
    kk[1][1] = P*12*(c**2)/(L**3)
    kk[1][2] =-P*6*c/(L**2)
    kk[1][3] = P*12*c*s/(L**3)
    kk[1][4] =-P*12*(c**2)/(L**3)
    kk[1][5] =-P*6*c/(L**2)
    kk[2][0] = kk[0][2]
    kk[2][1] = kk[1][2]
    kk[2][2] = P*4/L
    kk[2][3] =-P*6*s/(L**2)
    kk[2][4] = P*6*c/(L**2)
    kk[2][5] = P*2/L
    kk[3][0] = kk[0][3]
    kk[3][1] = kk[1][3]
    kk[3][2] = kk[2][3]
    kk[3][3] = P*12*(s**2)/(L**3)
    kk[3][4] = -P*12*c*s/(L**3)
    kk[3][5] = -P*6*s/(L**2)
    kk[4][0] = kk[0][4]
    kk[4][1] = kk[1][4]
    kk[4][2] = kk[2][4]
    kk[4][3] = kk[3][4]
    kk[4][4] = P*12*(c**2)/(L**3)
    kk[4][5] = P*6*c/(L**2)
    kk[5][0] = kk[0][5]
    kk[5][1] = kk[1][5]
    kk[5][2] = kk[2][5]
    kk[5][3] = kk[3][5]
    kk[5][4] = kk[4][5]
    kk[5][5] = 4*L

    K_elementaire=kk+kro

    #nommage des colonnes et des lignes
    A_colonnes = nommage_matrice_portique_colonnes(A)
    A_lignes = nommage_matrice_portique_lignes(A)
    K_elementaire = pandas.DataFrame(K_elementaire, columns=A_colonnes, index=A_colonnes)
    return K_elementaire


def creation_K_assemble(N_noeud,list_K):

    #On commence par déterminer les noeuds qui seront dans le tableau final.
    #Par exemple pour 2 élements il y'aura 3 noeuds

    E= numpy.array([i for i in range(1,N_noeud+1)]) #On crée un tableau qui part de 1 jusqu'au nombre de noeud
    E = nommage_matrice_portique_colonnes(E) #On en fait E = ["u1","v1","theta1",...,"un","vn","thetan"]
    K_final = pandas.DataFrame(0,columns = E,index = E)
#On créer le K final. Cette table est initialement composé de 0 uniquement.
    #Avec les elements de la liste E en titre de colonne et en titre de ligne

    print(K_final)

    for i in E:
        for j in E:
            for k in list_K:
                 if i in k.K_local_portique.columns and j in k.K_local_portique.index :
                    K_final[i][j]+= k.K_local_portique[i][j]
    return K_final


def create_F_assemble(listForce,N_noeud):
    E = nommage_matrice_portique_lignes([i for i in range(1,N_noeud+1)])
    Tab = pandas.DataFrame(listForce,index = E,columns = ['F'])
    return Tab

def create_d_assemble(d,N_Noeud):
    E = nommage_matrice_portique_lignes([i for i in range(1,N_noeud+1)])
    return d_assemble


ElementSet = []
NoeudSet = []
List_noeud_save = []

print("Combien d'elements? :")
N_element = int(input())

for i in range(N_element):                                      #cette boucle ne bouge pas entre barre et portique
    #Les données utilisées ici sont celles qui ont été saisies précédemment.
    print("***********Element n°", i + 1, "**********")
    print("Aire_section :")
    Aire_section = float(input())
    '''
    print("Largeur_section :")
    Largeur_section = float(input())
    print("Hauteur_section :")
    Hauteur_section = float(input())
    '''
    print("Numero du 1er noeud :")
    Noeud_label_i = int(input())
    print("Numero du 2eme noeud :")
    Noeud_label_j = int(input())
    List_noeud = []
    List_noeud.append(Noeud_label_i)
    List_noeud.append(Noeud_label_j)
    List_noeud_save.append(Noeud_label_i)
    List_noeud_save.append(Noeud_label_j)
    print("Module de Young :")
    E = float(input())
    '''
    print("Moment d’inertie :")
    I = float(input())
    print("Coefficient de Poisson :")
    Coef_poisson = float(input())
    '''

    #Création d'objets
    Ele = Element(List_noeud = List_noeud, Aire_section = Aire_section, E = E)
    ElementSet.append(Ele)

N_noeud = len(list(set(List_noeud_save)))
for i in range(N_noeud):
    print("***********Noeud n°", i + 1, "**********")
    print("type d'appui' (encastrement, rotule ou rien) :")
    type = str(input())  # str : pour la chaine de caracteres
    print("coordonnée abscisse pour noeud", i + 1, ": ")
    X = float(input())
    print("coordonnée ordonnée pour noeud", i + 1, ": ")
    Y = float(input())
    print("Fx pour noeud", i + 1, ": ")
    Fx = float(input())
    print("Fy pour noeud", i + 1, ": ")
    Fy = float(input())
    print("Mz pour noeud", i + 1, ": ")
    Mz = float(input())
    N = Noeud(X, Y, type, Fx, Fy, Mz)
    NoeudSet.append(N)

for i in range(N_element):
    ElementSet[i].__calcule__()
    # exemple de sortie
    K_local_portique = ElementSet[i].K_local_portique
    print("K_local_portique={}".format(K_local_portique))


CL_d = [] # Contiendra les colonnes et les lignes à enlever
CL_f = []

for i in range(N_noeud):
    print("**************** Noeud ",i+1,"***************\n")
    print("liberté selon X")
    a = int(input())
    if a == 0 :
        CL_d.append("u"+str(i+1)+"x")
        CL_f.append("F"+str(i+1)+"x")

    print("liberté selon Y")
    a = int(input())
    if a == 0 :
        CL_d.append("u"+str(i+1)+"y")
        CL_f.append("F"+str(i+1)+"y")

    print("liberté selon ")
    a = int(input())
    if a == 0 :  ####rajout pour theta avec moment
        CL_d.append("theta"+str(i+1))
        CL_f.append("F"+str(i+1)+"M")

K_final = creation_K_assemble(N_noeud, ElementSet)
K_assemble = K_final
print(K_final)

list_F = []
for i in NoeudSet :
    list_F.append(i.Fx)
    list_F.append(i.Fy)
    list_F.append(i.FM)

F_final = create_F_assemble(list_F,N_noeud)
F_assemble = F_final
for i in CL_d:
    K_final = K_final.drop(index = i,columns = i)

for i in CL_f:
    F_final = F_final.drop(index=i)


deplacement = linalg.solve(K_final.to_numpy(),F_final.to_numpy())

print(deplacement)




""" NOTES :

Pour convertir matrice nn en 1*n et inversement :
 a=np.arange(16)
>>> a
array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15])
>>> a.reshape(4,4)
array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11],
       [12, 13, 14, 15]])
>>> a.reshape(2,8)
array([[ 0,  1,  2,  3,  4,  5,  6,  7],
       [ 8,  9, 10, 11, 12, 13, 14, 15]])
"""
