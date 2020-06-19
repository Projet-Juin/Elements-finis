import numpy
import math
import pandas
import pandas as pd
from numpy import linalg
import numpy as np
import scipy
from scipy import *
import matplotlib.pyplot as plt
import matplotlib
class Element(object):
    
    def __init__(self, List_noeud = [], Aire_section = 0, Largeur_section = 0, Hauteur_section = 0, E = 0, I = 0, Coef_poisson = 0):

        #Importation de données
        self.List_noeud = List_noeud
        self.Noeud_label_i, self.Noeud_label_j = List_noeud
        self.Aire_section = Aire_section
        self.E = E
        self.I = I
        self.EI = E * I
        '''
        self.Coef_poisson = Coef_poisson
        self.Largeur_section = Largeur_section
        self.Hauteur_section = Hauteur_section
        '''

    def __calcule__(self):
        self.Longueur_poutre = numpy.sqrt(
            (NoeudSet[self.Noeud_label_i - 1].X - NoeudSet[self.Noeud_label_j - 1].X) ** 2 + (
                        NoeudSet[self.Noeud_label_i - 1].Y - NoeudSet[self.Noeud_label_j - 1].Y) ** 2)
        self.C = ((NoeudSet[self.Noeud_label_j - 1].X - NoeudSet[self.Noeud_label_i - 1].X)) / self.Longueur_poutre
        self.S = ((NoeudSet[self.Noeud_label_j - 1].Y - NoeudSet[self.Noeud_label_i - 1].Y)) / self.Longueur_poutre

        #Créer des matrices
        self.K_local_portique = self. __matrice_locale_portique_ko(self.C, self.S, self.Aire_section, self.E, self.I, self.Longueur_poutre, self.List_noeud)
        #self.K_local_poutre = self.__matrice_locale_poutre(self.Longueur_poutre, self.EI, self.List_noeud)

    #Créer la matrice locale
    def __matrice_locale_portique_ko(self, C, S, A, E, I, L, List_n):
        # print(C)
        # print(S)
        kro = numpy.array([[0.0 for i in range(6)] for i in range(6)])
        K = A * E / L
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
        # print("kro :")
        # print(kro)
        kk = numpy.array([[0.0 for i in range(6)] for i in range(6)])
        P = E * I  # a modifier avec les classes
        kk[0][0] = P * 12 * (S ** 2) / (L ** 3)
        kk[0][1] = P * 12 * C * (S ** 2) / (L ** 3)
        kk[0][2] = P * 6 * S / (L ** 2)
        kk[0][3] = -P * 12 * (S ** 2) / (L ** 3)
        kk[0][4] = P * 12 * C * (S ** 2) / (L ** 3)
        kk[0][5] = P * 6 * S / (L ** 2)
        kk[1][0] = kk[0][1]
        kk[1][1] = P * 12 * (C ** 2) / (L ** 3)
        kk[1][2] = -P * 6 * C / (L ** 2)
        kk[1][3] = P * 12 * C * S / (L ** 3)
        kk[1][4] = -P * 12 * (C ** 2) / (L ** 3)
        kk[1][5] = -P * 6 * C / (L ** 2)
        kk[2][0] = kk[0][2]
        kk[2][1] = kk[1][2]
        kk[2][2] = P * 4 / L
        kk[2][3] = -P * 6 * S / (L ** 2)
        kk[2][4] = P * 6 * C / (L ** 2)
        kk[2][5] = P * 2 / L
        kk[3][0] = kk[0][3]
        kk[3][1] = kk[1][3]
        kk[3][2] = kk[2][3]
        kk[3][3] = P * 12 * (S ** 2) / (L ** 3)
        kk[3][4] = -P * 12 * C * S / (L ** 3)
        kk[3][5] = -P * 6 * S / (L ** 2)
        kk[4][0] = kk[0][4]
        kk[4][1] = kk[1][4]
        kk[4][2] = kk[2][4]
        kk[4][3] = kk[3][4]
        kk[4][4] = P * 12 * (C ** 2) / (L ** 3)
        kk[4][5] = P * 6 * C / (L ** 2)
        kk[5][0] = kk[0][5]
        kk[5][1] = kk[1][5]
        kk[5][2] = kk[2][5]
        kk[5][3] = kk[3][5]
        kk[5][4] = kk[4][5]
        kk[5][5] = P * 4 / L
        # print("kbo :")
        # print(kk)
        K_elementaire = kk + kro

        # nommage des colonnes et des lignes
        A_colonnes = nommage_matrice_portique_colonnes(List_n)
        A_lignes = nommage_matrice_portique_lignes(List_n)
        K_elementaire = pandas.DataFrame(K_elementaire, columns=A_colonnes, index=A_colonnes)
        return K_elementaire

