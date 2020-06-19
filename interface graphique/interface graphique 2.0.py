# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 17:48:31 2020

@author: Guillaume WEBER
"""

import tkinter as tk
from tkinter import ttk
# from pour_portique-2 import Calculer

def main():
    global liste_noeuds, liste_poutres
    main_w = tk.Tk() # crée la fenêtre principale
    main_w.geometry("750x750+0+8") # dimentions dimXxdimY+écartAuBordX+écartAuBordY
    main_w.title('Calcul de strucure par la Méthode éléments finis') # titre
    
    Liste_listboxNoeuds = []
    Liste_listboxPoutres = []
    Liste_listboxNoeudsP = []
    Liste_listboxPoutresP = []
    
    ongletsModele = ttk.Notebook(main_w) # crée une barre d'onglet
    
    
    ongletsEtapePoutre = ttk.Notebook(ongletsModele)
    PanedwindowPoutre = ttk.Panedwindow(ongletsEtapePoutre, orient=tk.HORIZONTAL) # même chose pour l'onglet 2
    
    if True or 'Inputs': # juste pour structurer le programme
        
        ongletsInputPoutre = ttk.Notebook(PanedwindowPoutre)
        frameNoeudP = tk.Frame(ongletsInputPoutre)
        
        if True or 'Noeuds':
            Noeud_rouge = tk.PhotoImage(file="Noeud_rouge.gif").subsample(9,9)
            Noeud_vert = tk.PhotoImage(file="Noeud_vert.gif").subsample(7,7)
            
            def AjouterNoeubP(evt):
                AjouterNoeudP()
            def AjouterNoeudP():
                plein = True
                try:
                    float(XnoeudP.get())
                    float(YnoeudP.get())
                    float(ZnoeudP.get())
                except ValueError:
                    plein = False
                if plein:
                    temp_noeud=(float(XnoeudP.get()),float(YnoeudP.get()),float(ZnoeudP.get()))
                    absent = True
                    for i in liste_noeuds:
                        if i[1]==temp_noeud:
                            absent = False
                            break
                    if absent:
                        liste_noeuds.append(['Nœud '+str(len(liste_noeuds)+1),temp_noeud,None,None,None])
                        listboxNoeud_updateP(len(liste_noeuds)-1)
                        XnoeudP.focus()
                        XnoeudP.select_range(0,tk.END)
                    else:
                        tk.messagebox.showerror('Erreur', 'Ce nœud existe déjà, il ne peut pas être ajouté.')
                else:
                    tk.messagebox.showerror('Erreur', 'Un champ de coordonnées ne peut pas être interprété comme float')
            
            def listboxNoeud_updateP(index):
                for i in Liste_listboxNoeudsP:
                    i.delete(index)
                if Liste_listboxNoeudsP[0].size()!=len(liste_noeuds):
                    for i in Liste_listboxNoeudsP:
                        i.insert(index,liste_noeuds[index][0]+" "+str(liste_noeuds[index][1]))
                Liste_listboxNoeudsP[0].see(index)
                if len(liste_noeuds)<2:
                    ongletsInputPoutre.tab(0, image = Noeud_rouge, compound=tk.LEFT)
                else:
                    ongletsInputPoutre.tab(0, image = Noeud_vert, compound=tk.LEFT)
                
            def SupprimerNoeudP():
                if Liste_listboxNoeudsP[0].curselection()!=():
                    del liste_noeuds[Liste_listboxNoeudsP[0].curselection()[0]]
                    listboxNoeud_updateP(Liste_listboxNoeudsP[0].curselection()[0])
                else:
                    tk.messagebox.showerror('Erreur', 'Aucun nœud sélectionné.')
            
            def RenommerNoeudP():
                if Liste_listboxNoeudsP[0].curselection()!=():
                    temp_nom_noeud=tk.simpledialog.askstring("Renommer nœud", 'Nouveau nom du nœud : "'+Liste_listboxNoeuds[0].get(Liste_listboxNoeuds[0].curselection()[0])+'" :')
                    if temp_nom_noeud!='':
                        liste_noeuds[Liste_listboxNoeudsP[0].curselection()[0]][0] = temp_nom_noeud
                        listboxNoeud_updateP(Liste_listboxNoeudsP[0].curselection()[0])
                else:
                    tk.messagebox.showerror('Erreur', 'Aucun nœud sélectionné.')
            
            tk.Label(frameNoeudP, text='Ajouter des nœuds :').grid(row=0)
            tk.Label(frameNoeudP, text='Position selon X (m) :').grid(row=1)
            tk.Label(frameNoeudP, text='Position selon Y (m) :').grid(row=3)
            tk.Label(frameNoeudP, text='Position selon Z (m) :').grid(row=5)
            XnoeudP = tk.Entry(frameNoeudP)
            XnoeudP.grid(row=2)
            YnoeudP = tk.Entry(frameNoeudP)
            YnoeudP.grid(row=4)
            ZnoeudP = tk.Entry(frameNoeudP)
            ZnoeudP.grid(row=6)
            def Xnoeud_nextP(evt):
                YnoeudP.focus()
                YnoeudP.select_range(0,tk.END)
            def Ynoeud_nextP(evt):
                ZnoeudP.focus()
                ZnoeudP.select_range(0,tk.END)
            XnoeudP.bind('<Return>', Xnoeud_nextP)
            YnoeudP.bind('<Return>', Ynoeud_nextP)
            ZnoeudP.bind('<Return>', AjouterNoeubP)
            tk.Button(frameNoeudP, text='Ajouter nœud', command=AjouterNoeudP).grid(row=7)
            Liste_listboxNoeudsP.append(tk.Listbox(frameNoeudP, selectmode=tk.SINGLE))
            Liste_listboxNoeudsP[0].grid(row=8)
            tk.Button(frameNoeudP, text='Renommer nœud', command=RenommerNoeudP).grid(row=11)
            tk.Button(frameNoeudP, text='Supprimer nœud', command=SupprimerNoeudP).grid(row=12)
            
        ongletsInputPoutre.add(frameNoeudP)
        ongletsInputPoutre.tab(0, text='Nœuds',image=Noeud_rouge, compound=tk.LEFT)
        frameChargementsP = tk.Frame(ongletsInputPoutre)
        
        
        if True or 'Chargements / Degrés de liberté':
            Fleche_rouge = tk.PhotoImage(file="fleche_rouge.png").subsample(18,18)
            Fleche_verte = tk.PhotoImage(file="fleche_verte.png").subsample(15,15)
            
            def choix_liaisonP(evt):
                if ComboboxP.current()>=0:
                    update_deg_liberteP(ListeLibertesP[Combobox.current()])
                    ComboboxP.set('')
                
            def update_deg_liberteP(libertes):
                for i in range(len(libertes)):
                    ListeCheckP[i].state([('' if libertes[i] else '!')+'selected'])
                    lockP(i)
            
            def appliquer_chargementsP():
                global liste_noeuds
                if Liste_listboxNoeudsP[1].curselection()!=():
                    selectd_index= Liste_listboxNoeudsP[1].curselection()[0]
                    plein = True
                    for i in range(6):
                        try:
                            float(listeEntryP[i].get())
                        except ValueError:
                            listeEntryP[i].focus()
                            listeEntryP[i].select_range(0,tk.END)
                            plein = False
                            break
                    if plein:
                        for i in range(3):
                            try:
                                float(listeEntryRP[i].get())
                            except ValueError:
                                listeEntryRP[i].focus()
                                listeEntryRP[i].select_range(0,tk.END)
                                plein = False
                                break
                            
                    if plein:
                        # degrés de liberté
                        liste_noeuds[selectd_index][2] = [int(ListeCheckP[i].instate(['!selected'])) for i in range(6)]
                        # liste_noeuds[Liste_listboxNoeuds[1].curselection()[0]][2] = [int(ListeCheck[0].instate(['!selected'])),int(ListeCheck[1].instate(['!selected'])),int(ListeCheck[2].instate(['!selected'])),int(ListeCheck[3].instate(['!selected'])),int(ListeCheck[4].instate(['!selected'])),int(ListeCheck[5].instate(['!selected']))]
                        # forces et moments
                        liste_noeuds[selectd_index][3] = [float(listeEntryP[0].get()), float(listeEntryP[1].get()), float(listeEntryP[2].get()), float(listeEntryP[3].get()), float(listeEntryP[4].get()), float(listeEntryP[5].get())]
                        # ressort
                        liste_noeuds[selectd_index][4] = [float(listeEntryRP[0].get()), float(listeEntryRP[1].get()), float(listeEntryRP[2].get())]
                        
                        update_deg_liberteP((0,0,0,0,0,0))
                        for i in listeEntryP:
                            i.delete(0,tk.END)
                            i.insert(0,'0')
                        for i in listeEntryRP:
                            i.delete(0,tk.END)
                            i.insert(0,'0')
                        Liste_listboxNoeudsP[1].focus()
                        Liste_listboxNoeudsP[1].index(selectd_index)
                        Liste_listboxNoeudsP[1].activate(selectd_index+1)
                        
                        vert = True
                        for i in liste_noeuds:
                            if i[2]==None:
                                vert = False
                                break
                        if vert:
                            ongletsInputPoutre.tab(1, image = Fleche_verte, compound=tk.LEFT)
                        else:
                            ongletsInputPoutre.tab(1, image = Fleche_rouge, compound=tk.LEFT)
                    else:
                        tk.messagebox.showerror('Erreur', 'Une donnée ne peut pas être interprétée comme float')
                else:
                    tk.messagebox.showerror('Erreur', 'Pas de nœud sélectionné')
            
            def lockP(index):
                listeEntryP[index].config(state = (tk.NORMAL if ListeCheckP[index].instate(['!selected']) else tk.DISABLED))
                if index <=2:
                    listeEntryRP[index].config(state = (tk.NORMAL if ListeCheckP[index].instate(['!selected']) else tk.DISABLED))
                
            tk.Label(frameChargementsP, text='Définir les propriétés des nœuds :').grid(row=0) 
            tk.Label(frameChargementsP, text='Choix du nœud :').grid(row=1)
            Liste_listboxNoeudsP.append(tk.Listbox(frameChargementsP, selectmode=tk.SINGLE))
            Liste_listboxNoeudsP[1].grid(row=2)
            
            frameDeplacementsP = tk.LabelFrame(frameChargementsP, text='Degrés de liberté du nœud')
            frameDeplacementsP.grid(row=3)
            ListeCheckP = []
            temp_text=("Bloquage selon X","Bloquage selon Y","Bloquage selon Z","Bloquage en rotation selon X","Bloquage en rotation selon Y","Bloquage en rotation selon Z")
            for i in range(6):
                ListeCheckP.append(ttk.Checkbutton(frameDeplacementsP, text = temp_text[i], command= lambda index=i: lock(index)))
                ListeCheckP[i].state(['!alternate'])
                ListeCheckP[i].grid(row=i%3, column = i//3)
            tk.Label(frameDeplacementsP, text = 'liaisons standard :').grid(row=3, column = 0,sticky=tk.E)
            ListeliaisonsP = ['Encastrement','Rotule','Libre']
            ListeLibertesP = [(1,1,1,1,1,1),(1,1,1,0,0,0),(0,0,0,0,0,0)]
            ComboboxP = ttk.Combobox(frameDeplacementsP,values = ListeliaisonsP)
            ComboboxP.grid(row=3, column = 1,sticky=tk.W)
            ComboboxP.bind('<<ComboboxSelected>>',choix_liaisonP)
            
            frameForceP = tk.LabelFrame(frameChargementsP, text = 'Chargements du nœud')
            frameForceP.grid(row=4)
            tk.Label(frameForceP, text = 'Force selon X (N) :').grid(row=0, column = 0)
            tk.Label(frameForceP, text = 'Force selon Y (N) :').grid(row=1, column = 0)
            tk.Label(frameForceP, text = 'Force selon Z (N) :').grid(row=2, column = 0)
            tk.Label(frameForceP, text = 'Moment selon X (N.m) :').grid(row=3, column = 0)
            tk.Label(frameForceP, text = 'Moment selon Y (N.m) :').grid(row=4, column = 0)
            tk.Label(frameForceP, text = 'Moment selon Z (N.m) :').grid(row=5, column = 0)
            def next_ForceP(evt, index):
                if index==5:
                    listeEntryRP[0].focus()
                    listeEntryRP[0].select_range(0,tk.END)
                else:
                    listeEntryP[index+1].focus()
                    listeEntryP[index+1].select_range(0,tk.END)
            listeEntryP = []
            for i in range(6):
                listeEntryP.append(tk.Entry(frameForceP))
                listeEntryP[i].insert(0,'0')
                listeEntryP[i].grid(row=i, column = 1)
                listeEntryP[i].bind('<Return>', lambda evt, index=i:next_ForceP(evt,index))
            
            frameRessortP = tk.LabelFrame(frameChargementsP, text = 'Ressort du nœud')
            frameRessortP.grid(row=5)
            listeEntryRP = []
            tk.Label(frameRessortP, text = 'Ressort selon X (N/m) :').grid(row=0, column = 0) # ajouter ressort en torsion ?
            tk.Label(frameRessortP, text = 'Ressort selon Y (N/m) :').grid(row=1, column = 0)
            tk.Label(frameRessortP, text = 'Ressort selon Z (N/m) :').grid(row=2, column = 0)
            def next_RessortP(evt, index):
                if index==2:
                    appliquer_chargementsP()
                else:
                    listeEntryRP[index+1].focus()
                    listeEntryRP[index+1].select_range(0,tk.END)
            for i in range(3):
                listeEntryRP.append(tk.Entry(frameRessortP))
                listeEntryRP[i].insert(0,'0')
                listeEntryRP[i].grid(row=i, column = 1)
                listeEntryRP[i].bind('<Return>', lambda evt, index=i:next_RessortP(evt,index))
            
            tk.Button(frameChargementsP, text = 'Appliquer les propriétés au nœud', command = appliquer_chargementsP).grid(row= 6)
            
        ongletsInputPoutre.add(frameChargementsP)
        ongletsInputPoutre.tab(1, text='Propriétés des nœuds',image=Fleche_rouge, compound=tk.LEFT)
        framePoutreP = tk.Frame(ongletsInputPoutre)
        
        if True or 'Poutres':
            
            def ajouter_poutreP():
                global liste_poutres
                if len(Liste_listboxNoeudsP[2].curselection())==2:
                    
                    plein = True
                    for i in listeEntreesP:
                        try:
                            float(i.get())
                        except ValueError:
                            plein = False
                            break
                    if plein:
                        for i in listeRepartieP:
                            try:
                                float(i.get())
                            except ValueError:
                                plein = False
                                break
                    if plein:
                        temp_poutre = ['Poutre '+str(len(liste_poutres)+1),[liste_noeuds[min(Liste_listboxNoeuds[2].curselection())][0],liste_noeuds[max(Liste_listboxNoeuds[2].curselection())][0]]]+[(float(i.get()) for i in listeEntrees)]+[[(float(j.get()) for j in listeRepartie)]]
                        absent = True
                        for i in liste_poutres:
                            if temp_poutre[1]==i[1]:
                                absent = False
                                tk.messagebox.showerror('Erreur', 'Cette poutre existe déjà. Elle a pour nom :' + temp_poutre[0])
                                break
                        if absent:
                            liste_poutres.append(temp_poutre)
                            update_poutresP(len(liste_poutres)-1)
                        # else:
                        #     tk.messagebox.showerror('Erreur', '')
                else:
                    tk.messagebox.showerror('Erreur', 'Sélectionner 2 nœuds dans la liste')
            
            def update_poutresP(index):
                for i in Liste_listboxPoutresP:
                    i.delete(index)
                if Liste_listboxPoutresP[0].size()!=len(liste_poutres):
                    for i in Liste_listboxPoutresP:
                        i.insert(index,liste_poutres[index][0]+" "+str(liste_poutres[index][1]))
                Liste_listboxPoutresP[0].see(index)
                temp_noeuds= []
                for i in liste_poutres:
                    for j in i[1]:
                        if not(j in temp_noeuds):
                            temp_noeuds.append(j)
                
                if len(liste_noeuds)>len(temp_noeuds):
                    ongletsInputPoutre.tab(2, image = Poutre_rouge, compound=tk.LEFT)
                else:
                    ongletsInputPoutre.tab(2, image = Poutre_verte, compound=tk.LEFT)
                
                
                
            Poutre_rouge = tk.PhotoImage(file="Poutre_rouge.png").subsample(6,6)
            Poutre_verte = tk.PhotoImage(file="Poutre_verte.png").subsample(10,10)
            
            tk.Label(framePoutreP, text='Définir les liaisons entre les nœuds et leurs propriétés :').grid(row=0) 
            tk.Label(framePoutreP, text='Liste des poutres :').grid(row=1)
            Liste_listboxPoutresP.append(tk.Listbox(framePoutreP, selectmode=tk.SINGLE))
            Liste_listboxPoutresP[0].grid(row=2)
            tk.Label(framePoutreP, text='Choix des nœuds à lier :').grid(row=3)
            Liste_listboxNoeudsP.append(tk.Listbox(framePoutreP, selectmode=tk.MULTIPLE))
            Liste_listboxNoeudsP[2].grid(row=4)
            tk.Label(framePoutreP, text='Aire de la section (m²) :').grid(row=5)
            tk.Label(framePoutreP, text='Inertie de la poutre (m^4) :').grid(row=7)
            tk.Label(framePoutreP, text='Module de Young (Pa) :').grid(row=9)
            listeEntreesP = []
            for i in range(3):
                listeEntreesP.append(tk.Entry(framePoutreP))
                listeEntreesP[i].insert(0,'0')
                listeEntreesP[i].grid(row = 6+i*2)
            
            frameRepartieP = tk.LabelFrame(framePoutreP, text = 'Charge répartie sur la poutre')
            frameRepartieP.grid(row=11)
            listeRepartieP = []
            tk.Label(frameRepartieP, text = 'Charge répartie selon X (N/m) :').grid(row=0, column = 0) # ajouter ressort en torsion ?
            tk.Label(frameRepartieP, text = 'Charge répartie selon Y (N/m) :').grid(row=1, column = 0)
            tk.Label(frameRepartieP, text = 'Charge répartie selon Z (N/m) :').grid(row=2, column = 0)
            def next_RepartieP(evt, index):
                if index==2:
                    appliquer_chargementsP()
                else:
                    listeRepartieP[index+1].focus()
                    listeRepartieP[index+1].select_range(0,tk.END)
            for i in range(3):
                listeRepartieP.append(tk.Entry(frameRepartieP))
                listeRepartieP[i].insert(0,'0')
                listeRepartieP[i].grid(row=i, column = 1)
                listeRepartieP[i].bind('<Return>', lambda evt, index=i:next_RepartieP(evt,index))
            tk.Button(framePoutreP, text = 'Ajouter poutre', command = ajouter_poutreP).grid(row= 12)
            
        ongletsInputPoutre.add(framePoutreP)
        ongletsInputPoutre.tab(2, text='Poutres',image=Poutre_rouge, compound=tk.LEFT)
            
    PanedwindowPoutre.add(ongletsInputPoutre)
    PanedwindowPoutre.add(tk.Canvas(PanedwindowPoutre))
    # PanedwindowPoutre.sashpos(0, 10)
    ongletsEtapePoutre.add(PanedwindowPoutre)
    ongletsEtapePoutre.tab(0, text="Données d'entrée")
    
    if True or 'Output': # juste pour structurer le programme
        
        def CalculerP():
            print(liste_noeuds, '\n', liste_poutres)
            
            
            # Calculer(données_d_entrée)
        
        BoutonCalculerP = tk.Button(ongletsEtapePoutre,text = 'Lancer le calcul', command = CalculerP)
        BoutonCalculerP.pack(side=tk.LEFT, expand = tk.Y, fill = tk.BOTH)
        ongletsEtapePoutre.add(BoutonCalculerP)
        ongletsEtapePoutre.tab(1, text="Résultats du calcul")
    
    ongletsModele.add(ongletsEtapePoutre)
    ongletsModele.tab(0, text="Modèle Poutre") # nomme cet onglet 
    
    frameBarre = tk.Frame(ongletsModele)
    ongletsModele.add(frameBarre)
    ongletsModele.tab(1, text="Modèle Barre/Treillis")
    ongletsEtape = ttk.Notebook(ongletsModele)
    PanedwindowPortique = ttk.Panedwindow(ongletsEtape, orient=tk.HORIZONTAL)
    
    if True or 'Inputs': # juste pour structurer le programme
        
        ongletsInput = ttk.Notebook(PanedwindowPortique)
        frameNoeud = tk.Frame(ongletsInput)
        
        if True or 'Noeuds':
            Noeud_rouge = tk.PhotoImage(file="Noeud_rouge.gif").subsample(9,9)
            Noeud_vert = tk.PhotoImage(file="Noeud_vert.gif").subsample(7,7)
            
            def AjouterNoeub(evt):
                AjouterNoeud()
            def AjouterNoeud():
                plein = True
                try:
                    float(Xnoeud.get())
                    float(Ynoeud.get())
                    float(Znoeud.get())
                except ValueError:
                    plein = False
                if plein:
                    temp_noeud=(float(Xnoeud.get()),float(Ynoeud.get()),float(Znoeud.get()))
                    absent = True
                    for i in liste_noeuds:
                        if i[1]==temp_noeud:
                            absent = False
                            break
                    if absent:
                        liste_noeuds.append(['Nœud '+str(len(liste_noeuds)+1),temp_noeud,None,None,None])
                        listboxNoeud_update(len(liste_noeuds)-1)
                        Xnoeud.focus()
                        Xnoeud.select_range(0,tk.END)
                    else:
                        tk.messagebox.showerror('Erreur', 'Ce nœud existe déjà, il ne peut pas être ajouté.')
                else:
                    tk.messagebox.showerror('Erreur', 'Un champ de coordonnées ne peut pas être interprété comme float')
            
            def listboxNoeud_update(index):
                for i in Liste_listboxNoeuds:
                    i.delete(index)
                if Liste_listboxNoeuds[0].size()!=len(liste_noeuds):
                    for i in Liste_listboxNoeuds:
                        i.insert(index,liste_noeuds[index][0]+" "+str(liste_noeuds[index][1]))
                Liste_listboxNoeuds[0].see(index)
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
            Fleche_verte = tk.PhotoImage(file="fleche_verte.png").subsample(15,15)
            
            def choix_liaison(evt):
                if Combobox.current()>=0:
                    update_deg_liberte(ListeLibertes[Combobox.current()])
                    Combobox.set('')
                
            def update_deg_liberte(libertes):
                for i in range(len(libertes)):
                    ListeCheck[i].state([('' if libertes[i] else '!')+'selected'])
                    lock(i)
            
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
                            break
                    if plein:
                        for i in range(3):
                            try:
                                float(listeEntryR[i].get())
                            except ValueError:
                                listeEntryR[i].focus()
                                listeEntryR[i].select_range(0,tk.END)
                                plein = False
                                break
                            
                    if plein:
                        # degrés de liberté
                        liste_noeuds[selectd_index][2] = [int(ListeCheck[i].instate(['!selected'])) for i in range(6)]
                        # liste_noeuds[Liste_listboxNoeuds[1].curselection()[0]][2] = [int(ListeCheck[0].instate(['!selected'])),int(ListeCheck[1].instate(['!selected'])),int(ListeCheck[2].instate(['!selected'])),int(ListeCheck[3].instate(['!selected'])),int(ListeCheck[4].instate(['!selected'])),int(ListeCheck[5].instate(['!selected']))]
                        # forces et moments
                        liste_noeuds[selectd_index][3] = [float(listeEntry[0].get()), float(listeEntry[1].get()), float(listeEntry[2].get()), float(listeEntry[3].get()), float(listeEntry[4].get()), float(listeEntry[5].get())]
                        # ressort
                        liste_noeuds[selectd_index][4] = [float(listeEntryR[0].get()), float(listeEntryR[1].get()), float(listeEntryR[2].get())]
                        
                        update_deg_liberte((0,0,0,0,0,0))
                        for i in listeEntry:
                            i.delete(0,tk.END)
                            i.insert(0,'0')
                        for i in listeEntryR:
                            i.delete(0,tk.END)
                            i.insert(0,'0')
                        Liste_listboxNoeuds[1].focus()
                        Liste_listboxNoeuds[1].index(selectd_index)
                        Liste_listboxNoeuds[1].activate(selectd_index+1)
                        
                        vert = True
                        for i in liste_noeuds:
                            if i[2]==None:
                                vert = False
                                break
                        if vert:
                            ongletsInput.tab(1, image = Fleche_verte, compound=tk.LEFT)
                        else:
                            ongletsInput.tab(1, image = Fleche_rouge, compound=tk.LEFT)
                    else:
                        tk.messagebox.showerror('Erreur', 'Une donnée ne peut pas être interprétée comme float')
                else:
                    tk.messagebox.showerror('Erreur', 'Pas de nœud sélectionné')
            
            def lock(index):
                listeEntry[index].config(state = (tk.NORMAL if ListeCheck[index].instate(['!selected']) else tk.DISABLED))
                if index <=2:
                    listeEntryR[index].config(state = (tk.NORMAL if ListeCheck[index].instate(['!selected']) else tk.DISABLED))
                
            tk.Label(frameChargements, text='Définir les propriétés des nœuds :').grid(row=0) 
            tk.Label(frameChargements, text='Choix du nœud :').grid(row=1)
            Liste_listboxNoeuds.append(tk.Listbox(frameChargements, selectmode=tk.SINGLE))
            Liste_listboxNoeuds[1].grid(row=2)
            
            frameDeplacements = tk.LabelFrame(frameChargements, text='Degrés de liberté du nœud')
            frameDeplacements.grid(row=3)
            ListeCheck = []
            temp_text=("Bloquage selon X","Bloquage selon Y","Bloquage selon Z","Bloquage en rotation selon X","Bloquage en rotation selon Y","Bloquage en rotation selon Z")
            for i in range(6):
                ListeCheck.append(ttk.Checkbutton(frameDeplacements, text = temp_text[i], command= lambda index=i: lock(index)))
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
            listeEntry = []
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
        framePoutre = tk.Frame(ongletsInput)
        
        if True or 'Poutres':
            
            def ajouter_poutre():
                global liste_poutres
                if len(Liste_listboxNoeuds[2].curselection())==2:
                    
                    plein = True
                    for i in listeEntrees:
                        try:
                            float(i.get())
                        except ValueError:
                            plein = False
                            break
                    if plein:
                        for i in listeRepartie:
                            try:
                                float(i.get())
                            except ValueError:
                                plein = False
                                break
                    if plein:
                        temp_poutre = ['Poutre '+str(len(liste_poutres)+1),[liste_noeuds[min(Liste_listboxNoeuds[2].curselection())][0],liste_noeuds[max(Liste_listboxNoeuds[2].curselection())][0]]]+[(float(i.get()) for i in listeEntrees)]+[[(float(j.get()) for j in listeRepartie)]]
                        absent = True
                        for i in liste_poutres:
                            if temp_poutre[1]==i[1]:
                                absent = False
                                tk.messagebox.showerror('Erreur', 'Cette poutre existe déjà. Elle a pour nom :' + temp_poutre[0])
                                break
                        if absent:
                            liste_poutres.append(temp_poutre)
                            update_poutres(len(liste_poutres)-1)
                        # else:
                        #     tk.messagebox.showerror('Erreur', '')
                else:
                    tk.messagebox.showerror('Erreur', 'Sélectionner 2 nœuds dans la liste')
            
            def update_poutres(index):
                for i in Liste_listboxPoutres:
                    i.delete(index)
                if Liste_listboxPoutres[0].size()!=len(liste_poutres):
                    for i in Liste_listboxPoutres:
                        i.insert(index,liste_poutres[index][0]+" "+str(liste_poutres[index][1]))
                Liste_listboxPoutres[0].see(index)
                temp_noeuds= []
                for i in liste_poutres:
                    for j in i[1]:
                        if not(j in temp_noeuds):
                            temp_noeuds.append(j)
                
                if len(liste_noeuds)>len(temp_noeuds):
                    ongletsInput.tab(2, image = Poutre_rouge, compound=tk.LEFT)
                else:
                    ongletsInput.tab(2, image = Poutre_verte, compound=tk.LEFT)
                
                
                
            Poutre_rouge = tk.PhotoImage(file="Poutre_rouge.png").subsample(6,6)
            Poutre_verte = tk.PhotoImage(file="Poutre_verte.png").subsample(10,10)
            
            tk.Label(framePoutre, text='Définir les liaisons entre les nœuds et leurs propriétés :').grid(row=0) 
            tk.Label(framePoutre, text='Liste des poutres :').grid(row=1)
            Liste_listboxPoutres.append(tk.Listbox(framePoutre, selectmode=tk.SINGLE))
            Liste_listboxPoutres[0].grid(row=2)
            tk.Label(framePoutre, text='Choix des nœuds à lier :').grid(row=3)
            Liste_listboxNoeuds.append(tk.Listbox(framePoutre, selectmode=tk.MULTIPLE))
            Liste_listboxNoeuds[2].grid(row=4)
            tk.Label(framePoutre, text='Aire de la section (m²) :').grid(row=5)
            tk.Label(framePoutre, text='Inertie de la poutre (m^4) :').grid(row=7)
            tk.Label(framePoutre, text='Module de Young (Pa) :').grid(row=9)
            listeEntrees = []
            for i in range(3):
                listeEntrees.append(tk.Entry(framePoutre))
                listeEntrees[i].insert(0,'0')
                listeEntrees[i].grid(row = 6+i*2)
            
            frameRepartie = tk.LabelFrame(framePoutre, text = 'Charge répartie sur la poutre')
            frameRepartie.grid(row=11)
            listeRepartie = []
            tk.Label(frameRepartie, text = 'Charge répartie selon X (N/m) :').grid(row=0, column = 0) # ajouter ressort en torsion ?
            tk.Label(frameRepartie, text = 'Charge répartie selon Y (N/m) :').grid(row=1, column = 0)
            tk.Label(frameRepartie, text = 'Charge répartie selon Z (N/m) :').grid(row=2, column = 0)
            def next_Repartie(evt, index):
                if index==2:
                    appliquer_chargements()
                else:
                    listeRepartie[index+1].focus()
                    listeRepartie[index+1].select_range(0,tk.END)
            for i in range(3):
                listeRepartie.append(tk.Entry(frameRepartie))
                listeRepartie[i].insert(0,'0')
                listeRepartie[i].grid(row=i, column = 1)
                listeRepartie[i].bind('<Return>', lambda evt, index=i:next_Repartie(evt,index))
            tk.Button(framePoutre, text = 'Ajouter poutre', command = ajouter_poutre).grid(row= 12)
            
        ongletsInput.add(framePoutre)
        ongletsInput.tab(2, text='Poutres',image=Poutre_rouge, compound=tk.LEFT)
            
    PanedwindowPortique.add(ongletsInput)
    PanedwindowPortique.add(tk.Canvas(PanedwindowPortique))
    # PanedwindowPortique.sashpos(0, 10)
    ongletsEtape.add(PanedwindowPortique)
    ongletsEtape.tab(0, text="Données d'entrée")
    
    if True or 'Output': # juste pour structurer le programme
        
        def Calculer():
            print(liste_noeuds, '\n', liste_poutres)
            
            
            # Calculer(données_d_entrée)
        
        BoutonCalculer = tk.Button(ongletsEtape,text = 'Lancer le calcul', command = Calculer)
        BoutonCalculer.pack(side=tk.LEFT, expand = tk.Y, fill = tk.BOTH)
        ongletsEtape.add(BoutonCalculer)
        ongletsEtape.tab(1, text="Résultats du calcul")
    
    ongletsModele.add(ongletsEtape)
    ongletsModele.tab(2, text="Modèle Portique")
    
    
    ongletsModele.pack(side=tk.LEFT, expand = tk.Y, fill = tk.BOTH)
    main_w.mainloop()






liste_noeuds=[]
liste_poutres=[]
main()
