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

from matplotlib import patches

import matplotlib.pyplot as pyplot


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

def etendre_la_matrice_abscisse(listeabscisse,nombrepointsentre2noeuds):
    liste_abscisse_allongee=[]
    for k in range(len(listeabscisse)-1):
        pas=calcul_du_pas(listeabscisse[k+1]-listeabscisse[k],nombrepointsentre2noeuds+1)
        liste_abscisse_allongee.append(listeabscisse[k])
        for i in range (1,nombrepointsentre2noeuds+1):
            liste_abscisse_allongee.append(pas*i+listeabscisse[k])
    liste_abscisse_allongee.append(listeabscisse[-1])
    return liste_abscisse_allongee


def supprimer_valeurs_inutiles_dans_matrice_forces(liste_abscisse_allongee,listeabscisse,F_assemblee,d_assemblee):
    M=[]

    for k in range (0,len(d_assemblee),1):
        if d_assemblee[k][0]!=0:
            print(d_assemblee[k])
            M.append(F_assemblee[k])
    F_assemblee=M
    return F_assemblee


def supprimer_inutil_dans_matricerigidite(d_assemblee,matricerigidite):
    L=[]
    for k in range(0,len(d_assemblee)):
        if d_assemblee[k]==[0]:
            L.append(k)
    L=list(reversed(L)) #inverse la liste des colonnes a supprimer
    for l in range (len(L)):
        matricerigidite=np.delete(matricerigidite, L[l], 1)
        matricerigidite=np.delete(matricerigidite, L[l], 0)
    return matricerigidite
    #print(matricerigidite)

def mettre_tous_les_deplacements_en_1matrice(d_assemblee,deplacementinconnu):
    i=0
    for p in range(len(d_assemblee)) :

        if d_assemblee[p]==[1]:
            d_assemblee[p]=[deplacementinconnu[i]]
            i=i+1
    return d_assemblee


def fonction_listedebutchargerepartie_allongee(listedebutchargerepartie,nombrepointsentre2noeuds):
    listedebutchargerepartie_allongee=[]
    for k in range (len(listedebutchargerepartie)):
        listedebutchargerepartie_allongee.append(listedebutchargerepartie[k])
        for i in range (nombrepointsentre2noeuds):
            listedebutchargerepartie_allongee.append(0)
    #listedebutchargerepartie_allongee.append(0)
    return listedebutchargerepartie_allongee


def fonction_listeressort_allongee(listeressort,nombrepointsentre2noeuds):
    listeressort_allongee=[]
    for k in range (len(listeressort)-1):
        listeressort_allongee.append([listeressort[k]])
        for i in range (nombrepointsentre2noeuds):
            listeressort_allongee.append([0,0])
    listeressort_allongee.append([listeressort[k]])
    return listeressort_allongee

def fonction_liste_force_allongee(liste_force,nombrepointsentre2noeuds):
    liste_force_allongee=[]
    for k in range (len(liste_force)-1):
        liste_force_allongee.append(liste_force[k])
        for i in range (nombrepointsentre2noeuds):
            liste_force_allongee.append([0,0])
    liste_force_allongee.append(liste_force[-1])
    return liste_force_allongee



# N_element=3

# listeabscisse=[1,4,7]

# nombrepointsentre2noeuds=1

# I=0.0004

# E=210000000

# type_appui=['encastrement','rien','encastrement']

# listedebutchargerepartie=[0,0]

# listeressort=[0,0,0]

# liste_force=[[0,0],[10,0],[0,0]]