class Noeud(object):
    def __init__(self, X, Y, type = "rien", Fx = 0, Fy = 0, Mz = 0):
        self.type = type
        self.X = X
        self.Y = Y
        self.Fx = Fx
        self.Fy = Fy
        self.Mz = Mz

#fonctions a ajouter :
'''
def moment_charge_uniformement_repartie (force,longueur_section):
    M_reparti=force*(longueur_section**2)/12
    return M_reparti

def force_charge_uniformement_repartie (force,longueur_section):
    F_repartie=force*longueur_section/2
    return F_repartie
'''

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

def creation_K_assemble(N_noeud,list_K):

    #On commence par déterminer les noeuds qui seront dans le tableau final.
    #Par exemple pour 2 élements il y'aura 3 noeuds

    E= numpy.array([i for i in range(1,N_noeud+1)]) #On crée un tableau qui part de 1 jusqu'au nombre de noeud
    E = nommage_matrice_portique_colonnes(E) #On en fait E = ["u1","v1","theta1",...,"un","vn","thetan"]
    K_final = pandas.DataFrame(0.0,columns = E,index = E)
#On créer le K final. Cette table est initialement composé de 0 uniquement.
    #Avec les elements de la liste E en titre de colonne et en titre de ligne

    #print(K_final)

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


