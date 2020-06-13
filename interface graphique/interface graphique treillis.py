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
liste_poutres = []

def Bouton_geometrie():
    global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    def Ajouter_point():
        liste.insert(END,(float(champ_point_x.get()),float(champ_point_y.get())))
        champ_point_x.delete(0,END)
        champ_point_y.delete(0,END)
        
    def Supprimer_point():
        if liste.curselection()!=():
            liste.delete(liste.curselection())
        
    def Valider():
        global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
        if (liste.size()>1):
            liste_points = liste.get(0,END)
            fenetre_geometie.destroy()
        else:
            messagebox.showerror('Erreur','Pas de Données de Géométrie')
        
        
    fenetre_geometie = Tk()
    fenetre_geometie.geometry("450x500+90+150")
    fenetre_geometie.title('Renseigner la geométrie de la structure à étudier')
    p3 = PanedWindow(fenetre_geometie, orient=VERTICAL)
    p6 =PanedWindow(fenetre_geometie, orient=HORIZONTAL)
    p6.add(Label(p6,text="Coordonnées du point (m) :"))
    champ_point_x = Entry(p6)
    champ_point_y = Entry(p6)
    p6.add(champ_point_x)
    p6.add(champ_point_y)
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
    
    
def Bouton_calculer():
    # global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    print(liste_points,liste_forces,liste_deplacements, liste_poutres)
    
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
            B[0][0] = c
            B[0][1] = s
            B[1][2] = c
            B[1][3] = s
            
            d = self.deplacement_local.to_numpy()
            self.force_axe = self.k_barre * numpy.mat(A) * numpy.mat(B) * numpy.mat(d)
            
        
                
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
        
    CL_d=[]
    CL_f=[]
    RessortSet=[]
    ElementSet=[]
    NoeudSet=[]
    
    N_noeud = len(liste_points)
    
    for i in range(len(liste_points)):
        N = Noeud(liste_points[i][0], liste_points[i][1], liste_forces[i][0], liste_forces[i][1], liste_forces[i][2])
        NoeudSet.append(N)
     
    for i in range(len(liste_points)):
        if liste_deplacements[i][0] == 0 :
            CL_d.append("d"+str(i+1)+"x")
            CL_f.append("F"+str(i+1)+"x")

        if liste_deplacements[i][1] == 0 :
            CL_d.append("d"+str(i+1)+"y")
            CL_f.append("F"+str(i+1)+"y")
            
        axe = ["d"+str(i+1)+"x","d"+str(i+1)+"y"]
        a = liste_forces[i][3]
        b = liste_forces[i][4]
        resistance = pandas.DataFrame([[a,0],[0,b]],columns = axe,index = axe)
        ressort = Ressort([i+1],resistance)
        RessortSet.append(ressort)
            
    for i in range(len(liste_poutres)):
        Aire_section = liste_poutres[i][3]
        Noeud_label_i = liste_poutres[i][0]
        Noeud_label_j = liste_poutres[i][1]
        List_noeud = []
        List_noeud.append(Noeud_label_i)
        List_noeud.append(Noeud_label_j)
        # List_noeud_save.append(Noeud_label_i)
        # List_noeud_save.append(Noeud_label_j)
        E = liste_poutres[i][2]
        
        #Création d'objets
        Ele = Element(List_noeud = List_noeud, Aire_section = Aire_section, E = E)
        ElementSet.append(Ele)
        
        ElementSet[i].__calcule__()
        
        # K_local_poutre = Ele.K_local_poutre
        
        
        
    K_final = creation_K_assemble(N_noeud, ElementSet,RessortSet)

    K_assemble = K_final
    
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
    
    for i in range(len(liste_poutres)):
         ElementSet[i].create_d_local(deplacement, N_noeud)
         ElementSet[i].create_force_axial()
         print("Matrice force : " ,ElementSet[i].force_axe )
        
def Bouton_contraintes():
    global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    
    def Ajouter_contraintes():
        
        if liste.curselection()!=():
            liste_forces.insert(liste.curselection()[0],[float(Fx.get()), float(Fy.get()), float(Mz.get()), float(Rx.get()), float(Ry.get())])
            Fx.delete(0,END)
            Fx.insert(0,'0')
            Fy.delete(0,END)
            Fy.insert(0,'0')
            Mz.delete(0,END)
            Mz.insert(0,'0')
            Rx.delete(0,END)
            Rx.insert(0,'0')
            Ry.delete(0,END)
            Ry.insert(0,'0')
            # liste.activate(liste.curselection()[0]+1)
    
    def Valider():
        return ''
    
    fenetre_contraintes = Tk()
    fenetre_contraintes.geometry("450x500+470+150")
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
    Mz = Entry(frame_force, )
    Mz.grid(row=2,column=1)
    frame_force.pack(side = LEFT,fill="both", expand="yes")
    frame_ressort = LabelFrame(frame, text="forces :")
    Label(frame_ressort, text="Ressort selon x (N) :").grid(row=0,column=0)
    Label(frame_ressort, text="Force selon y (N) :").grid(row=1,column=0)
    Rx = Entry(frame_ressort)
    Rx.grid(row=0,column=1)
    Ry = Entry(frame_ressort)
    Ry.grid(row=1,column=1)
    frame_ressort.pack(side = RIGHT,fill="both", expand="yes")
    p3.add(frame)
    Fx.delete(0,END)
    Fx.insert(0,'0')
    Fy.delete(0,END)
    Fy.insert(0,'0')
    Mz.delete(0,END)
    Mz.insert(0,'0')
    Rx.delete(0,END)
    Rx.insert(0,'0')
    Ry.delete(0,END)
    Ry.insert(0,'0')
    p3.add(Button(p3, text='Ajouter contraintes', command=Ajouter_contraintes))
    p3.add(Button(p3, text='Valider', command=Valider))
    p3.add(Button(p3, text='Quitter', command=fenetre_contraintes.destroy))
    p3.pack(side=TOP, expand=Y, fill=X, pady=2, padx=2)
    fenetre_contraintes.mainloop()


