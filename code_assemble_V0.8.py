import numpy
import math
import pandas
import pandas as pd
from numpy import linalg
import numpy as np
import scipy
from scipy import *

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
        self.k_barre = self.Aire_section * self.E / self.Longueur_poutre
        self.C = ((NoeudSet[self.Noeud_label_j - 1].X - NoeudSet[self.Noeud_label_i - 1].X)) / self.Longueur_poutre
        self.S = ((NoeudSet[self.Noeud_label_j - 1].Y - NoeudSet[self.Noeud_label_i - 1].Y)) / self.Longueur_poutre

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
    def __init__(self, X, Y, type = "rien", Fx = 0, Fy = 0, Mz = 0):
        self.type = type
        self.X = X
        self.Y = Y
        self.Fx = Fx
        self.Fy = Fy
        self.Mz = Mz




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


def creation_K_assemble(N_noeud,list_K):

    #On commence par déterminer les noeuds qui seront dans le tableau final.

    #Par exemple pour 2 élements il y'aura 3 noeuds

    E= numpy.array([i for i in range(1,N_noeud+1)]) #On crée un tableau qui part de 1 jusqu'au nombre de noeud

    E = nommage_matrice_barre_colonnes(E) #On en fait E = ["1x","1y","2x","2y",...,"nx","ny"]

    K_final = pandas.DataFrame(0,columns = E,index = E)

    #On créer le K final. Cette table est initialement composé de 0 uniquement.

    #Avec les elements de la liste E en titre de colonne et en titre de ligne

    print(K_final)

    for i in E:

        for j in E:

            for k in list_K:

                 if i in k.K_local_barre.columns and j in k.K_local_barre.index : #Par exemple on compare

                     K_final[i][j]+= k.K_local_barre[i][j]

    return K_final



def create_F_assemble(listForce,N_noeud):

    E = nommage_matrice_barre_lignes([i for i in range(1,N_noeud+1)])
    Tab = pandas.DataFrame(listForce,index = E,columns = ['F'])

    return Tab

def create_d_assemble(d,N_Noeud):
        
        E = nommage_matrice_barre_colonnes([i for i in range(1,N_noeud+1)])
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


print("Poutre ou Treillis ?")

choix_forme = str(input())



if choix_forme=="Treillis":

################################################################if __name__ == '__main__':



    # ******************************** POUR ELEMENT BARRE **************************
    ElementSet = []
    NoeudSet = []
    List_noeud_save = []

    print("Combien d'elements? :")
    N_element = int(input())

    for i in range(N_element):

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
        print("type d'appui' (encastrement, rotule ou rien :")
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
        K_local_barre = ElementSet[i].K_local_barre
        # K_local_poutre = Ele.K_local_poutre
        print("K_local_barre={}".format(K_local_barre))
        # print("K_local_poutre={}".format(K_local_poutre))






    CL_d = [] # Contiendra les colonnes et les lignes à enlever

    CL_f = []

    for i in range(N_noeud):

        print("**************** Noeud ",i+1,"***************\n")
        print("liberté selon X")
        a = int(input())
        if a == 0 :
            CL_d.append("d"+str(i+1)+"x")
            CL_f.append("F"+str(i+1)+"x")

        print("liberté selon Y")
        a = int(input())
        if a == 0 :
            CL_d.append("d"+str(i+1)+"y")
            CL_f.append("F"+str(i+1)+"y")

    K_final = creation_K_assemble(N_noeud, ElementSet)

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
    
    for i in range(N_element):
         ElementSet[i].create_d_local(deplacement, N_noeud)
         ElementSet[i].create_force_axial()



    # ******************************** POUR ELEMENT POUTRE **************************

if choix_forme=="Poutre":



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

    matricerigidite=calcul_matrice_totale(listeabscisse,EI) # pour la suite car sera modifiee

    K_assemblee=matricerigidite #ne bougera plus


    # pour la matrice de deplacement

    F_assemblee=[]

    d_assemblee=[] #pour la matrice de deplacements : en considerant qu'il a rentré les noeuds par ordre croissant abscisses

    for i in range(N_element):

        print("***********Element n°",i+1,"**********")

        print("type d'appui' (encastrement, rotule ou rien :)")

        j = str(input()) # str : pour la chaine de caracteres

        if j=="encastrement": #dy=phi=0

            d_assemblee.append([0])

            d_assemblee.append([0])

        elif j=="rotule": #dy=0 et phi =/=0

            d_assemblee.append([0])

            d_assemblee.append([1])

            print("moment :")#IL FAUDRA VOIR POUR LES UNITES

            f = float(input())

            F_assemblee.append(f)

        elif j=="rien": #dy et phi =/=0

            d_assemblee.append([1])

            d_assemblee.append([1])

            print("force")

            f = float(input())

            F_assemblee.append(f)

            print("moment")

            f = float(input())

            F_assemblee.append(f)


    # pour supprimer tout ce qui est inutile pour calculer f dans f=K.u : en considerant qu'il a rentré les noeuds par ordre croissant abscisses

    L=[]

    for k in range(0,len(d_assemblee)):

        if d_assemblee[k]==[0]:

            L.append(k)



    L=list(reversed(L)) #inverse la liste des colonnes a supprimer

    for l in range (len(L)):

        matricerigidite=np.delete(matricerigidite, L[l], 1)

        matricerigidite=np.delete(matricerigidite, L[l], 0)


    # pour resoudre le système linéaire : a remodifié pour avoir les forces autrement que en demande au moment du choix des appuis

    deplacementinconnu=linalg.solve(matricerigidite,F_assemblee)


    # pour afficher tous les déplacements :

    i=0

    for p in range(len(d_assemblee)) :

        if d_assemblee[p]==[1]:

            d_assemblee[p]=[deplacementinconnu[i]]

            i=i+1

    # pour afficher la matrice force



    F_assemblee=np.dot(K_assemblee,d_assemblee)



    #pour passer en dataframes
    print("***matrice rigidité assemblée : ")
    matrice_assemblee=pd.DataFrame(K_assemblee,index=nommage_matrice_poutre_colonnes(int(np.shape(K_assemblee)[0]-(np.shape(K_assemblee)[0]/2))) ,columns=nommage_matrice_poutre_colonnes(int(np.shape(K_assemblee)[0]-(np.shape(K_assemblee)[0]/2))))
    print(matrice_assemblee)
    print("***matrice déplacements")
    d_assemblee=pd.DataFrame(d_assemblee,index=nommage_matrice_poutre_colonnes(int(np.shape(d_assemblee)[0]-(np.shape(d_assemblee)[0]/2))) ,columns=['deplacement'])
    print(d_assemblee)
    print("***matrice forces")
    F_assemblee=pd.DataFrame(F_assemblee,index=nommage_matrice_poutre_lignes(int(np.shape(F_assemblee)[0]-(np.shape(F_assemblee)[0]/2))),columns=['force'])
    print(F_assemblee)