def CalculerPortique(liste_points,liste_poutres) :
    N_noeud = len(liste_points)
    taille_maillage = 10
    
    
    for i in range(len(liste_points)):
        N = Noeud(liste_points[i][1][0], liste_points[i][1][1], liste_points[i][3][0], liste_points[i][3][1], liste_points[i][3][2])
        NoeudSet.append(N)
        
    for i in range(len(liste_points)):
        if liste_points[i][2][0] == 0 :#Selon X
            CL_d.append("u"+str(i+1)+"°") 
            CL_f.append("u"+str(i+1)+"°")

        if liste_points[i][2][1] == 0 : #Selon Y
            CL_d.append("v"+str(i+1)+"°")
            CL_f.append("v"+str(i+1)+"°")
        if liste_points[i][2][2] == 0 : #Le moment
            CL_d.append("theta"+str(i+1))
            CL_f.append("theta"+str(i+1))
    for i in range(len(liste_poutres)):
        Aire_section = liste_poutres[i][2]
        Noeud_label_i = int(liste_poutres[i][1][0].split()[1])
        Noeud_label_j = int(liste_poutres[i][1][1].split()[1])
        List_noeud = []
        List_noeud.append(Noeud_label_i)
        List_noeud.append(Noeud_label_j)
        # List_noeud_save.append(Noeud_label_i)
        # List_noeud_save.append(Noeud_label_j)
        E = liste_poutres[i][4]
        I = liste_poutres[i][3]
        #Création d'objets
        Ele = Element(List_noeud = List_noeud, Aire_section = Aire_section, E = E,I =I)
        ElementSet.append(Ele)
        ElementSet2.append(Ele)
    for i in range(len(liste_poutres)):
        ElementSet[i].__calcule__()
        ElementSet2[i].__calcule__()
    plotun = []
    for i in ElementSet:
        list_X = []
        list_Y = []
        list_X.append(NoeudSet[i.Noeud_label_i-1].X)
        list_X.append(NoeudSet[i.Noeud_label_j-1].X)
        list_Y.append(NoeudSet[i.Noeud_label_i-1].Y)
        list_Y.append(NoeudSet[i.Noeud_label_j-1].Y)
        plotun.append([list_X,list_Y])
        plt.plot(list_X,list_Y,'-.', c="red", marker='o')
        
    Element_supprime = []
    for i in range(len(liste_poutres)):
        Nde = int(liste_poutres[i][0].split()[1])
        F = float(liste_poutres[i][5][0])
        N_parties_maillage = taille_maillage
        L = ElementSet[Nde - 1].Longueur_poutre
        C = ElementSet[Nde - 1].C
        S = ElementSet[Nde - 1].S
        F_total = L * F
        '''
        print(ElementSet[Nde - 1].Noeud_label_i)
        print(ElementSet[Nde - 1].Noeud_label_j)
        print(F_total)
        '''
        N_noeud += N_parties_maillage - 1
        # Ajout de nouveaux noeuds
        for j in range(N_parties_maillage - 1):
            X = (NoeudSet[ElementSet[Nde - 1].Noeud_label_j - 1].X - NoeudSet[
                ElementSet[Nde - 1].Noeud_label_i - 1].X) / N_parties_maillage * (j + 1) + NoeudSet[
                    ElementSet[Nde - 1].Noeud_label_i - 1].X
            Y = (NoeudSet[ElementSet[Nde - 1].Noeud_label_j - 1].Y - NoeudSet[
                ElementSet[Nde - 1].Noeud_label_i - 1].Y) / N_parties_maillage * (j + 1) + NoeudSet[
                    ElementSet[Nde - 1].Noeud_label_i - 1].Y
            N = Noeud(X, Y, "rien", F_total / N_parties_maillage * S, - F_total / N_parties_maillage * C, 0)
            NoeudSet.append(N)
    
        NoeudSet[ElementSet[Nde - 1].Noeud_label_i - 1].Fx += F_total * S / N_parties_maillage / 2
        NoeudSet[ElementSet[Nde - 1].Noeud_label_i - 1].Fy += - F_total * C / N_parties_maillage / 2
        NoeudSet[ElementSet[Nde - 1].Noeud_label_i - 1].Mz += F * (L / N_parties_maillage) ** 2 / 12
        NoeudSet[ElementSet[Nde - 1].Noeud_label_j - 1].Fx += F_total * S / N_parties_maillage / 2
        NoeudSet[ElementSet[Nde - 1].Noeud_label_j - 1].Fy += - F_total * C / N_parties_maillage / 2
        NoeudSet[ElementSet[Nde - 1].Noeud_label_j - 1].Mz += - F * (L / N_parties_maillage) ** 2 / 12
    
        # Ajout de nouveaux éléments
        for j in range(N_parties_maillage - 2):
            List_noeud = []
            List_noeud.append(len(list(set(NoeudSet))) - j)
            List_noeud.append(len(list(set(NoeudSet))) - 1 - j)
            Ele = Element(List_noeud=List_noeud, Aire_section=ElementSet[Nde - 1].Aire_section, E=ElementSet[Nde - 1].E,
                          I=ElementSet[Nde - 1].I)
            ElementSet.append(Ele)
    
        if N_parties_maillage > 1:
            List_noeud = []
            List_noeud.append(len(list(set(NoeudSet))))
            List_noeud.append(ElementSet[Nde - 1].Noeud_label_j)
            Ele = Element(List_noeud=List_noeud, Aire_section=ElementSet[Nde - 1].Aire_section, E=ElementSet[Nde - 1].E,
                          I=ElementSet[Nde - 1].I)
            ElementSet.append(Ele)
            List_noeud = []
            List_noeud.append(len(list(set(NoeudSet))) - N_parties_maillage + 2)
            List_noeud.append(ElementSet[Nde - 1].Noeud_label_i)
            Ele = Element(List_noeud=List_noeud, Aire_section=ElementSet[Nde - 1].Aire_section, E=ElementSet[Nde - 1].E,
                          I=ElementSet[Nde - 1].I)
            ElementSet.append(Ele)
            Element_supprime.append(ElementSet[Nde - 1])
    
    #     for i in range(len(list(set(NoeudSet)))):
    #         print("Noeud :", i + 1)
    #         print(NoeudSet[i].X)
    #         print(NoeudSet[i].Y)
    #         print(NoeudSet[i].Fx)
    #         print(NoeudSet[i].Fy)
    #         print(NoeudSet[i].Mz)
    # print(Element_supprime)
    
    # for i in range(len(list(set(ElementSet)))):
    #     print("element :", i + 1)
    #     print(ElementSet[i].Noeud_label_i)
    #     print(ElementSet[i].Noeud_label_j)
    
    # Suppression des éléments superflus
    for i in Element_supprime:
        ElementSet.remove(i)
        ElementSet2.remove(i)
    
    for i in ElementSet2:
        L = i.Longueur_poutre
        C = i.C
        S = i.S
        F_total = L * F
        '''
        print(ElementSet[Nde - 1].Noeud_label_i)
        print(ElementSet[Nde - 1].Noeud_label_j)
        print(F_total)
        '''
        N_noeud += N_parties_maillage - 1
        # Ajout de nouveaux noeuds
        for j in range(N_parties_maillage - 1):
            X = (NoeudSet[i.Noeud_label_j - 1].X - NoeudSet[
                i.Noeud_label_i - 1].X) / N_parties_maillage * (j + 1) + NoeudSet[
                    i.Noeud_label_i - 1].X
            Y = (NoeudSet[i.Noeud_label_j - 1].Y - NoeudSet[
                i.Noeud_label_i - 1].Y) / N_parties_maillage * (j + 1) + NoeudSet[
                    i.Noeud_label_i - 1].Y
            N = Noeud(X, Y, "rien", 0, 0, 0)
            NoeudSet.append(N)
    
        # Ajout de nouveaux éléments
        for j in range(N_parties_maillage - 2):
            List_noeud = []
            List_noeud.append(len(list(set(NoeudSet))) - j)
            List_noeud.append(len(list(set(NoeudSet))) - 1 - j)
            Ele = Element(List_noeud=List_noeud, Aire_section=ElementSet[Nde - 1].Aire_section, E=ElementSet[Nde - 1].E,
                          I=ElementSet[Nde - 1].I)
            ElementSet.append(Ele)
    
        if N_parties_maillage > 1:
            List_noeud = []
            List_noeud.append(len(list(set(NoeudSet))))
            List_noeud.append(i.Noeud_label_j)
            Ele = Element(List_noeud=List_noeud, Aire_section=i.Aire_section, E=i.E,
                          I=i.I)
            ElementSet.append(Ele)
            List_noeud = []
            List_noeud.append(len(list(set(NoeudSet))) - N_parties_maillage + 2)
            List_noeud.append(i.Noeud_label_i)
            Ele = Element(List_noeud=List_noeud, Aire_section=i.Aire_section, E=i.E,
                          I=i.I)
            ElementSet.append(Ele)
    
    for i in ElementSet2:
        ElementSet.remove(i)
    
    
    for i in range(len(list(set(ElementSet)))):
        ElementSet[i].__calcule__()
        
    K_final = creation_K_assemble(N_noeud, ElementSet)
    K_assemble = K_final
    list_F = []
    for i in NoeudSet :
        list_F.append(i.Fx)
        list_F.append(i.Fy)
        list_F.append(i.Mz)

    F_final = create_F_assemble(list_F,N_noeud)
    # print(F_final)
    F_assemble = F_final
    for i in CL_d:
        K_final = K_final.drop(index = i,columns = i)
    
    for i in CL_f:
        F_final = F_final.drop(index=i)
    
    # print(F_final)
    # print(K_final)
    
    deplacement = linalg.solve(K_final.to_numpy(),F_final.to_numpy())
    
    # print(deplacement)
    j = 0

    for i in range(N_noeud):
        ui = "u" + str(i + 1) + "°"
        vi = "v" + str(i + 1) + "°"
        thi = "theta" + str(i + 1)
        if ui in F_final.index:
            NoeudSet[i].X += deplacement[j]
            j += 1
        if vi in F_final.index:
            NoeudSet[i].Y += deplacement[j]
            j += 1
        if thi in F_final.index:
            j += 1
    
    # for i in range(N_noeud):
    #     print(NoeudSet[i].X)
    #     print(NoeudSet[i].Y)
    
    plotdeux = []
    for i in ElementSet:
        list_X = []
        list_Y = []
        # print(i.Noeud_label_i)
        # print(NoeudSet[i.Noeud_label_i-1].X)
        # print(NoeudSet[i.Noeud_label_i - 1].Y)
        # print(i.Noeud_label_j)
        # print(NoeudSet[i.Noeud_label_j - 1].X)
        # print(NoeudSet[i.Noeud_label_j - 1].Y)
        list_X.append(NoeudSet[i.Noeud_label_i-1].X)
        list_X.append(NoeudSet[i.Noeud_label_j-1].X)
        list_Y.append(NoeudSet[i.Noeud_label_i-1].Y)
        list_Y.append(NoeudSet[i.Noeud_label_j-1].Y)
        plotdeux.append([list_X,list_Y])
        # plt.plot(list_X,list_Y)
    
    # plt.xlabel('x')
    # plt.ylabel('y')
    
    # plt.show()
    return plotun , plotdeux
    
CL_d=[]
CL_f=[]
RessortSet=[]
ElementSet=[]
NoeudSet=[]
ElementSet2 = []


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

