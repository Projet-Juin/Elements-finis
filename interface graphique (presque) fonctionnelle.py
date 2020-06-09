# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:15:37 2020

@author: Guillaume WEBER
"""

from tkinter import * 
from tkinter import ttk
import numpy

import math

import pandas

import pandas as pd

from numpy import linalg

import numpy as np

import scipy

from scipy import *

Aire_section = 0
I = 0
liste_points = ()
E = 0
liste_forces = []
liste_deplacements = []

donnees = [Aire_section,I,liste_points,E,liste_forces,liste_deplacements]
print(donnees)

def Bouton_geometrie():
    global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    def Ajouter_point():
        liste.insert(END,float(champ_point.get()))
        champ_point.delete(0,END)
        
    def Supprimer_point():
        if liste.curselection()!=():
            liste.delete(liste.curselection())
        
    def Valider():
        global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
        if ((champ_aire.get() and champ_I.get())!='' and liste.size()>1):
            Aire_section = champ_aire.get()
            I = champ_I.get()
            liste_points = liste.get(0,END)
            fenetre_geometie.destroy()
        else:
            messagebox.showerror('Erreur','Pas de Données de Géométrie')
        
        
    fenetre_geometie = Tk()
    fenetre_geometie.geometry("380x500+90+150")
    fenetre_geometie.title('Renseigner la geométrie de la structure à étudier')
    p3 = PanedWindow(fenetre_geometie, orient=VERTICAL)
    p4 =PanedWindow(fenetre_geometie, orient=HORIZONTAL)
    p4.add(Label(p4,text='Aire de la section (m²) :'))
    champ_aire = Entry(p4)
    p4.add(champ_aire)
    p4.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
    p3.add(p4)
    p5 =PanedWindow(fenetre_geometie, orient=HORIZONTAL)
    p5.add(Label(p5,text="Moment d'inertie (m^4) :"))
    champ_I = Entry(p5)
    p5.add(champ_I)
    p5.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
    p3.add(p5)
    p6 =PanedWindow(fenetre_geometie, orient=HORIZONTAL)
    p6.add(Label(p6,text="Coordonnées du point (m) :"))
    champ_point = Entry(p6)
    p6.add(champ_point)
    liste = Listbox(p3, selectmode = SINGLE)
    p6.add(Button(p6, text='Ajouter point', command=Ajouter_point))
    p6.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
    p3.add(p6)
    p3.add(liste)
    p3.add(Button(p3, text='Supprimer point', command=Supprimer_point))
    p3.add(Button(p3, text='Valider', command=Valider))
    p3.add(Button(p3, text='Quitter', command=fenetre_geometie.destroy))
    p3.pack(side=TOP, expand=Y, fill=X, pady=2, padx=2)
    fenetre_geometie.mainloop()
    
    
    
def Bouton_materiaux():
    global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    temp_e=simpledialog.askfloat("Matériaux","Quel est le module de Young du matériaux de la poutre ? (Pa)")
    if not(temp_e == None):
        E=temp_e
    
def Bouton_calculer():
    # global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    print(Aire_section,I,liste_points,E,liste_forces,liste_deplacements)
    
    
    def matrice_rigidite_elementaire_poutre_1valeur_de_Longueur_poutre(Longueur_poutre,EI):   #L est la longueur entre 2 noeuds
    
        k=np.array([[12,6*Longueur_poutre,-12,6*Longueur_poutre],[0,4*Longueur_poutre**2,-6*Longueur_poutre,2*Longueur_poutre**2],[0,0,12,-6*Longueur_poutre],[0,0,0,4*Longueur_poutre**2]]) #matrice  sans EI/Longueur_poutre
    
        m=EI/(Longueur_poutre**3)           #constante devant la matrice
    
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
    
    
    
    EI=float(I)
    listeabscisse=list(liste_points)
    temp_d=[]
    for i in range(len(liste_deplacements)):
        for j in range(len(liste_deplacements[0])):
            temp_d.append(liste_deplacements[i][j])
    
    d_assemblee=temp_d
    
    F_assemblee=[float(i) for i in liste_forces]
    
    matricerigidite=calcul_matrice_totale(listeabscisse,EI)
    K_assemblee=matricerigidite
    
    L=[]

    for k in range(0,len(d_assemblee)):

        if d_assemblee[k]==[0]:

            L.append(k)



    L=list(reversed(L)) #inverse la liste des colonnes a supprimer

    for l in range (len(L)):

        matricerigidite=np.delete(matricerigidite, L[l], 1)

        matricerigidite=np.delete(matricerigidite, L[l], 0)


    # pour resoudre le système linéaire : a remodifié pour avoir les forces autrement que en demande au moment du choix des appuis
    print(F_assemblee)
    print(matricerigidite)
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
    
    
def Bouton_contraintes():
    global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    
    def Ajouter_contraintes():
        
        if liste.curselection()!=():
            
            
            
            liste_deplacements.insert(liste.curselection()[0],[ int(CheckY.instate(['!selected'])), int(CheckZ.instate(['!selected']))])
            if CheckY.instate(['!selected']) and CheckZ.instate(['!selected']):
                print()
            elif CheckZ.instate(['!selected']):
                liste_forces.append(float(Mz.get()))
            elif CheckY.instate(['!selected']):
                liste_forces.append(float(Fy.get()))
            else:
                liste_forces.append(float(Fy.get()))
                liste_forces.append(float(Mz.get()))
                
            Fx.delete(0,END)
            Fx.insert(0,'0')
            Fy.delete(0,END)
            Fy.insert(0,'0')
            Mz.delete(0,END)
            Mz.insert(0,'0')
            CheckX.state(['!selected'])
            CheckY.state(['!selected'])
            CheckZ.state(['!selected'])
            liste.activate(liste.curselection()[0]+1)
    
    def Valider():
        return ''
    
    fenetre_contraintes = Tk()
    fenetre_contraintes.geometry("380x500+470+150")
    fenetre_contraintes.title('Renseigner les contraintes des points de la structure à étudier')
    p3 = PanedWindow(fenetre_contraintes, orient=VERTICAL)
    p3.add(Label(p3,text="Liste des points :"))
    liste = Listbox(p3, selectmode = SINGLE)
    for i in liste_points:
        liste.insert(END, i)
    p3.add(liste)
    frame = Frame(p3)
    frame_force = LabelFrame(frame, text="forces :")
    Label(frame_force, text="Force selon x (N) :").grid(row=0,column=0)
    Label(frame_force, text="Force selon y (N) :").grid(row=1,column=0)
    Label(frame_force, text="Moment selon z (N) :").grid(row=2,column=0)
    Fx = Entry(frame_force)
    Fx.grid(row=0,column=1)
    Fy = Entry(frame_force)
    Fy.grid(row=1,column=1)
    Mz = Entry(frame_force)
    Mz.grid(row=2,column=1)
    Fx.insert(0,'0')
    Fy.insert(0,'0')
    Mz.insert(0,'0')
    frame_force.pack(side=LEFT,fill="both", expand="yes")
    frame_deplacement = LabelFrame(frame, text="déplacements :")
    CheckX = ttk.Checkbutton(frame_deplacement, text = "Bloquage selon x (m) :")
    CheckX.state(['!alternate'])
    CheckX.grid(row=0)
    CheckY = ttk.Checkbutton(frame_deplacement, text = "Bloquage selon y (m) :")
    CheckY.state(['!alternate'])
    CheckY.grid(row=1)
    CheckZ = ttk.Checkbutton(frame_deplacement, text = "Bloquage en rotation selon z (°) :")
    CheckZ.state(['!alternate'])
    CheckZ.grid(row=2)
    frame_deplacement.pack(side=RIGHT,fill="both", expand="yes")
    p3.add(frame)
    p3.add(Button(p3, text='Ajouter contraintes', command=Ajouter_contraintes))
    p3.add(Button(p3, text='Valider', command=Valider))
    p3.add(Button(p3, text='Quitter', command=fenetre_contraintes.destroy))
    p3.pack(side=TOP, expand=Y, fill=X, pady=2, padx=2)
    fenetre_contraintes.mainloop()
    
    
main_w = Tk()
main_w.geometry("1000x600")
main_w.title('Calcul de strucure par la Méthode éléments finis')

p1 = PanedWindow(main_w, orient=VERTICAL)
p2 = PanedWindow(main_w, orient=HORIZONTAL)
#crée des onglets clickables
p2.add(Button(p2, text='Géométrie', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_geometrie))
p2.add(Button(p2, text='Matériaux', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_materiaux))
p2.add(Button(p2, text='Contraintes', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_contraintes))
p2.add(Button(p2, text='Calculer', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_calculer))

p1.add(p2)
canvas = Canvas(p1, width = 1000, height = 600, background='#ffb3b3')
p1.add(canvas)
p1.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

main_w.mainloop()


    





