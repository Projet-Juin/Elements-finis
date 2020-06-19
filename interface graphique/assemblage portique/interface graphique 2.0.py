# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 17:48:31 2020

@author: Guillaume WEBER
"""

import tkinter as tk
import json
from tkinter import ttk
from PortiqueBien import CalculerPortique
from code_pour_poutre import liste_des_demandes_utilisateur
from Fichier_barre import Calculer_Barre
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


def main():
    global liste_noeuds, liste_poutres
    main_w = tk.Tk() # crée la fenêtre principale
    main_w.geometry("750x750+0+8") # dimentions dimXxdimY+écartAuBordX+écartAuBordY
    main_w.title('Calcul de strucure par la Méthode éléments finis') # titre
    
    if True or 'Barre de Menu':
        
        def ouvrir():
            global liste_noeuds, liste_poutres
            temp_nom = tk.simpledialog.askstring("Ouvrir fichier", 'Nom du fichier :')
            with open(temp_nom+'.json', "r") as f:
                liste_noeuds, liste_poutres = json.load(f)
            
        def sauvegarder():
            temp_nom = tk.simpledialog.askstring("Sauvegarder fichier", 'Nom du fichier :')
            with open(temp_nom+".json", "w") as f:
                json.dump((liste_noeuds, liste_poutres), f)
        
        def set_modele_poutre():
            Ynoeud.config(state= tk.DISABLED)
            Znoeud.config(state= tk.DISABLED)
        def set_2D():
            Znoeud.config(state= (tk.DISABLED if D2.get()==1 else tk.NORMAL))
            
        barre_de_menu = tk.Menu(main_w)
        main_w.config(menu=barre_de_menu)
        menu_modele = tk.Menu(barre_de_menu) # Création d'un menu élts finis
        modele = tk.IntVar()
        modele.set(3)
        D2 = tk.IntVar()
        D2.set(1)
        menu_modele.add_radiobutton(label="Passer au modèle Poutre",command=set_modele_poutre, variable = modele, value = 1) # ajout de l'item permettant d'aller en élément finis
        menu_modele.add_radiobutton(label='Passer au modèle Barre / Treillis',command='', variable = modele, value = 2) # ajout de l'item permettant d'importer les données d'éléments finis
        menu_modele.add_radiobutton(label='Passer au modèle Portique',command='', variable = modele, value = 3) # ajout de l'item permettant d'exporter les données d'éléments finis
        menu_modele.add_separator()
        menu_modele.add_checkbutton(label='2D',command=set_2D, variable = D2)
        barre_de_menu.add_cascade(label='Choix du modèle', menu=menu_modele)
        
        # Création d'un menu fichier et ajout d'items
        fichier_menu = tk.Menu(barre_de_menu) # Création d'un menu fichier
        fichier_menu.add_command(label='Ouvrir',command=ouvrir) # ajout de l'item ouvrir
        fichier_menu.add_command(label='Sauvegarder',command=sauvegarder) # ajout de l'item sauvegarder
        fichier_menu.add_command(label='Redémarrer,command=reboot_programme') # ajout de l'item redémarrer
        fichier_menu.add_separator() #ajout d'un separateur
        fichier_menu.add_command(label='Quitter',command=main_w.destroy) # ajout de l'item quitter (ou sys.exit)
        barre_de_menu.add_cascade(label='Fichier', menu=fichier_menu)
        # Création d'un menu éléments finis et ajout d'items
        elts_finis_menu = tk.Menu(barre_de_menu) # Création d'un menu élts finis
        elts_finis_menu.add_command(label="Ouvrir l'interface Résistance des matériaux,command=switch_elts_finis") # ajout de l'item permettant d'aller en élément finis
        elts_finis_menu.add_separator() #ajout d'un separateur
        elts_finis_menu.add_command(label='Importer les Inputs d\'Éléments finis,command=import_elts_finis') # ajout de l'item permettant d'importer les données d'éléments finis
        elts_finis_menu.add_command(label='Exporter les Inputs d\'Éléments finis,command=export_elts_finis') # ajout de l'item permettant d'exporter les données d'éléments finis
        barre_de_menu.add_cascade(label='Résistance des Matériaux', menu=elts_finis_menu)
        # Création d'un menu autres et ajout d'items
        autres_menu = tk.Menu(barre_de_menu) # Création d'un menu autres
        autres_menu.add_command(label='Aide,command=aide') # ajout de l'item aide
        autres_menu.add_command(label='Conditions de fonctionnement,command=ctds_de_fct') # ajout de l'item conditions de la rdm
        autres_menu.add_separator() #ajout d'un separateur
        autres_menu.add_command(label='Crédit,command=credit') # ajout de l'item crédit
        barre_de_menu.add_cascade(label='Autres', menu=autres_menu) # ajouter de autres_menu dans barre_de_menu
    
    
    
    Liste_listboxNoeuds = []
    Liste_listboxPoutres = []
    
    # ongletsModele = ttk.Notebook(main_w) # crée une barre d'onglet
    # framePoutre = tk.Frame(ongletsModele) # crée un cadre
    # ongletsModele.add(framePoutre) # l'ajoute dans un onglet de la barre d'onglet
    # ongletsModele.tab(0, text="Modèle Poutre") # nomme cet onglet 
    # frameBarre = tk.Frame(ongletsModele) # même chose pour l'onglet 2
    # ongletsModele.add(frameBarre)
    # ongletsModele.tab(1, text="Modèle Barre/Treillis")
    ongletsEtape = ttk.Notebook(main_w)
    PanedwindowPortique = ttk.Panedwindow(ongletsEtape, orient="horizontal")
    
    if True or 'Inputs': # juste pour structurer le programme
        
        ongletsInput = ttk.Notebook(PanedwindowPortique)
        frameNoeud = tk.Frame(ongletsInput)
        
        if True or 'Noeuds':
            Noeud_rouge = tk.PhotoImage(file="images\\Noeud_rouge.gif").subsample(9,9)
            Noeud_vert = tk.PhotoImage(file="images\\Noeud_vert.gif").subsample(7,7)
            
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
            Fleche_rouge = tk.PhotoImage(file="images\\fleche_rouge.png").subsample(18,18)
            Fleche_verte = tk.PhotoImage(file="images\\fleche_verte.png").subsample(15,15)
            
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
            Combobox = ttk.Combobox(frameDeplacements,values = Listeliaisons, state = "readonly")
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
                        temp_poutre = ['Poutre '+str(len(liste_poutres)+1),[liste_noeuds[min(Liste_listboxNoeuds[2].curselection())][0],liste_noeuds[max(Liste_listboxNoeuds[2].curselection())][0]]]
                        temp_poutre.append(float(listeEntrees[0].get()))
                        temp_poutre.append(float(listeEntrees[1].get()))
                        temp_poutre.append(float(listeEntrees[2].get()))
                        temp_poutre.append([float(listeRepartie[0].get()) ,float(listeRepartie[1].get()),float(listeRepartie[2].get())])
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
                
                
                
            Poutre_rouge = tk.PhotoImage(file="images\\Poutre_rouge.png").subsample(6,6)
            Poutre_verte = tk.PhotoImage(file="images\\Poutre_verte.png").subsample(10,10)
            
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
            tk.Label(frameRepartie, text = 'Charge normale répartie (N/m) :').grid(row=0, column = 0) # ajouter ressort en torsion ?
            tk.Label(frameRepartie, text = '').grid(row=1, column = 0) # Charge répartie selon Y (N/m) :
            tk.Label(frameRepartie, text = '').grid(row=2, column = 0) # Charge répartie selon Z (N/m) :
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
    PanedwindowPortique.sashpos(0, 10)
    ongletsEtape.add(PanedwindowPortique)
    ongletsEtape.tab(0, text="Données d'entrée")
    
    if True or 'Output': # juste pour structurer le programme
        
        def Calculer():
            print(liste_noeuds, '\n', liste_poutres)
            if modele.get() == 1:
                N_element = len(liste_noeuds)
                listeabcisse = []
                type_appui = []
                for i in liste_noeuds:
                    listeabcisse.append(i[1][0])
                    temp = i[2][0] +i[2][1] +i[2][5]
                    if temp == 0:
                        type_appui.append("encastrement")
                    elif temp == 2:
                        type_appui.append("rotule")
                    elif temp == 3:
                        type_appui.append("rien")
                E = liste_poutres[0][4]
                I = liste_poutres[0][3]
                liste_force= []
                listeressort = []
                for i in liste_noeuds:
                    liste_force.append([i[3][1], i[3][5]])
                    listeressort.append(i[4][0])
                temp_poutres = sorted(liste_poutres, key = lambda poutre: int(liste_poutres[1][0].split()[1]))
                
                listedebutchargerepartie = []
                for i in temp_poutres:
                    listedebutchargerepartie.append(i[5][0])
                nombrepointsentre2noeuds = 1
                print(N_element,listeabcisse,nombrepointsentre2noeuds,I,E,type_appui,listedebutchargerepartie,listeressort,liste_force)
                
                liste_des_demandes_utilisateur(N_element,listeabcisse,nombrepointsentre2noeuds,I,E,type_appui,listedebutchargerepartie,listeressort,liste_force)
                
                
            elif modele.get() == 2:
                Calculer_Barre(liste_noeuds, liste_poutres)
                
            elif modele.get() == 3:
                plotun, plotdeux = CalculerPortique(liste_noeuds, liste_poutres)
                
                f = Figure(figsize=(16, 9), dpi=80)
                a = f.add_subplot(111)
                for i in plotun:
                    a.plot(i[0],i[1],'-.', c="red", marker='o')
                for j in plotdeux:
                    a.plot(j[0],j[1])
                a.set_xlabel('x')
                a.set_ylabel('y')
                
                canvas = FigureCanvasTkAgg(f, master=framegraph)
                canvas.get_tk_widget().grid(row = 0)
                
                # panedCalc.add(framegraph)
                # canvasgraph.pack(side=tk.TOP)
                # panedCalc.add(canvasgraph)
            
                
        
        panedCalc = ttk.Panedwindow(ongletsEtape, orient = tk.HORIZONTAL)
        
        BoutonCalculer = tk.Button(panedCalc,text = 'Lancer le calcul', command = Calculer)
        panedCalc.add(BoutonCalculer)
        framegraph = tk.LabelFrame(panedCalc, text = 'graph')
        # canvasgraph = tk.Canvas(panedCalc)
        # panedCalc.add(canvasgraph)
        panedCalc.add(framegraph)
        ongletsEtape.add(panedCalc)
        ongletsEtape.tab(1, text="Résultats du calcul")
        ongletsEtape.pack(side=tk.LEFT, expand = tk.Y, fill = tk.BOTH)
    
    # ongletsModele.add(ongletsEtape)
    # ongletsModele.tab(2, text="Modèle Portique")
    
    
    # ongletsModele.pack(side=tk.LEFT, expand = tk.Y, fill = tk.BOTH)
    main_w.mainloop()






liste_noeuds=[]
liste_poutres=[]
main()
