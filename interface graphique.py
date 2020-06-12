# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:15:37 2020

@author: Guillaume WEBER
"""

from tkinter import * 
from tkinter import ttk

Aire_section = 0
I = 0
liste_points = ()
E = 0
liste_forces = []
liste_deplacements = []
liste_poutres = []

donnees = [Aire_section,I,liste_points,E,liste_forces,liste_deplacements]
print(donnees)

def Bouton_geometrie():
    global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    def Ajouter_point():
        liste.insert(END,(champ_point_x.get(),champ_point_y.get()))
        champ_point_x.delete(0,END)
        champ_point_y.delete(0,END)
        
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
    
    
    
def Bouton_materiaux():
    global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    temp_e=simpledialog.askfloat("Matériaux","Quel est le module de Young du matériaux de la poutre ? (Pa)")
    if not(temp_e == None):
        E=temp_e
    
def Bouton_calculer():
    # global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    print(Aire_section,I,liste_points,E,liste_forces,liste_deplacements)
    
def Bouton_contraintes():
    global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    
    def Ajouter_contraintes():
        
        if liste.curselection()!=():
            liste_forces.insert(liste.curselection()[0],[Fx.get(), Fy.get(), Mz.get()])
            

            Fx.delete(0,END)
            Fx.insert(0,'0')
            Fy.delete(0,END)
            Fy.insert(0,'0')
            Mz.delete(0,END)
            Mz.insert(0,'0')
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
    frame_force = LabelFrame(p3, text="forces :")
    Label(frame_force, text="Force selon x (N) :").grid(row=0,column=0)
    Label(frame_force, text="Force selon y (N) :").grid(row=1,column=0)
    Label(frame_force, text="Moment selon z (N) :").grid(row=2,column=0)
    Fx = Entry(frame_force)
    Fx.grid(row=0,column=1)
    Fy = Entry(frame_force)
    Fy.grid(row=1,column=1)
    Mz = Entry(frame_force)
    Mz.grid(row=2,column=1)
    frame_force.pack(fill="both", expand="yes")
    p3.add(frame_force)
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
            elif CheckY.instate(['selected']):
                liste_deplacements.insert(liste.curselection()[0],[1,1,1])

            CheckX.state(['!selected'])
            CheckY.state(['!selected'])
            CheckZ.state(['!selected'])
            liste.activate(liste.curselection()[0]+1)
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
            nouvelle_poutre = (liste.get(liste.curselection()[0]),liste.get(liste.curselection()[1]),MYoung.get())
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
    MYoung = Entry(frame2)
    MYoung.grid(row=0,column=1)
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
p2.add(Button(p2, text='Matériaux', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_materiaux))
p2.add(Button(p2, text='Conditions aux limites', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_deplacements))
p2.add(Button(p2, text='Chargements', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_contraintes))
p2.add(Button(p2, text='Poutres', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_poutres))
p2.add(Button(p2, text='Calculer', background='#4d0000', foreground='white', anchor=W, command=Bouton_calculer))

p1.add(p2)
canvas = Canvas(p1, width = 1000, height = 600, background='#ffb3b3')
p1.add(canvas)
p1.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

main_w.mainloop()


    





