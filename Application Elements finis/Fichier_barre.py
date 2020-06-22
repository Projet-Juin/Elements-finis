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
        vectA = (NoeudSet[self.Noeud_label_j - 1].X - NoeudSet[self.Noeud_label_i - 1].X)
        vectB = (NoeudSet[self.Noeud_label_j - 1].Y - NoeudSet[self.Noeud_label_i - 1].Y)
        self.Longueur_poutre = numpy.sqrt(
            (NoeudSet[self.Noeud_label_i - 1].X - NoeudSet[self.Noeud_label_j - 1].X) ** 2 + (
                    NoeudSet[self.Noeud_label_i - 1].Y - NoeudSet[self.Noeud_label_j - 1].Y) ** 2)
        self.C = ((NoeudSet[self.Noeud_label_j - 1].X - NoeudSet[self.Noeud_label_i - 1].X)) / self.Longueur_poutre
        self.S = ((NoeudSet[self.Noeud_label_j - 1].Y - NoeudSet[self.Noeud_label_i - 1].Y)) / self.Longueur_poutre
        print("Check")
        print(self.Longueur_poutre)
        print(self.C)
        print(self.S)
        self.k_barre = self.Aire_section * self.E / self.Longueur_poutre
       
        #Créer des matrices
        self.K_local_barre = self. __matrice_locale_barre(self.C, self.S, self.k_barre, self.List_noeud)
        #self.K_local_poutre = self.__matrice_locale_poutre(self.Longueur_poutre, self.EI, self.List_noeud)

    #Créer la matrice locale pour barre
    def __matrice_locale_barre(self, C, S, K, A):
        print("C", C)
        print("S", S)
        print(K)
        print(C ** 2 * K)
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
        print(kk)
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
        print("c=",c)
        print("s=",s)
        B[0][0] = c
        B[0][1] = s
        B[1][2] = c
        B[1][3] = s
        
        d = self.deplacement_local.to_numpy()
        self.force_axe = self.k_barre * numpy.mat(A) * numpy.mat(B) * numpy.mat(d)
        print(self.force_axe)
    
            
    def create_d_local(self,deplacement,N_noeud):

        E = nommage_matrice_barre_colonnes([i for i in range(1,N_noeud+1)])
        print(E)
        c = list(set(E) - set(nommage_matrice_barre_colonnes(self.List_noeud)))
        print(c)
        for i in c:
            
            deplacement = deplacement.drop(index = i)
            
        print(deplacement)
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
        print(Tab)
        return Tab
        

def nommage_matrice_barre_colonnes(listnoeud):
        # Ici on créer une chaine composé des noms des colonnes des matrices barres
        A = []
        for i in range(len(listnoeud)):

            A.append("d" + str(listnoeud[i]) + "x")

            A.append("d" + str(listnoeud[i]) + "y")
        return A

def nommage_matrice_barre_lignes(listnoeud):
        # Ici on créer une chaine composé des noms des lignes des matrices barres
        A = []
        for i in range(len(listnoeud)):
            A.append("F" + str(listnoeud[i]) + "x")
            A.append("F" + str(listnoeud[i]) + "y")

        return A

def nommage_matrice_poutre_colonnes(n_noeud):
        # Ici on créer une chaine composé des noms des colonnes des matrices poutres
        A = []
        for i in range(n_noeud):
            A.append("d" + str(i+1) + "y")
            A.append("phi" +str(i+1))
        return A



def nommage_matrice_poutre_lignes(n_noeud):

        # Ici on créer une chaine composé des noms des lignes des matrices poutres
        A = []
        for i in range(n_noeud):
            A.append("F" + str(i+1) + "y")
            A.append("M" + str(i+1))
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

    print(K_final)

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
                    print(d[j][i])
                    B.append(d[j][i])
                    Tab[j][i]+= d[j][i]
                else :
                    B.append(Tab[j][i]) 
                
        Tab = pandas.DataFrame(B,index = E,columns = ["d"])
        
        return Tab
        


#pour version 2 du code (encore non utilisé)
#Pour barre/treillis
def moment_quadratique_et_aire_section_rectangle(Largeur_section,Hauteur_section):
    Aire_section=Largeur_section*Hauteur_section
    return Aire_section

def moment_quadratique_et_aire_section_cylindrique(diametre_section):
    Aire_section=pi*((diametre_section/2)**2)
    return Aire_section



############# pour les poutres

#Créer la matrice locale pour poutre

def matrice_rigidite_elementaire_poutre_1valeur_de_Longueur_poutre(Longueur_poutre,EI):   #L est la longueur entre 2 noeuds

    k=np.array([[12,6*Longueur_poutre,-12,6*Longueur_poutre],[0,4*Longueur_poutre**2,-6*Longueur_poutre,2*Longueur_poutre**2],[0,0,12,-6*Longueur_poutre],[0,0,0,4*Longueur_poutre**2]]) #matrice  sans EI/Longueur_poutre

    m=EI/Longueur_poutre              #constante devant la matrice

    k=[i*m for i in k]                #matrice rigidité finie

    return k

