import numpy
import math
import pandas
import pandas as pd
from numpy import linalg
import numpy as np
import scipy
from scipy import *
import matplotlib.pyplot as pyplot
import matplotlib.pyplot as plt
from matplotlib import patches
#
class Element(object):
    def __init__(self, List_noeud = [], Aire_section = 0, Largeur_section = 0, Hauteur_section = 0, E = 0, I = 0, Coef_poisson = 0):

        #Importation de données
        self.List_noeud = List_noeud
        self.Noeud_label_i, self.Noeud_label_j = List_noeud
        self.Aire_section = Aire_section
        self.E = E
        '''
        self.I = I
        self.EI = E * I
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
        self.k_barre = self.Aire_section * self.E / self.Longueur_poutre
       
        #Créer des matrices
        self.K_local_barre = self. __matrice_locale_barre(self.C, self.S, self.k_barre, self.List_noeud)
        #self.K_local_poutre = self.__matrice_locale_poutre(self.Longueur_poutre, self.EI, self.List_noeud)
        
    #Créer la matrice locale pour barre
    def __matrice_locale_barre(self, C, S, K, A):
        kk = numpy.array([[0 for i in range(4)] for i in range(4)])
        kk=kk.astype(float)
        
        kk[0][0] = C ** 2 * K
        kk[2][2] = C ** 2 * K
        kk[1][1] = S ** 2 * K
        kk[3][3] = S ** 2 * K
        kk[0][1] = C * S * K
        kk[1][0] = C * S * K
        kk[2][3] = C * S * K
        kk[3][2] = C * S * K
        kk[0][2] = - C ** 2 * K
        kk[2][0] = - C ** 2 * K
        kk[1][3] = - S ** 2 * K
        kk[3][1] = - S ** 2 * K
        kk[0][3] = - C * S * K
        kk[1][2] = - C * S * K
        kk[2][1] = - C * S * K
        kk[3][0] = - C * S * K

        #nommage des colonnes et des lignes
        A_colonnes = nommage_matrice_barre_colonnes(A)
        A_lignes = nommage_matrice_barre_lignes(A)
        kk = pandas.DataFrame(kk, columns=A_colonnes, index=A_colonnes)
        return kk
                     
    def create_force_axial(self):
        
       
        A = numpy.array([[1,-1],[-1,1]])
        B = numpy.array([[0 for i in range(4)] for i in range(2)])
        A = A.astype(float)
        B = B.astype(float)
        c = self.C
        s = self.S
        B[0][0] = c
        B[0][1] = s
        B[1][2] = c
        B[1][3] = s
        
        d = self.deplacement_local.to_numpy()
        self.force_axe = self.k_barre * numpy.mat(A) * numpy.mat(B) * numpy.mat(d)
        print(np.squeeze(np.asarray(self.force_axe[1])))
        force_axial_barre.append(np.squeeze(np.asarray(self.force_axe[1])))
    
            
    def create_d_local(self,deplacement,N_noeud):

        E = nommage_matrice_barre_colonnes([i for i in range(1,N_noeud+1)])
        c = list(set(E) - set(nommage_matrice_barre_colonnes(self.List_noeud)))
        for i in c:
            
            deplacement = deplacement.drop(index = i)
            
        self.deplacement_local = deplacement
        
        


class Noeud(object):
    
    def __init__(self, X, Y, Fx = 0, Fy = 0, Mz = 0):
        self.X = X
        self.Y = Y
        self.Fx = Fx
        self.Fy = Fy
        self.Mz = Mz
        
class Ressort(object):
    
    def __init__(self, noeud, resistance):
        self.noeud = noeud
        self.resistance = resistance
        self.k_matrice = self.matrice_Ressort()
    
    def matrice_Ressort(self):
        E = nommage_matrice_barre_colonnes(list(self.noeud))
        Tab = pandas.DataFrame(0,index=E,columns=E)
        for i in E:
            if i in self.resistance.columns:
                Tab[i][i] = self.resistance[i][i]
        return Tab
        

def nommage_matrice_barre_colonnes(listnoeud):
        # Ici on créer une chaine composé des noms des colonnes des matrices barres
        A = []
        for i in range(len(listnoeud)):

            A.append("d" + str(listnoeud[i]) + "x")

            A.append("d" + str(listnoeud[i]) + "y")
        return A
    
def nommage_matrice_force_axial(N_barre):
        # Ici on créer une chaine composé des noms des colonnes des matrices barres
        A = []
        for i in range(N_barre):

            A.append("Force barre" + str(i+1))
        return A
    
def nommage_matrice_barre_lignes(listnoeud):
        # Ici on créer une chaine composé des noms des lignes des matrices barres
        A = []
        for i in range(len(listnoeud)):
            A.append("F" + str(listnoeud[i]) + "x")
            A.append("F" + str(listnoeud[i]) + "y")

        return A


def creation_K_assemble(N_noeud,list_K,list_ressort):

    #On commence par déterminer les noeuds qui seront dans le tableau final.

    #Par exemple pour 2 élements il y'aura 3 noeuds

    E= numpy.array([i for i in range(1,N_noeud+1)]) #On crée un tableau qui part de 1 jusqu'au nombre de noeud

    E = nommage_matrice_barre_colonnes(E) #On en fait E = ["1x","1y","2x","2y",...,"nx","ny"]

    K_final = pandas.DataFrame(0,columns = E,index = E)
    K_final = K_final.astype(float)

    #On créer le K final. Cette table est initialement composé de 0 uniquement.

    #Avec les elements de la liste E en titre de colonne et en titre de ligne


    for i in E:

        for j in E:

            for k in list_K:

                 if i in k.K_local_barre.columns and j in k.K_local_barre.index : #Par exemple on compare

                     K_final[i][j]+= k.K_local_barre[i][j]
                     
            for r in list_ressort:
                
                if i in r.k_matrice.columns and j in r.k_matrice.index :
                     K_final[i][j]+= r.k_matrice[i][j]
                    

    return K_final



def create_F_assemble(listForce,N_noeud):

    E = nommage_matrice_barre_lignes([i for i in range(1,N_noeud+1)])
    Tab = pandas.DataFrame(listForce,index = E,columns = ['F'])

    return Tab

def create_d_assemble(d,N_Noeud):
        
        E = nommage_matrice_barre_colonnes([i for i in range(1,N_Noeud+1)])
        Tab = pandas.DataFrame(0,index = E,columns = ["d"])
        A = ["d"]
        B = []
        for i in E:
            for j in A:
                if j in d.columns and i in d.index : #Par exemple on compare
                    B.append(d[j][i])
                    Tab[j][i]+= d[j][i]
                else :
                    B.append(Tab[j][i]) 
                
        Tab = pandas.DataFrame(B,index = E,columns = ["d"])
        
        return Tab
        
def dessinBarres(liste_poutre,liste_noeud,liste_noeud2):
    list_a = []
    list_b = []
    for i in liste_poutre:
        liste_abscisses = []
        liste_ordonnee = []
        liste_abscisses.append(liste_noeud[i.Noeud_label_i-1].X)
        liste_ordonnee.append(liste_noeud[i.Noeud_label_i-1].Y)
        liste_abscisses.append(liste_noeud[i.Noeud_label_j-1].X)
        liste_ordonnee.append(liste_noeud[i.Noeud_label_j-1].Y)
        list_a.append([liste_abscisses,liste_ordonnee,'b'])
        # if liste_points[i][2][0] == 0 & :
    for i in liste_poutre:
        liste_abscisses2 = []
        liste_ordonnee2 = []
        liste_abscisses2.append(liste_noeud2[i.Noeud_label_i-1].X)
        liste_ordonnee2.append(liste_noeud2[i.Noeud_label_i-1].Y)
        liste_abscisses2.append(liste_noeud2[i.Noeud_label_j-1].X)
        liste_ordonnee2.append(liste_noeud2[i.Noeud_label_j-1].Y)
        list_b.append([liste_abscisses2,liste_ordonnee2,'r--'])
        
    return list_a,list_b
        
        
CL_d=[]
CL_f=[]
RessortSet=[]
ElementSet=[]
NoeudSet=[]
Liaison = []
force_axial_barre = []


def Calculer_Barre(liste_points,liste_poutres):
    list_dataframe = []
    N_noeud = len(liste_points)
    for i in range(len(liste_points)):
        N = Noeud(liste_points[i][1][0], liste_points[i][1][1], liste_points[i][3][0], liste_points[i][3][1], liste_points[i][3][2])
        NoeudSet.append(N)

    for i in range(len(liste_points)):
        a = 1 # Pour recuperer les liaisons de chaque points
        b = 1 #
        c = 1 #
        if liste_points[i][2][0] == 0 :#Selon X
            CL_d.append("d"+str(i+1)+"x")
            CL_f.append("F"+str(i+1)+"x")
            a = 0

        if liste_points[i][2][1] == 0 : #Selon Y
            CL_d.append("d"+str(i+1)+"y")
            CL_f.append("F"+str(i+1)+"y")
            b = 0
        if liste_points[i][2][5] == 0 :
            c = 0
        
        Liaison.append((a,b,c))
            
            
        axe = ["d"+str(i+1)+"x","d"+str(i+1)+"y"]
        a = liste_points[i][4][0]  #A modifier (k Ressort en X)
        b = liste_points[i][4][1]  #A modifier (k Ressort en Y)
        resistance = pandas.DataFrame([[a,0],[0,b]],columns = axe,index = axe)
        ressort = Ressort([i+1],resistance)
        RessortSet.append(ressort)
    for i in range(len(liste_poutres)):
        Aire_section = liste_poutres[i][2] #A vérifier
        Noeud_label_i = int(liste_poutres[i][1][0].split()[1])
        Noeud_label_j = int(liste_poutres[i][1][1].split()[1])
        List_noeud = []
        List_noeud.append(Noeud_label_i)
        List_noeud.append(Noeud_label_j)
        # List_noeud_save.append(Noeud_label_i)
        # List_noeud_save.append(Noeud_label_j);
        E = liste_poutres[i][4] #A vérifier
        #Création d'objets
        Ele = Element(List_noeud = List_noeud, Aire_section = Aire_section, E = E)
        
        ElementSet.append(Ele)
        ElementSet[i].__calcule__()
        
    K_final = creation_K_assemble(N_noeud, ElementSet,RessortSet)
    K_assemble = K_final

    print(K_final)

    list_F = []

    for i in NoeudSet :

        list_F.append(i.Fx)

        list_F.append(i.Fy)

    F_final = create_F_assemble(list_F,N_noeud)
    F_assemble = F_final
    for i in CL_d:
        K_final = K_final.drop(index = i,columns = i)

    for i in CL_f:
        F_final = F_final.drop(index=i)


    deplacement = linalg.solve(K_final.to_numpy(),F_final.to_numpy())
    deplacement = pandas.DataFrame(deplacement,index = list(K_final.columns), columns = ['d'])
    deplacement = create_d_assemble(deplacement,N_noeud)
    list_dataframe.append(("Deplacement",deplacement))
    
    print("deplacement")
    print(deplacement)
    
    for i in range(len(liste_poutres)):
         ElementSet[i].create_d_local(deplacement, N_noeud)
         print("force axial barre ",i+1)
         ElementSet[i].create_force_axial()
    
    liste_abscisses = []
    liste_ordonnee = []
    NoeudSet2 = []
    for i in range(len(NoeudSet)):
        N = Noeud(NoeudSet[i].X+ float(deplacement["d"]["d"+str(i+1)+"x"]), NoeudSet[i].Y+ float(deplacement["d"]["d"+str(i+1)+"y"]), NoeudSet[i].Fx,NoeudSet[i].Fy, NoeudSet[i].Mz)
        NoeudSet2.append(N)
        
    list_a , list_b = dessinBarres(ElementSet,NoeudSet,NoeudSet2)
    graph = ["déplacement (en m)",*list_a,*list_b]
    print("Efforts intérieurs : ")
    
    list_graph = []
    list_graph.append(graph)
    matrice_force_barre = [i for i in force_axial_barre]
    matrice_force_barre = pandas.DataFrame(matrice_force_barre,index = nommage_matrice_force_axial(len(ElementSet)), columns = ['N'])
    print(matrice_force_barre)
    
    list_dataframe.append(("Effort Normal",matrice_force_barre))
    
    
    del ElementSet[:]
    del NoeudSet[:]
    del NoeudSet2[:]
    del CL_d[:]
    del CL_f[:]
    del RessortSet[:]
    del Liaison[:]
    del force_axial_barre[:]
    
    return list_graph , list_dataframe
    
    
         