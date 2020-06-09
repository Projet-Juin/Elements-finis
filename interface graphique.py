# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:15:37 2020

@author: Guillaume WEBER
"""

from tkinter import * 

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
        liste.insert(END,champ_point.get())
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
    E=(simpledialog.askfloat("Matériaux","Quel est le module de Young du matériaux de la poutre ? (Pa)"))
    
def Bouton_calculer():
    # global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    print(Aire_section,I,liste_points,E,liste_forces,liste_deplacements)
    # if donnees==():
    #     messagebox.showerror('Erreur','Pas de Données de Géométrie')
    
def Bouton_contraintes():
    global Aire_section,I,liste_points,E,liste_forces,liste_deplacements
    def Ajouter_contraintes():
        if liste.curselection()!=():
            liste_forces.insert(liste.curselection()[0],[Fx.get(), Fy.get(), Mz.get()])
            liste_deplacements.insert(liste.curselection()[0],[DeplacementX.get(), DeplacementY.get(), DeplacementZ.get()])
            
    
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
    frame_force.pack(side=LEFT,fill="both", expand="yes")
    frame_deplacement = LabelFrame(frame, text="déplacements :")
    DeplacementX = IntVar()
    DeplacementY = IntVar()
    DeplacementZ = IntVar()
    Checkbutton(frame_deplacement, variable= DeplacementX, text = "Bloquage selon x (m) :").grid(row=0)
    Checkbutton(frame_deplacement, variable= DeplacementY, text = "Bloquage selon y (m) :").grid(row=1)
    Checkbutton(frame_deplacement, variable= DeplacementZ, text = "Bloquage en rotation selon z (°) :").grid(row=2)
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
bouton_geometrie = Button(p2, text='Géométrie', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_geometrie)
p2.add(bouton_geometrie)
p2.add(Button(p2, text='Matériaux', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_materiaux))
p2.add(Button(p2, text='Contraintes', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_contraintes))
p2.add(Button(p2, text='Calculer', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_calculer))

p1.add(p2)
canvas = Canvas(p1, width = 1000, height = 600, background='#ffb3b3')
p1.add(canvas)
p1.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

main_w.mainloop()


    





