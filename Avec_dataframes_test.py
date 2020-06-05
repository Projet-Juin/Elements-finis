# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 18:30:18 2020

@author: Lansana Diomande
"""
import pandas as pd
import numpy as np


def  CreateMatrix(C, S, K,A):
    #Creation de la matrice K pour un element en fonction du cosinus , du sinus et de (A*E/L)
        kk = np.array([[0 for i in range(4)] for i in range(4)])
        kk[0][0] = C ** 2 * K
        kk[2][2] = C ** 2 * K
        kk[1][1] = S ** 2 * K
        kk[3][3] = S ** 2 * K
        kk[0][1] = C*S * K
        kk[1][0] = C*S * K
        kk[2][3] = C*S * K
        kk[3][2] = C*S * K
        kk[0][2] = - C ** 2 * K
        kk[2][0] = - C ** 2 * K
        kk[1][3] = - S ** 2 * K
        kk[3][1] = - S ** 2 * K
        kk[0][3] = - C*S * K
        kk[1][2] = - C*S * K
        kk[2][1] = - C*S * K
        kk[3][0] = - C*S * K
        
            #La matrice est créer
        A = nommage(A) #On créer une liste comme ["1x","1y","2x","2y"] ou ["1x","1y","3x","3y"] etc...
        
        kk=pd.DataFrame(kk,columns = A,index = A) #on titre les colonnes et les lignes 
        
        return kk
    
def  nommage(listnoeud):
    #Ici on créer une chaine composé des noms des colonnes et lignes des tableaux 
    #a partir des numéros de noeuds d'un élément
    #exemple: ["1x","1y","2x","2y",...,"nx","ny"]
     A=[]
    
     for i in range(len(listnoeud)):
         A.append(str(listnoeud[i])+"x")
         A.append(str(listnoeud[i])+"y")
     
     return A
 
def creation_Tabfinal(N_noeud):
    #On commence par déterminer les noeuds qui seront dans le tableau final.
    #Par exemple pour 2 élements il y'aura 3 noeuds
    E= np.array([i for i in range(1,N_noeud+1)]) #On crée un tableau qui part de 1 jusqu'au nombre de noeud
    E = nommage(E) #On en fait E = ["1x","1y","2x","2y",...,"nx","ny"]
    Tabfinal = pd.DataFrame(0,columns = E,index = E) 
    #On créer le K final. Cette table est initialement composé de 0 uniquement.
    #Avec les elements de la liste E en titre de colonne et en titre de ligne
    return Tabfinal



##############   Le code se lance ici ##########################

print("Combien d'elements? :")

N_element = int(input())
List_K=[]
list_noeud = [] #Cette liste va gader les numéros de noeuds pour chaque 
# élément mais elle sera supprimer à chaque tour de boucle
list_noeud_sans_virer = [] # Cette liste va garder les numéros de noeuds pour tout les elements
# elle servira a compter le nombre de noeud en tout et servira pour créer la matrice K final

for i in range(N_element):
    del list_noeud[:]
    print("***********Element n°",i+1,"**********")
    print("Valeur de C :")
    C = float(input()) #Récupération du cosinus de l'angle par rapport à l'axe x
    print("Valeur de S :")
    S= float(input())  #Récupération du sinus de l'angle par rapport à l'axe x
    print("Valeur de k (A*E/L) :")
    k= float(input())
    print("Numero du 1er noeud :")
    a=int(input())
    list_noeud.append(a)
    list_noeud_sans_virer.append(a)
    
    print("Numero du 2eme noeud :")
    b=int(input())
    list_noeud.append(b)
    list_noeud_sans_virer.append(b)
    
    K= CreateMatrix(C,S,k,list_noeud) #Creation de la matrice pour la barre i
    
    List_K.append(K) #Ajout de la matrice de la barre i dans la liste des creations
    

N_noeud =len(list(set(list_noeud_sans_virer))) #Ici on retire les doublons de 
#list_noeud_sans_virer et determine le nombre de noeud en faisant +1 à la taille de la liste sans doublon
print(N_noeud)
Tabfinal = creation_Tabfinal(N_noeud)#Creation de la table final
E= np.array([i for i in range(1,N_noeud+1)]) #On crée un tableau qui part de 1 jusqu'au nombre de noeud
E = nommage(E) #On en fait E = ["1x","1y","2x","2y",...,"nx","ny"]
    
for i in E:
    for j in E:
        for k in List_K:
            if i in k.columns and j in k.index : #Par exemple on compare 
                Tabfinal[i][j]+= k[i][j]
                
# Dans les boucles precedentes on fouille le tableau final et 
# On somme les cases du tableau final avec les éléments des matrices K 
# lorsqu'ils ont le même nom de colonne et le même nom de ligne

        
 
print(Tabfinal)
      







