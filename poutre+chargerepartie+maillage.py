# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 13:33:09 2020

@author: ombline delassus
"""


import numpy
import math
import matplotlib.pyplot as plt
import pandas
import pandas as pd
from numpy import linalg
import numpy as np
import scipy
from scipy import *
from mpl_toolkits.mplot3d import Axes3D



############# pour les poutres

#Créer la matrice locale pour poutre

def matrice_rigidite_elementaire_poutre_1valeur_de_Longueur_poutre(Longueur_poutre,EI):   #L est la longueur entre 2 noeuds

    k=np.array([[12,6*Longueur_poutre,-12,6*Longueur_poutre],[0,4*Longueur_poutre**2,-6*Longueur_poutre,2*Longueur_poutre**2],[0,0,12,-6*Longueur_poutre],[0,0,0,4*Longueur_poutre**2]]) #matrice  sans EI/Longueur_poutre

    m=EI/(Longueur_poutre**3)              #constante devant la matrice

    k=[i*m for i in k]                #matrice rigidité finie

    return k

#fonction ajoutant 1 ligne et 1 colonne à un tableau

def ettendre_1ligne_et_1colonne(tableau):

    tableau=append(tableau,[zeros(shape(tableau)[0])],axis=0)

    tableau=append(tableau,zeros((shape(tableau)[0],1)),axis=1)

    return tableau


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

#######################################################"" A SUPPRIMER
def charge_uniformement_repartie (force,longueur_section):
    M=force*(longueur_section**2)/12
    return M
####################################################### A AJOUTER
def moment_charge_uniformement_repartie (force,longueur_section):
    M_reparti=force*(longueur_section**2)/12
    return M_reparti

def force_charge_uniformement_repartie (force,longueur_section):
    F_repartie=force*longueur_section/2
    return F_repartie




def moment_quadratique_section_rectangle(Largeur_section,Hauteur_section):
    I=Largeur_section*(Hauteur_section**3)/12    #################formules a verifier
    return I

def moment_quadratique_section_cylindrique(diametre_section):
    I=pi*(diametre_section**4)/64
    return I

def moment_quadratique_section_I(Largeur_section,Hauteur_section,epaisseur_partiecentrale,epaisseur_rebords):
    I=((Largeur_section*(Hauteur_section**3))-((Largeur_section-epaisseur_partiecentrale)*((Hauteur_section-2*epaisseur_rebords)**3)))/12
    return I


def calcul_du_pas(distance_entre_2_noeuds,nombrepointsentre2noeuds):
    longueur_du_pas=distance_entre_2_noeuds/nombrepointsentre2noeuds
    return longueur_du_pas


def force_ressort(constante_de_raideur,longueur_ressort):
    valeur_force_ressort=-constante_de_raideur*longueur_ressort
    return valeur_force_ressort



print("Combien d'elements? :")                              #nombre de noeuds sur la poutre

N_element = int(input())

listeabscisse=[]

for i in range(N_element):

    print("***********Element n°",i+1,"**********")

    print("Valeur du noeud :")

    j = float(input())                                      #Récupération des différentes valeurs des abscisses des noeuds

    listeabscisse.append(j)
    
    
liste_abscisse_allongee=[]
for k in range(len(listeabscisse)-1):
    nombrepointsentre2noeuds=50 #######################a modifier si choix de l'utilisateur
    pas=calcul_du_pas(listeabscisse[k+1]-listeabscisse[k],nombrepointsentre2noeuds)
    liste_abscisse_allongee.append(listeabscisse[k])
    for i in range (1,nombrepointsentre2noeuds):
        liste_abscisse_allongee.append(pas*i+listeabscisse[k])
liste_abscisse_allongee.append(listeabscisse[-1])
 
    
    
print("Valeur de E :")
E= float(input())

print("type de section étudiée ? (rectangle ou cylindre ou I )")
section = str(input())
if section =="cylindre" :
    print("Valeur du diamètre de la section :")
    diametresection = float(input()) 
    I=moment_quadratique_section_cylindrique(diametresection)

if section =="rectangle":
    print("Valeur de la largeur de la section :")
    Largeur_section = float(input()) 
    print("Valeur de la hauteur de la section :")
    Hauteur_section = float(input())     
    I=moment_quadratique_section_rectangle(Largeur_section,Hauteur_section)

if section=="I":
    print ("Valeur de la largeur de la section :")
    Largeur_section = float(input()) 
    print("Valeur de la hauteur de la section :")
    Hauteur_section = float(input())  
    print("Valeur de l'epaisseur de la partie centrale :")
    epaisseur_partiecentrale = float(input()) 
    print("Valeur de l'epaisseur des rebords :")
    epaisseur_rebords = float(input())  
    I=moment_quadratique_section_I(Largeur_section,Hauteur_section,epaisseur_partiecentrale,epaisseur_rebords)

    
#print("Valeur de I :")
#I= float(input())

EI=E*I

matricerigidite=calcul_matrice_totale(liste_abscisse_allongee,EI) # pour la suite car sera modifiee

K_assemblee=matricerigidite #ne bougera plus



type_appui=[]

for i in range(N_element):

    print("***********Element n°",i+1,"**********")    
    print("type d'appui (encastrement, rotule ou rien :)")
    j = str(input()) # str : pour la chaine de caracteres
    type_appui.append(j)


N_element_allongee=len(liste_abscisse_allongee)

F_repartie=[0 for i in range(2*N_element_allongee)] #va servir pour forces réparties : matrice colonne de 0 de taille 2*N_element : a remodifier pour que ca fonctionne

F_assemblee=[0 for i in range(2*N_element_allongee)] #va servir pour le systeme matrice colonne de 0 de taille 2*N_element : a remodifier pour que ca fonctionne

d_assemblee=[] #pour la matrice de deplacements : en considerant qu'il a rentré les noeuds par ordre croissant abscisses



for i in range(N_element_allongee-1):
    if liste_abscisse_allongee[i] in listeabscisse :
        p=listeabscisse.index(liste_abscisse_allongee[i])   
        print("***********Element n°",p+1,"**********")
        
        j=type_appui[p]
    
        if j=="encastrement": #dy=phi=0
            d_assemblee.append([0])
            d_assemblee.append([0])
            print("début de charge répartie ? (oui ou non)")
            chargepossible = str(input())
            if chargepossible=='oui':
                print("charge :")
                charge = float(input())
                F_repartie[i*2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                F_repartie[i*2+1]+=moment_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                if liste_abscisse_allongee[i+1] in listeabscisse :
                    pp=listeabscisse.index(liste_abscisse_allongee[i+1])
                    z=type_appui[pp]
        
                    if z=="encastrement": #dy=phi=0
                        F_repartie[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                        F_repartie[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
        
                    if z=="rotule":
                        ressort=0
                        print("ressort ? (oui ou non)")
                        ressort = str(input())
                        if ressort=='oui':
                            print("longueur_ressort")
                            longueur_ressort=float(input())
                            print("constante_de_raideur")
                            constante_de_raideur=float(input())
                            force_ressort=force_ressort(constante_de_raideur,longueur_ressort)
                        F_repartie[i*2+2]+=force_ressort
                        F_repartie[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                        F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
        
                    if z=="rien":   
                        F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                        F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i]) 
                else :
                     F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])

                 
        if j=="rotule": #dy=0 et phi =/=0
            d_assemblee.append([0])
            d_assemblee.append([1])
            print("moment :")#IL FAUDRA VOIR POUR LES UNITES
            f = float(input())
            F_assemblee[i*2+1]+=f        
            print("début de charge répartie ? (oui ou non")
            chargepossible = str(input())
    
            if chargepossible=='oui':
                print("charge :")
                charge = float(input())
                F_repartie[i]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                F_assemblee[i*2+1]+=moment_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])

                if liste_abscisse_allongee[i+1] in listeabscisse :
                    pp=listeabscisse.index(liste_abscisse_allongee[i+1])
                    z=type_appui[pp]
                    if z=="encastrement": #dy=phi=0
                        F_repartie[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                        F_repartie[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])  
        
                    if z=="rotule":    
                        F_repartie[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                        F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
        
                    if z=="rien":      
                        F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                        F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i]) 
                else :
                     F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                                   
        if j=="rien":   
            print("ressort ? (oui ou non)")
            ressort = str(input())
            if ressort=='oui':
                print("longueur_ressort")
                longueur_ressort=float(input())
                print("constante_de_raideur")
                constante_de_raideur=float(input())
                valeur_force_ressort=force_ressort(constante_de_raideur,longueur_ressort)
                F_repartie[i*2]+=valeur_force_ressort
            d_assemblee.append([1])
            d_assemblee.append([1])
            print("force")
            f = float(input())
            F_assemblee[i*2]+=f #+F_repartie[i]
            print("moment")
            f = float(input())
            F_assemblee[i*2]+=f#+F_repartie[i]
            print("début de charge répartie ? (oui ou non")
            chargepossible = str(input())
    
            if chargepossible=='oui':
                print("charge :")
                charge = float(input())
                F_assemblee[i*2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                F_assemblee[i*2+1]+=moment_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                if liste_abscisse_allongee[i+1] in listeabscisse :
                    pp=listeabscisse.index(liste_abscisse_allongee[i+1])
                    z=type_appui[pp]
                    if z=="encastrement": #dy=phi=0
                        F_repartie[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                        F_repartie[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])  
        
                    if z=="rotule":    
                        F_repartie[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                        F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
        
                    if z=="rien":   
                        F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                        F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                else :
                        F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                        
    else : 
            d_assemblee.append([1])
            d_assemblee.append([1])
            F_assemblee[i*2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])     
            
            if liste_abscisse_allongee[i+1] in listeabscisse :
               #print("liste_abscisse_allongee[i+1]")
                #print(liste_abscisse_allongee[i+1])
                #print(i)
                pp=listeabscisse.index(liste_abscisse_allongee[i+1])
                z=type_appui[pp]
                if z=="encastrement": #dy=phi=0
                    F_repartie[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                    F_repartie[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])  
    
                if z=="rotule":    
                    F_repartie[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                    F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
    
                if z=="rien":   
                    F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                    F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
         
            else : 
                F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                
        
print("***********Element n°",N_element,"**********")    #faire le cas du N_element    

j=type_appui[-1] # str : pour la chaine de caracteres
if j=="encastrement": #dy=phi=0
    d_assemblee.append([0])
    d_assemblee.append([0])
    
if j=="rotule": #dy=0 et phi =/=0
    d_assemblee.append([0])
    d_assemblee.append([1])
    print("moment :")#IL FAUDRA VOIR POUR LES UNITES
    f = float(input())
    F_assemblee[-1]+=f

if j=="rien": #dy et phi =/=0
    ressort=0
    print("ressort ? (oui ou non)")
    ressort = str(input())
    if ressort=='oui':
        print("longueur_ressort")
        longueur_ressort=float(input())
        print("constante_de_raideur")
        constante_de_raideur=float(input())
        force_ressort=force_ressort(constante_de_raideur,longueur_ressort)
        F_repartie[i*2]+=force_ressort
    d_assemblee.append([1])
    d_assemblee.append([1])
    print("force")
    f = float(input())
    F_assemblee[-2]+=f 
    print("moment")
    f = float(input())
    F_assemblee[-1]+=f                



for k in range (len(liste_abscisse_allongee)): #permet de supprimer tous les zeros de la liste utilisée pour le systeme
    if liste_abscisse_allongee[k] in listeabscisse :
        p=liste_abscisse_allongee.index(liste_abscisse_allongee[k])   #recuperer lindice dans liste_abscisse_allongee de la valeur a supprimer
        del F_assemblee[p]


F_assemblee=np.asarray(F_assemblee).reshape(len(F_assemblee),1) #convertir la ligne en matrice colonne array
F_repartie=np.asarray(F_repartie).reshape(len(F_repartie),1)               


# pour supprimer tout ce qui est inutile pour calculer f dans f=K.u : en considerant qu'il a rentré les noeuds par ordre croissant abscisses

L=[]
for k in range(0,len(d_assemblee)):
    if d_assemblee[k]==[0]:
        L.append(k)

L=list(reversed(L)) #inverse la liste des colonnes a supprimer

for l in range (len(L)):
    matricerigidite=np.delete(matricerigidite, L[l], 1)
    matricerigidite=np.delete(matricerigidite, L[l], 0)
    #print(matricerigidite)

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
#print(shape(F_assemblee))

#print(F_assemblee)
#print(F_repartie)
#pour passer en dataframes
print("***matrice rigidité assemblée : ")
matrice_assemblee=pd.DataFrame(K_assemblee,index=nommage_matrice_poutre_colonnes(int(np.shape(K_assemblee)[0]-(np.shape(K_assemblee)[0]/2))) ,columns=nommage_matrice_poutre_colonnes(int(np.shape(K_assemblee)[0]-(np.shape(K_assemblee)[0]/2))))
print(matrice_assemblee)
print("***matrice déplacements")
d_assemblee=pd.DataFrame(d_assemblee,index=nommage_matrice_poutre_colonnes(int(np.shape(d_assemblee)[0]-(np.shape(d_assemblee)[0]/2))) ,columns=['deplacement'])
print(d_assemblee)

F_assemble=F_assemblee+F_repartie


effort_tranchant=[]
moment=[]
for k in range(len(liste_abscisse_allongee)):
    effort_tranchant.append(F_assemble[2*k][0])
    moment.append(F_assemble[2*k+1][0])


#plt.plot(liste_abscisse_allongee, effort_tranchant)
#plt.grid() 
#plt.show()
#plt.plot(liste_abscisse_allongee, moment)
#plt.grid() 
#plt.show()

ax = Axes3D(plt.figure()) 
ax.plot(moment, effort_tranchant, liste_abscisse_allongee) 
plt.show()



print("***matrice forces")
F_assemble=pd.DataFrame(F_assemble,index=nommage_matrice_poutre_lignes(int(np.shape(F_assemble)[0]-(np.shape(F_assemble)[0]/2))),columns=['force'])
print(F_assemble)