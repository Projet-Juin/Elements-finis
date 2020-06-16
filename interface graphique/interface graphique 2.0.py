# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 17:48:31 2020

@author: Guillaume WEBER
"""

import tkinter as tk
from tkinter import ttk

def main():
    global liste_noeuds
    main_w = tk.Tk() # crée la fenêtre principale
    main_w.geometry("750x750+0+8") # dimentions dimXxdimY+écartAuBordX+écartAuBordY
    main_w.title('Calcul de strucure par la Méthode éléments finis') # titre
    
    Liste_listboxNoeuds = []
    
    ongletsModele = ttk.Notebook(main_w) # crée une barre d'onglet
    framePoutre = tk.Frame(ongletsModele) # crée un cadre
    ongletsModele.add(framePoutre) # l'ajoute dans un onglet de la barre d'onglet
    ongletsModele.tab(0, text="Modèle Poutre") # nomme cet onglet 
    frameBarre = tk.Frame(ongletsModele) # même chose pour l'onglet 2
    ongletsModele.add(frameBarre)
    ongletsModele.tab(1, text="Modèle Barre/Treillis")
    ongletsEtape = ttk.Notebook(ongletsModele)
    PanedwindowPortique = ttk.Panedwindow(ongletsEtape, orient="horizontal")
    
    if True or 'Inputs': # juste pour structurer le programme
        
        ongletsInput = ttk.Notebook(PanedwindowPortique)
        frameNoeud = tk.Frame(ongletsInput)
        
        if True or 'Noeuds':
            Noeud_rouge = tk.PhotoImage(file="Noeud_rouge.gif").subsample(9,9)
            Noeud_vert = tk.PhotoImage(file="Noeud_vert.gif").subsample(7,7)
            
            def AjouterNoeub(evt):
                AjouterNoeud()
            def AjouterNoeud():
                global liste_noeuds
                if Xnoeud.get()!='' and Ynoeud.get()!='' and Znoeud.get()!='':
                    temp_noeud=(float(Xnoeud.get()),float(Ynoeud.get()),float(Znoeud.get()))
                    absent = True
                    for i in liste_noeuds:
                        if i[1]==temp_noeud:
                            absent = False
                    if absent:
                        liste_noeuds.append(['Nœud'+str(len(liste_noeuds)+1),temp_noeud,None,None,None])
                        listboxNoeud_update(len(liste_noeuds)-1)
                        Xnoeud.focus()
                        Xnoeud.select_range(0,tk.END)
                    else:
                        tk.messagebox.showerror('Erreur', 'Ce nœud existe déjà, il ne peut pas être ajouté.')
                else:
                    tk.messagebox.showerror('Erreur', 'Un champ de coordonnées est vide.')
            
            def listboxNoeud_update(index):
                for i in Liste_listboxNoeuds:
                    i.delete(index)
                if Liste_listboxNoeuds[0].size()!=len(liste_noeuds):
                    for i in Liste_listboxNoeuds:
                        i.insert(index,liste_noeuds[index][0]+" "+str(liste_noeuds[index][1]))
                if len(liste_noeuds)<2:
                    ongletsInput.tab(0, image = Noeud_rouge, compound=tk.LEFT)
                else:
                    ongletsInput.tab(0, image = Noeud_vert, compound=tk.LEFT)
                
            def SupprimerNoeud():
                if Liste_listboxNoeuds[0].curselection()!=():
                    del liste_noeuds[Liste_listboxNoeuds[0].curselection()[0]]
                    listboxNoeud_update(Liste_listboxNoeuds[0].curselection()[0])
                else:
                    tk.messagebox.showerror('Erreur', 'Aucun nœud sélectionné.')
            
            def RenommerNoeud():
                if Liste_listboxNoeuds[0].curselection()!=():
                    
                    temp_nom_noeud=tk.simpledialog.askstring("Renommer nœud", 'Nouveau nom du nœud : "'+Liste_listboxNoeuds[0].get(Liste_listboxNoeuds[0].curselection()[0])+'" :')
                    if temp_nom_noeud!='':
                        liste_noeuds[Liste_listboxNoeuds[0].curselection()[0]][0] = temp_nom_noeud
                        listboxNoeud_update(Liste_listboxNoeuds[0].curselection()[0])
                else:
                    tk.messagebox.showerror('Erreur', 'Aucun nœud sélectionné.')
            
            tk.Label(frameNoeud, text='Ajouter des nœuds :').grid(row=0)
            tk.Label(frameNoeud, text='Position selon X (m) :').grid(row=1)
            tk.Label(frameNoeud, text='Position selon Y (m) :').grid(row=3)
            tk.Label(frameNoeud, text='Position selon Z (m) :').grid(row=5)
            Xnoeud = tk.Entry(frameNoeud)
            Xnoeud.grid(row=2)
            Ynoeud = tk.Entry(frameNoeud)
            Ynoeud.grid(row=4)
            Znoeud = tk.Entry(frameNoeud)
            Znoeud.grid(row=6)
            def Xnoeud_next(evt):
                Ynoeud.focus()
                Ynoeud.select_range(0,tk.END)
            def Ynoeud_next(evt):
                Znoeud.focus()
                Znoeud.select_range(0,tk.END)
            Xnoeud.bind('<Return>', Xnoeud_next)
            Ynoeud.bind('<Return>', Ynoeud_next)
            Znoeud.bind('<Return>', AjouterNoeub)
            tk.Button(frameNoeud, text='Ajouter nœud', command=AjouterNoeud).grid(row=7)
            Liste_listboxNoeuds.append(tk.Listbox(frameNoeud, selectmode=tk.SINGLE))
            Liste_listboxNoeuds[0].grid(row=8)
            tk.Button(frameNoeud, text='Renommer nœud', command=RenommerNoeud).grid(row=11)
            tk.Button(frameNoeud, text='Supprimer nœud', command=SupprimerNoeud).grid(row=12)
            
        ongletsInput.add(frameNoeud)
        ongletsInput.tab(0, text='Nœuds',image=Noeud_rouge, compound=tk.LEFT)
        frameChargements = tk.Frame(ongletsInput)
        
        if True or 'Chargements / Degrés de liberté':
            Fleche_rouge = tk.PhotoImage(file="fleche_rouge.png").subsample(18,18)
            Fleche_verte = tk.PhotoImage(file="fleche_verte.png").subsample(13,13)
            
            def choix_liaison(evt):
                if Combobox.current()>=0:
                    update_deg_liberte(ListeLibertes[Combobox.current()])
                    Combobox.set('')
                
            def update_deg_liberte(libertes):
                for i in range(len(libertes)):
                    ListeCheck[i].state([('' if libertes[i] else '!')+'selected'])
            
            def appliquer_chargements():
                global liste_noeuds
                if Liste_listboxNoeuds[1].curselection()!=():
                    selectd_index= Liste_listboxNoeuds[1].curselection()[0]
                    plein = True
                    for i in range(6):
                        try:
                            float(listeEntry[i].get())
                        except ValueError:
                            listeEntry[i].focus()
                            listeEntry[i].select_range(0,tk.END)
                            plein = False
                    for i in range(3):
                        try:
                            float(listeEntryR[i].get())
                        except ValueError:
                            listeEntryR[i].focus()
                            listeEntryR[i].select_range(0,tk.END)
                            plein = False
                            
                    if plein:
                        # degrés de liberté
                        liste_noeuds[selectd_index][2] = [int(ListeCheck[i].instate(['!selected'])) for i in range(5)]
                        # liste_noeuds[Liste_listboxNoeuds[1].curselection()[0]][2] = [int(ListeCheck[0].instate(['!selected'])),int(ListeCheck[1].instate(['!selected'])),int(ListeCheck[2].instate(['!selected'])),int(ListeCheck[3].instate(['!selected'])),int(ListeCheck[4].instate(['!selected'])),int(ListeCheck[5].instate(['!selected']))]
                        # forces et moments
                        liste_noeuds[selectd_index][3] = [float(listeEntry[0].get()), float(listeEntry[1].get()), float(listeEntry[2].get()), float(listeEntry[3].get()), float(listeEntry[4].get()), float(listeEntry[5].get())]
                        # ressort
                        liste_noeuds[selectd_index][4] = [float(listeEntryR[0].get()), float(listeEntryR[1].get()), float(listeEntryR[2].get())]
                        
                        for i in listeEntry:
                            i.delete(0,tk.END)
                            i.insert(0,'0')
                        Liste_listboxNoeuds[1].focus()
                        Liste_listboxNoeuds[1].activate(Liste_listboxNoeuds[1].curselection()[0]+1)
                    else:
                        tk.messagebox.showerror('Erreur', 'Une donnée ne peut pas être interprétée comme float')
                else:
                    tk.messagebox.showerror('Erreur', 'Pas de nœud sélectionné')
            
            tk.Label(frameChargements, text='Définir les propriétés des nœuds :').grid(row=0) 
            tk.Label(frameChargements, text='Choix du nœud :').grid(row=1)
            Liste_listboxNoeuds.append(tk.Listbox(frameChargements, selectmode=tk.SINGLE))
            Liste_listboxNoeuds[1].grid(row=2)
            
            frameDeplacements = tk.LabelFrame(frameChargements, text='Degrés de liberté du nœud')
            frameDeplacements.grid(row=3)
            ListeCheck = []
            ListeCheck.append(ttk.Checkbutton(frameDeplacements, text = "Bloquage selon X"))
            ListeCheck.append(ttk.Checkbutton(frameDeplacements, text = "Bloquage selon Y"))
            ListeCheck.append(ttk.Checkbutton(frameDeplacements, text = "Bloquage selon Z"))
            ListeCheck.append(ttk.Checkbutton(frameDeplacements, text = "Bloquage en rotation selon X"))
            ListeCheck.append(ttk.Checkbutton(frameDeplacements, text = "Bloquage en rotation selon Y"))
            ListeCheck.append(ttk.Checkbutton(frameDeplacements, text = "Bloquage en rotation selon Z"))
            for i in range(len(ListeCheck)):
                ListeCheck[i].state(['!alternate'])
                ListeCheck[i].grid(row=i%3, column = i//3)
            tk.Label(frameDeplacements, text = 'liaisons standard :').grid(row=3, column = 0,sticky=tk.E)
            Listeliaisons = ['Encastrement','Rotule','Libre']
            ListeLibertes = [(1,1,1,1,1,1),(1,1,1,0,0,0),(0,0,0,0,0,0)]
            Combobox = ttk.Combobox(frameDeplacements,values = Listeliaisons)
            Combobox.grid(row=3, column = 1,sticky=tk.W)
            Combobox.bind('<<ComboboxSelected>>',choix_liaison)
            
            frameForce = tk.LabelFrame(frameChargements, text = 'Chargements du nœud')
            frameForce.grid(row=4)
            listeEntry = []
            tk.Label(frameForce, text = 'Force selon X (N) :').grid(row=0, column = 0)
            tk.Label(frameForce, text = 'Force selon Y (N) :').grid(row=1, column = 0)
            tk.Label(frameForce, text = 'Force selon Z (N) :').grid(row=2, column = 0)
            tk.Label(frameForce, text = 'Moment selon X (N.m) :').grid(row=3, column = 0)
            tk.Label(frameForce, text = 'Moment selon Y (N.m) :').grid(row=4, column = 0)
            tk.Label(frameForce, text = 'Moment selon Z (N.m) :').grid(row=5, column = 0)
            def next_Force(evt, index):
                if index==5:
                    listeEntryR[0].focus()
                    listeEntryR[0].select_range(0,tk.END)
                else:
                    listeEntry[index+1].focus()
                    listeEntry[index+1].select_range(0,tk.END)
                    
            for i in range(6):
                listeEntry.append(tk.Entry(frameForce))
                listeEntry[i].insert(0,'0')
                listeEntry[i].grid(row=i, column = 1)
                listeEntry[i].bind('<Return>', lambda evt, index=i:next_Force(evt,index))
            
            frameRessort = tk.LabelFrame(frameChargements, text = 'Ressort du nœud')
            frameRessort.grid(row=5)
            listeEntryR = []
            tk.Label(frameRessort, text = 'Ressort selon X (N/m) :').grid(row=0, column = 0) # ajouter ressort en torsion ?
            tk.Label(frameRessort, text = 'Ressort selon Y (N/m) :').grid(row=1, column = 0)
            tk.Label(frameRessort, text = 'Ressort selon Z (N/m) :').grid(row=2, column = 0)
            def next_Ressort(evt, index):
                if index==2:
                    appliquer_chargements()
                else:
                    listeEntryR[index+1].focus()
                    listeEntryR[index+1].select_range(0,tk.END)
            for i in range(3):
                listeEntryR.append(tk.Entry(frameRessort))
                listeEntryR[i].insert(0,'0')
                listeEntryR[i].grid(row=i, column = 1)
                listeEntryR[i].bind('<Return>', lambda evt, index=i:next_Ressort(evt,index))
            
            tk.Button(frameChargements, text = 'Appliquer les propriétés au nœud', command = appliquer_chargements).grid(row= 6)
            
        ongletsInput.add(frameChargements)
        ongletsInput.tab(1, text='Propriétés des nœuds',image=Fleche_rouge, compound=tk.LEFT)
            
            
            
    PanedwindowPortique.add(ongletsInput)
    PanedwindowPortique.add(tk.Canvas(PanedwindowPortique))
    PanedwindowPortique.sashpos(0, 7000)
    ongletsEtape.add(PanedwindowPortique)
    ongletsEtape.tab(0, text="Données d'entrée")
    ongletsModele.add(ongletsEtape)
    ongletsModele.tab(2, text="Modèle Portique")
    
    
    
    ongletsModele.pack(side=tk.LEFT, expand = tk.Y, fill = tk.BOTH)
    main_w.mainloop()






liste_noeuds=[]
main()
