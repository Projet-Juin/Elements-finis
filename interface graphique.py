# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 14:15:37 2020

@author: Guillaume WEBER
"""

from tkinter import * 


def Bouton_geometrie():
    
    def Ajouter_point():
        liste.insert(END,champ_point.get())
        champ_point.delete(0,END)
        champ_point.insert(0, 'point ajouté!')
        
    def Supprimer_point():
        liste.delete(liste.curselection())
        
    def Valider():
        if ((champ_aire.get() and champ_I.get())!='' and liste.size()>1):
            return (TRUE, champ_aire.get(),champ_I.get(), liste.get(0,END))
        
        
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
    liste = Listbox(p3)
    p6.add(Button(p6, text='Ajouter point', command=Ajouter_point))
    p6.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
    p3.add(p6)
    p3.add(liste)
    p3.add(Button(p3, text='Supprimer point', command=Supprimer_point))
    bouton_valider = Button(p3, text='Valider', command=Valider)
    p3.add(bouton_valider)
    p3.add(Button(p3, text='Quitter', command=fenetre_geometie.quit))
    p3.pack(side=TOP, expand=Y, fill=X, pady=2, padx=2)
    fenetre_geometie.mainloop()
    
    if bouton_valider.invoke()[0]:
        return bouton_valider.invoke()[1:]
    
    
def Bouton_materiaux():
    Module_Young = simpledialog.askfloat("Matériaux","Quel est le module de Young du matériaux de la poutre ?")
    
    
def Bouton_calculer():
    if bouton_geometrie.invoke()==NONE:
        messagebox.showshowerror('Erreur','Pas de Données de Géométrie')
    
    
    
    
main_w = Tk()
main_w.geometry("1000x600")
main_w.title('Calcul de strucure par la Méthode éléments finis')

p1 = PanedWindow(main_w, orient=VERTICAL)
p2 = PanedWindow(main_w, orient=HORIZONTAL)
#crée des onglets clickables
bouton_geometrie = Button(p2, text='Géométrie', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_geometrie)
p2.add(bouton_geometrie)
p2.add(Button(p2, text='Matériaux', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_materiaux))
p2.add(Button(p2, text='Contraintes', background='#4d0000', foreground='white', anchor=CENTER))
p2.add(Button(p2, text='Calculer', background='#4d0000', foreground='white', anchor=CENTER, command=Bouton_calculer))

p1.add(p2)
canvas = Canvas(p1, width = 1000, height = 600, background='#ffb3b3')
p1.add(canvas)
p1.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)

main_w.mainloop()


    