#fonction ajoutant 1 ligne et 1 colonne à un tableau

def ettendre_1ligne_et_1colonne(tableau):

    tableau=append(tableau,[zeros(shape(tableau)[0])],axis=0)

    tableau=append(tableau,zeros((shape(tableau)[0],1)),axis=1)

    return tableau

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

            f=matrice_rigidite_elementaire_poutre_1valeur_de_Longueur_poutre(tab[i+1]-tab[i],EI)

        else :

            f=fonction_matrice_totale_triangulairesup(f,matrice_rigidite_elementaire_poutre_1valeur_de_Longueur_poutre(tab[i+1]-tab[i],EI))

    return f



def calcul_matrice_totale(listeabscisses,EI): #ajouter la partie symétrique a la matrice de rigidité

    K_assemblee=calcul_matrice_triangulaire_sup(sorted(listeabscisses),EI)

    K_assemblee=K_assemblee+np.transpose(K_assemblee)-np.diag(np.diag(K_assemblee))

    return K_assemblee



#pour version 2 du code (encore non utilisé)
#Pour poutre
def moment_quadratique_et_aire_section_rectangle(Largeur_section,Hauteur_section):
    I=Largeur_section*(Hauteur_section**3)/12
    return IGz

def moment_quadratique_et_aire_section_cylindrique(diametre_section):
    I=pi*(diametre_section**4)/64
    return I

def dessinBarres(liste_poutre,liste_noeud,liste_noeud2):
    figure = pyplot.figure(figsize = (10, 10))
    axes = figure.add_subplot(111)
    for i in liste_poutre:
        liste_abscisses = []
        liste_ordonnee = []
        liste_abscisses.append(liste_noeud[i.Noeud_label_i-1].X)
        liste_ordonnee.append(liste_noeud[i.Noeud_label_i-1].Y)
        liste_abscisses.append(liste_noeud[i.Noeud_label_j-1].X)
        liste_ordonnee.append(liste_noeud[i.Noeud_label_j-1].Y)
        print(liste_abscisses)
        print(liste_ordonnee)
        pyplot.plot(liste_abscisses,liste_ordonnee)
        # if liste_points[i][2][0] == 0 & :
    for i in liste_poutre:
        liste_abscisses2 = []
        liste_ordonnee2 = []
        liste_abscisses2.append(liste_noeud2[i.Noeud_label_i-1].X)
        liste_ordonnee2.append(liste_noeud2[i.Noeud_label_i-1].Y)
        liste_abscisses2.append(liste_noeud2[i.Noeud_label_j-1].X)
        liste_ordonnee2.append(liste_noeud2[i.Noeud_label_j-1].Y)
        print(liste_abscisses2)
        print(liste_ordonnee2)
        pyplot.plot(liste_abscisses2,liste_ordonnee2,'r--')
        
    return liste_abscisses,liste_ordonnee,liste_abscisses2,liste_ordonnee2 
        
        
CL_d=[]
CL_f=[]
RessortSet=[]
ElementSet=[]
NoeudSet=[]

def Calculer_Barre(liste_points,liste_poutres):
    N_noeud = len(liste_points)
    for i in range(len(liste_points)):
        N = Noeud(liste_points[i][1][0], liste_points[i][1][1], liste_points[i][3][0], liste_points[i][3][1], liste_points[i][3][2])
        NoeudSet.append(N)
    print("check")
    print(i.X for i in NoeudSet)
    for i in range(len(liste_points)):
        if liste_points[i][2][0] == 0 :#Selon X
            CL_d.append("d"+str(i+1)+"x")
            CL_f.append("F"+str(i+1)+"x")

        if liste_points[i][2][1] == 0 : #Selon Y
            CL_d.append("d"+str(i+1)+"y")
            CL_f.append("F"+str(i+1)+"y")
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
        # List_noeud_save.append(Noeud_label_j)
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

    print(deplacement)
    
    for i in range(len(liste_poutres)):
         ElementSet[i].create_d_local(deplacement, N_noeud)
         ElementSet[i].create_force_axial()
    liste_abscisses = []
    liste_ordonnee = []
    NoeudSet2 = []
    for i in range(len(NoeudSet)):
        N = Noeud(NoeudSet[i].X+ float(deplacement["d"]["d"+str(i+1)+"x"]), NoeudSet[i].Y+ float(deplacement["d"]["d"+str(i+1)+"y"]), NoeudSet[i].Fx,NoeudSet[i].Fy, NoeudSet[i].Mz)
        NoeudSet2.append(N)
    dessinBarres(ElementSet,NoeudSet,NoeudSet2)
    
    del ElementSet[:]
    del NoeudSet[:]
    del NoeudSet2[:]
    del CL_d[:]
    del CL_f[:]
    del RessortSet[:]
    
    
         