def Bouton_deplacements():
    global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    
    def Ajouter_contraintes():
        
        if liste.curselection()!=():
            
            if CheckX.instate(['selected']):
                liste_deplacements.insert(liste.curselection()[0],[0,0,0])
            elif CheckY.instate(['selected']):
                liste_deplacements.insert(liste.curselection()[0],[0,0,1])
            elif CheckZ.instate(['selected']):
                liste_deplacements.insert(liste.curselection()[0],[1,1,1])

            CheckX.state(['!selected'])
            CheckY.state(['!selected'])
            CheckZ.state(['!selected'])
            # liste.activate(liste.curselection()[0]+1)
        else:
            messagebox.showerror ('Erreur', 'pas de point sélectionné')
    
    fenetre_contraintes = Tk()
    fenetre_contraintes.geometry("380x500+470+150")
    fenetre_contraintes.title('Renseigner les forces des points de la structure à étudier')
    p3 = PanedWindow(fenetre_contraintes, orient=VERTICAL)
    p3.add(Label(p3,text="Liste des points :"))
    liste = Listbox(p3, selectmode = SINGLE)
    for i in liste_points:
        liste.insert(END, i)
    p3.add(liste)
    frame = Frame(p3)
    CheckX = ttk.Checkbutton(frame, text = "liaison encastrement", command=Ajouter_contraintes)
    CheckX.state(['!alternate'])
    CheckX.grid(row=0)
    CheckY = ttk.Checkbutton(frame, text = "liaison rotule", command=Ajouter_contraintes)
    CheckY.state(['!alternate'])
    CheckY.grid(row=1)
    CheckZ = ttk.Checkbutton(frame, text = "point libre", command=Ajouter_contraintes)
    CheckZ.state(['!alternate'])
    CheckZ.grid(row=2)
    p3.add(frame)
    p3.add(Button(p3, text='Quitter', command=fenetre_contraintes.destroy))
    p3.pack(side=TOP, expand=Y, fill=X, pady=2, padx=2)
    fenetre_contraintes.mainloop()

def Bouton_poutres():
    global Aire_section,I,liste_points,E,liste_forces,liste_deplacements,liste_poutres
    
    def Ajouter_poutre():
        
        if len(liste.curselection())==2 and MYoung.get()!='':
            nouvelle_poutre = (liste.curselection()[0]+1,liste.curselection()[1]+1, float(MYoung.get()),float(Apoutre.get()))
            absent = TRUE
            for i in liste_poutres:
                if i[0:2]==nouvelle_poutre[0:2]:
                    absent = FALSE
            if absent:
                liste_poutres.append(nouvelle_poutre)
                listepoutre.insert(END, nouvelle_poutre)
            else:
                messagebox.showerror('Erreur', 'poutre déjà existante')
        else:
            messagebox.showerror('Erreur', 'pas assez de point sélectionné')
    
    fenetre_contraintes = Tk()
    fenetre_contraintes.geometry("380x500+470+150")
    fenetre_contraintes.title('Renseigner les forces des points de la structure à étudier')
    p3 = PanedWindow(fenetre_contraintes, orient=VERTICAL)
    p3.add(Label(p3,text="Liste des points :"))
    liste = Listbox(p3, selectmode = MULTIPLE)
    liste.pack(side=LEFT, expand=Y, fill=BOTH)
    for i in liste_points:
        liste.insert(END, i)
    p3.add(liste)
    frame2 = Frame(p3)
    Label(frame2, text="Module de Young de la poutre (Pa) :").grid(row=0,column=0)
    Label(frame2, text="Aire de la section de la poutre (m²) :").grid(row=1,column=0)
    MYoung = Entry(frame2)
    MYoung.grid(row=0,column=1)
    Apoutre = Entry(frame2)
    Apoutre.grid(row=1,column=1)
    p3.add(frame2)
    p3.add(Button(p3, text='Ajouter poutres', command=Ajouter_poutre))
    listepoutre = Listbox(p3, selectmode = SINGLE)
    p3.add(listepoutre)
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
p2.add(Button(p2, text='Conditions aux limites', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_deplacements))
p2.add(Button(p2, text='Chargements', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_contraintes))
p2.add(Button(p2, text='Poutres', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_poutres))
p2.add(Button(p2, text='Calculer', background='#4d0000', foreground='white', anchor=W, command=Bouton_calculer))

p1.add(p2)
canvas = Canvas(p1, width = 1000, height = 600, background='#ffb3b3')
p1.add(canvas)
p1.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

main_w.mainloop()


    