def liste_des_demandes_utilisateur(N_element,listeabscisse,nombrepointsentre2noeuds,I,E,type_appui,listedebutchargerepartie,listeressort,liste_force):
    """
    N_element:nombre de noeuds
    listeabscisse :liste des abscisses des noeuds
    section : type de la section etudiée : cylindre,rectangle ou I
    E : Valeur de E
    type_appui : liste des appuis, exemple : ["encastrement","rien","rotule","encastrement"] : noeud1, noeud2, noeud3, noeud4
    liste_force : exemple : [[0,0],[125,625],[0,236],[0,0]] : force noeud1, moment noeud1, force noeud2, moment noeud2, ...
    listedebutchargerepartie : [0,256,0,0] : noeud1, noeud2, noeud3, noeud4 : s'arete au N_element-1
    listeressort : dans sous-ligne:constanteraideur,longueurressort] exemple: [[0,0],[566,2],[0,0],[0,0] : mettre des zeros si pas de ressort
    
    """
    
    
    liste_abscisse_allongee=etendre_la_matrice_abscisse(listeabscisse,nombrepointsentre2noeuds)
    
    
    N_element_allongee=len(liste_abscisse_allongee)
    listedebutchargerepartie_allongee=[]
    listedebutchargerepartie_allongee=fonction_listedebutchargerepartie_allongee(listedebutchargerepartie,nombrepointsentre2noeuds)
    listeressort_allongee=[]
    listeressort_allongee=fonction_listeressort_allongee(listeressort,nombrepointsentre2noeuds)
    
    liste_force_allongee=[]
    liste_force_allongee=fonction_liste_force_allongee(liste_force,nombrepointsentre2noeuds)
    
    
    
    F_assemblee=[0 for i in range(2*N_element_allongee)] #va servir pour le systeme matrice colonne de 0 de taille 2*N_element : a remodifier pour que ca fonctionne
    d_assemblee=[] #pour la matrice de deplacements : en considerant qu'il a rentré les noeuds par ordre croissant abscisses
    
    F_pour_dessin=[]
    
    for i in range(N_element_allongee-1):
        if liste_abscisse_allongee[i] in listeabscisse :
            p=listeabscisse.index(liste_abscisse_allongee[i])
            j=type_appui[p]
            if j=="encastrement": #dy=phi=0
                d_assemblee.append([0])
                d_assemblee.append([0])
                charge=0
                F_pour_dessin.append(0)
                F_pour_dessin.append(0)
                if not listedebutchargerepartie_allongee[i]==0:
                    charge = listedebutchargerepartie_allongee[i]
                    if liste_abscisse_allongee[i+1] in listeabscisse :
                        pp=listeabscisse.index(liste_abscisse_allongee[i+1])
                        z=type_appui[pp]
    
                        if z=="encastrement": #dy=phi=0
                            print()
                        if z=="rotule":
                            F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
    
                        if z=="rien":
                            F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                            F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                    else :
                         F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                         F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
    
            if j=="rotule": #dy=0 et phi =/=0
                charge=0
                d_assemblee.append([0])
                d_assemblee.append([1])
                f=liste_force_allongee[i][1]
                F_pour_dessin.append(0)
                F_pour_dessin.append(f)
                F_assemblee[i*2+1]+=f
                if not listedebutchargerepartie_allongee[i]==0:
                    charge = listedebutchargerepartie_allongee[i]
                    F_assemblee[i*2+1]+=moment_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
    
                    if liste_abscisse_allongee[i+1] in listeabscisse :
                        pp=listeabscisse.index(liste_abscisse_allongee[i+1])
                        z=type_appui[pp]
                        if z=="encastrement": #dy=phi=0
                            print()
    
                        if z=="rotule":
                            F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
    
                        if z=="rien":
                            F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                            F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                    else :
                         F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                         F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                
            if j=="rien":
    
                charge=0
                if not listeressort_allongee[i][0]==0:
                    longueur_ressort=listeressort_allongee[i][1]
                    listeressort_allongee[i][0]
                    valeurforce_ressort=force_ressort(listeressort_allongee[i][0],longueur_ressort)
                    F_assemblee[i*2]+=valeurforce_ressort
                d_assemblee.append([1])
                d_assemblee.append([1])
                f=liste_force_allongee[i][0]
                F_assemblee[i*2]+=f
                F_pour_dessin.append(f)
                f=liste_force_allongee[i][1]
                F_assemblee[i*2]+=f
                F_pour_dessin.append(f)
                print(F_assemblee)
    
                if not listedebutchargerepartie_allongee[i]==0:
                    charge = listedebutchargerepartie_allongee[i]
                    F_assemblee[i*2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                    F_assemblee[i*2+1]+=moment_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                    if liste_abscisse_allongee[i+1] in listeabscisse :
                        pp=listeabscisse.index(liste_abscisse_allongee[i+1])
                        z=type_appui[pp]
                        if z=="encastrement": #dy=phi=0
                            print()
    
                        if z=="rotule":
                            F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
    
                        if z=="rien":
                            F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                            F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                    else :
                            F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                            F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                    
        else :
                d_assemblee.append([1])
                d_assemblee.append([1])
                F_assemblee[i*2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                if liste_abscisse_allongee[i+1] in listeabscisse :
                    pp=listeabscisse.index(liste_abscisse_allongee[i+1])
                    z=type_appui[pp]
                    if z=="encastrement": #dy=phi=0
                        print()
                    if z=="rotule":
                        F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
    
                    if z=="rien":
                        F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                        F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
    
                else :
                    F_assemblee[i*2+2]+=force_charge_uniformement_repartie(charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
                    F_assemblee[i*2+3]+=moment_charge_uniformement_repartie(-charge,liste_abscisse_allongee[i+1]-liste_abscisse_allongee[i])
    
    j=type_appui[-1] # str : pour la chaine de caracteres
    if j=="encastrement": #dy=phi=0
        d_assemblee.append([0])
        d_assemblee.append([0])
        F_pour_dessin.append(0)
        F_pour_dessin.append(0)
    if j=="rotule": #dy=0 et phi =/=0
        d_assemblee.append([0])
        d_assemblee.append([1])
        f=liste_force_allongee[-1][1]
        F_assemblee[-1]+=f
        F_pour_dessin.append(0)
        F_pour_dessin.append(f)
    if j=="rien": #dy et phi =/=0
        if not listeressort_allongee[i][0]==0:
            longueur_ressort=listeressort_allongee[i][1]
            listeressort_allongee[i][0]
            valeurforce_ressort=force_ressort(listeressort_allongee[i][0],longueur_ressort)
            F_assemblee[i*2]+=valeurforce_ressort
        d_assemblee.append([1])
        d_assemblee.append([1])
        f=liste_force_allongee[-1][0]
        F_pour_dessin.append(f)
        F_assemblee[-2]+=f
        f=liste_force_allongee[-1][1]
        F_assemblee[-1]+=f
        F_pour_dessin.append(f)
    
    """
    ########################### pour le dessin 
    
    liste_ordonnee=[]
    for k in range(len(listeabscisse)):
        liste_ordonnee.append(0)
    figure = pyplot.figure(figsize = (10, 10))
    axes = figure.add_subplot(111)
    
    pyplot.plot(listeabscisse, liste_ordonnee, color='r', linestyle=':', marker='o')
    
    for k in range(len(listeabscisse)):
        if type_appui[k]=='encastrement':
            pyplot.scatter(listeabscisse[k], liste_ordonnee[k]-0.0002, s = 1000, c = 'g', marker = 's', edgecolors = 'b',label="encastrement")
    
        if type_appui[k]=="rotule":
            pyplot.scatter(listeabscisse[k], liste_ordonnee[k]-0.0002, s = 1000, c = 'g', marker = '^', edgecolors = 'b',label="rotule")
    
        if type_appui[k]=="rien":
            pyplot.scatter(listeabscisse[k], liste_ordonnee[k]-0.0002, s = 1000, c = 'g', marker = 'o', edgecolors = 'b',label="appui simple")
    
        if not F_pour_dessin[2*k]==0:
            pyplot.annotate('        ', xy=(listeabscisse[k], liste_ordonnee[k]),xycoords='data',xytext=(0.12, 1), textcoords='axes fraction',arrowprops=dict(facecolor='black', shrink=0.5),horizontalalignment='right', verticalalignment='top',)
        if not F_pour_dessin[2*k+1]==0:
           pyplot.annotate('        ',xy=(listeabscisse[k]+0.5, liste_ordonnee[k]-0.0003), xycoords='data', xytext=(-70,30), textcoords='offset points',arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=10,angleB=90,rad=20"),fontsize=10)
    pyplot.ylim(-0.25, 1.5)
    pyplot.legend()
    pyplot.show()
    
    """
    
    
    EI=E*I
    
    matricerigidite=calcul_matrice_totale(liste_abscisse_allongee,EI) # pour la suite car sera modifiee
    
    K_assemblee=matricerigidite #ne bougera plus
    
    #calcul de la matrice des forces a utiliser dans le systeme a resoudre
    M=[]
    for k in range (0,len(d_assemblee),1):
        if d_assemblee[k][0]!=0:
            M.append(F_assemblee[k])
    F_assemblee=M
    
    F_assemblee=np.asarray(F_assemblee).reshape(len(F_assemblee),1) #convertir la ligne en matrice colonne array
    
    
    #calcul de la matrice de rigidité a utiliser dans le systeme a resoudre
    L=[]
    for k in range(0,len(d_assemblee)):
        if d_assemblee[k]==[0]:
            L.append(k)
    L=list(reversed(L)) #inverse la liste des colonnes a supprimer
    
    for l in range (len(L)):
        matricerigidite=np.delete(matricerigidite, L[l], 1)
        matricerigidite=np.delete(matricerigidite, L[l], 0)
    
    
    
    
    #resolution systeme et obtention deplacements inconnus
    
    deplacementinconnu=linalg.solve(matricerigidite,F_assemblee)
    
    
    # pour afficher tous les déplacements :
    i=0
    for p in range(len(d_assemblee)) :
        if d_assemblee[p]==[1]:
            d_assemblee[p]=deplacementinconnu[i] #.tolist()
            i=i+1
    
    
    #♣calcul de la matrice des forces externes
    F_assemblee=np.dot(K_assemblee,d_assemblee) ##########################"on enleve ?
    
    
    
    #pour passer en dataframes
    print("***matrice rigidité assemblée : ")
    matrice_assemblee=pd.DataFrame(K_assemblee,index=nommage_matrice_poutre_colonnes(int(np.shape(K_assemblee)[0]-(np.shape(K_assemblee)[0]/2))) ,columns=nommage_matrice_poutre_colonnes(int(np.shape(K_assemblee)[0]-(np.shape(K_assemblee)[0]/2))))
    print(matrice_assemblee)
    print("***matrice déplacements")
    d_assemblee=pd.DataFrame(d_assemblee,index=nommage_matrice_poutre_colonnes(int(np.shape(d_assemblee)[0]-(np.shape(d_assemblee)[0]/2))) ,columns=['deplacement'])
    print(d_assemblee)
    
    
    d_assemblee_liste = d_assemblee['deplacement'].values.tolist()
    
    
    deplacement_y=[]
    deplacement_phi=[]
    
    for k in range(int(len(d_assemblee_liste)/2)):
        deplacement_y.append(d_assemblee_liste[2*k])
        deplacement_phi.append(d_assemblee_liste[2*k+1])
    
    ### calcul des forces internes
    forces_internes=[]
    force_internes_totales=[]
    d_pour_internes=[]
    liste_abscisse_allongee_pour_forces_internes=[] 
    
    #en calculant les forces internes théoriquement on se rend compte que aux noeuds, si la longueur entre 2 noeuds n'est pas la même sur la même poutre alors les forces internes calculées ne sont pas les mêmes sur les 2 systemes prenant en commpte un même vrai noeud.
    #on va donc représenter toutes les forces calculées pour les vrais noeuds (non maillage),
    
    rigidite_pour_internes=matrice_rigidite_elementaire_poutre_1valeur_de_Longueur_poutre(liste_abscisse_allongee[1]-liste_abscisse_allongee[0],EI)
    rigidite_pour_internes=rigidite_pour_internes+np.transpose(rigidite_pour_internes)-np.diag(np.diag(rigidite_pour_internes))
    d_pour_internes.append(d_assemblee_liste[0])
    d_pour_internes.append(d_assemblee_liste[1])
    d_pour_internes.append(d_assemblee_liste[2])
    d_pour_internes.append(d_assemblee_liste[3])
    forces_internes=np.dot(rigidite_pour_internes,d_pour_internes)
    force_internes_totales.append(-forces_internes[0])
    force_internes_totales.append(-forces_internes[1])
    force_internes_totales.append(forces_internes[2])
    force_internes_totales.append(forces_internes[3])
    liste_abscisse_allongee_pour_forces_internes.append(liste_abscisse_allongee[0])
    liste_abscisse_allongee_pour_forces_internes.append(liste_abscisse_allongee[1])
    for k in range(1,len(liste_abscisse_allongee)-1):
        d_pour_internes=[]
        rigidite_pour_internes=matrice_rigidite_elementaire_poutre_1valeur_de_Longueur_poutre(liste_abscisse_allongee[k+1]-liste_abscisse_allongee[k],EI)
        rigidite_pour_internes=rigidite_pour_internes+np.transpose(rigidite_pour_internes)-np.diag(np.diag(rigidite_pour_internes))
        d_pour_internes.append(d_assemblee_liste[2*k])
        d_pour_internes.append(d_assemblee_liste[2*k+1])
        d_pour_internes.append(d_assemblee_liste[2*k+2])
        d_pour_internes.append(d_assemblee_liste[2*k+3])
        forces_internes=np.dot(rigidite_pour_internes,d_pour_internes)
        if liste_abscisse_allongee[k] in listeabscisse :
            liste_abscisse_allongee_pour_forces_internes.append(liste_abscisse_allongee[k])
            force_internes_totales.append(-forces_internes[0])
            force_internes_totales.append(-forces_internes[1])
        force_internes_totales.append(forces_internes[2])
        force_internes_totales.append(forces_internes[3])
        liste_abscisse_allongee_pour_forces_internes.append(liste_abscisse_allongee[k+1])

    
    print("force_internes_totales")
    print(force_internes_totales)
    
    """
    plt.plot(liste_abscisse_allongee, deplacement_y)
    plt.plot(liste_abscisse_allongee, deplacement_phi)
    plt.grid()
    plt.legend(["deplacement y","deplacement phi"])
    plt.show()
    """
    
    
    effort_tranchant=[]
    moment=[]
    
    for k in range(len(liste_abscisse_allongee_pour_forces_internes)):
        effort_tranchant.append(force_internes_totales[2*k])
        moment.append(force_internes_totales[2*k+1])
    
    """
    plt.plot(liste_abscisse_allongee_pour_forces_internes, effort_tranchant)
    plt.grid()
    plt.legend(["effort tranchant"])
    plt.show()
    plt.plot(liste_abscisse_allongee_pour_forces_internes, moment)
    plt.grid()
    plt.legend(["moment fléchissant"])
    plt.show()
    #print("***matrice forces externes")
    #F_assemblee=pd.DataFrame(F_assemblee,index=nommage_matrice_poutre_lignes(int(np.shape(F_assemblee)[0]-(np.shape(F_assemblee)[0]/2))),columns=['force'])
    #print(F_assemblee)

    """

###########################"modifié a partir d'ici pour ce qui est à retourner
    
    deg_point=[]
    for k in type_appui:
        if k=="encastrement":
            deg_point.append((0,0,0))
        if k=="rotule":
            deg_point.append((1,1,0))            
        if k=="rien":
            deg_point.append((1,1,1))
            
            #listeabscisse, poutre, liste_abscisse_allongee, d_assemblee_liste, effort_tranchant, moment sont des listes

    
    poutre=[0 for i in range(len(listeabscisse))] #toujours 0 en ordonnées , 
    
    graph1=["déplacement en m",[listeabscisse,poutre,'b'],[liste_abscisse_allongee,deplacement_y,'r--']]
    graph2=["déplacement rotationnel en m",[listeabscisse,poutre,'b',[deg_point]],[liste_abscisse_allongee,deplacement_phi,'r--']]
    
    graph3=["effort tranchant en N",[listeabscisse,poutre,'b',[deg_point],],[liste_abscisse_allongee_pour_forces_internes,effort_tranchant,'r--']]
            
    graph4=["moment fléchissant en N.m",[listeabscisse,poutre,'b',[deg_point]],[liste_abscisse_allongee_pour_forces_internes,moment,'r--']]
    
    
    #graph4=[dessin poutre????????]
    
    liste_des_graphs=[graph1,graph2,graph3,graph4]
    
    print(liste_des_graphs)
    
    return liste_des_graphs
