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
from section_inertie import getInertie
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pandastable import Table

def main():
    global liste_noeuds, liste_poutres
    main_w = tk.Tk() # crée la fenêtre principale
    main_w.geometry("900x750+0+8") # dimentions dimXxdimY+écartAuBordX+écartAuBordY
    main_w.title('Calcul de strucure par la Méthode éléments finis') # titre
    
    if True or 'Barre de Menu':
        
        def ouvrir():
            global liste_noeuds, liste_poutres
            temp_filename = tk.filedialog.askopenfilename()
            if temp_filename!='':
                with open(temp_filename, "r") as f:
                    liste_noeuds, liste_poutres = json.load(f)
                for i in Liste_listboxNoeuds:
                    i.delete(0,tk.END)
                    for j in liste_noeuds[:-1]:
                        i.insert(tk.END, j[0]+" "+str(j[1]))
                listboxNoeud_update(len(liste_noeuds)-1)
                for i in Liste_listboxPoutres:
                    i.delete(0,tk.END)
                    for j in liste_poutres[:-1]:
                        i.insert(tk.END, j[0]+" "+str(j[1]))
                update_poutres(len(liste_poutres)-1)
                valid_chargement()
                    
        def sauvegarder():
            temp_filename = tk.filedialog.asksaveasfilename()
            if temp_filename!='':
                with open(temp_filename, "w") as f:
                    json.dump((liste_noeuds, liste_poutres), f)
        
        def change_model():
            Combomodel.set(('Modèle Poutre', 'Modèle Barre / Treillis', 'Modèle Portique')[modele.get()-1])
            Ynoeud.config(state= (tk.DISABLED if modele.get() in (1,) else tk.NORMAL))
            Znoeud.config(state= (tk.DISABLED if modele.get() in (1,2,3) or D2.get() else tk.NORMAL))
            listeEntry[0].config(state= (tk.DISABLED if modele.get() in (1,) or ListeCheck[0].instate(['selected']) else tk.NORMAL))
            listeEntry[1].config(state= (tk.DISABLED if ListeCheck[1].instate(['selected']) else tk.NORMAL))
            listeEntry[2].config(state= (tk.DISABLED if modele.get() in (1,2,3) or D2.get() or ListeCheck[2].instate(['selected']) else tk.NORMAL))
            listeEntry[3].config(state= (tk.DISABLED if modele.get() in (1,2,3) or D2.get() or ListeCheck[3].instate(['selected']) else tk.NORMAL))
            listeEntry[4].config(state= (tk.DISABLED if modele.get() in (1,2,3) or D2.get() or ListeCheck[4].instate(['selected']) else tk.NORMAL))
            listeEntry[5].config(state= (tk.DISABLED if modele.get() in (2,) or ListeCheck[5].instate(['selected']) else tk.NORMAL))
            listeEntryR[0].config(state= (tk.DISABLED if modele.get() in (1,2,3) or ListeCheck[0].instate(['selected']) else tk.NORMAL))
            listeEntryR[1].config(state= (tk.DISABLED if modele.get() in (1,2,3) or ListeCheck[1].instate(['selected']) else tk.NORMAL))
            listeEntryR[2].config(state= (tk.DISABLED if modele.get() in (1,2,3) or D2.get() or ListeCheck[2].instate(['selected']) else tk.NORMAL))
            for i in (2,3,4):
                ListeCheck[i].state((['disabled'] if D2.get() else ['!disabled']))
            listeEntrees[0].config(state= (tk.DISABLED if modele.get() in (1,) else tk.NORMAL))
            listeEntrees[1].config(state= (tk.DISABLED if modele.get() in (2,) else tk.NORMAL))
            listeRepartie[0].config(state= (tk.DISABLED if modele.get() in (2,) else tk.NORMAL))
            tailleMaillage.config(state= (tk.DISABLED if modele.get() in (2,) else tk.NORMAL))
            
            
        def credit():
            root=tk.Toplevel()
            root.title("Solve Structure --- Crédits")
            root.geometry("600x500")
            tk.Label(root,font=("Arial", 14, "bold italic"),text='SOLVE STRUCTURE --- VERSION 1.0').pack(fill='both')
            tk.Label(root,justify='center',text= "A la demande de l'EPF, une équipe d'étudiants a mis en place le logiciel SolveStructure.\nC'est un programme ayant pour objectif d'étudier les effets d'une ou plusieurs charges sur une structure.\n").pack(fill='both')
            tk.Label(root,justify='center',text= 'L\'application a été conçu par :\n').pack(fill='both')
            tk.Label(root,justify='center',text= 'Partie RDM : \nAgnès DURIEZ --- Clara FERRU --- Henri FORJOT\n').pack(fill='both')
            tk.Label(root,justify='center',text= 'Partie Eléments finis : \nOmbline DELASSUS --- Lansana DIOMANDE --- Guillaume WEBER --- Xingyu XIA\n').pack(fill='both')
            logo_1 = tk.PhotoImage(file='images\\Logo_EPF.png')
            logo_2 = tk.PhotoImage(file='images\\logo_crédit.png')
            labellogo_1=tk.Label(root,image=logo_1)
            labellogo_1.image = logo_1
            labellogo_1.pack(anchor='s')
            labellogo_2=tk.Label(root,image=logo_2)
            labellogo_2.image = logo_2
            labellogo_2.pack(anchor='s')
            
        barre_de_menu = tk.Menu(main_w)
        main_w.config(menu=barre_de_menu)
        menu_modele = tk.Menu(barre_de_menu) # Création d'un menu élts finis
        modele = tk.IntVar()
        modele.set(3)
        D2 = tk.IntVar()
        D2.set(1)
        menu_modele.add_radiobutton(label="Passer au modèle Poutre",command=change_model, variable = modele, value = 1) 
        menu_modele.add_radiobutton(label='Passer au modèle Barre / Treillis',command=change_model, variable = modele, value = 2)
        menu_modele.add_radiobutton(label='Passer au modèle Portique',command=change_model, variable = modele, value = 3) 
        menu_modele.add_separator()
        menu_modele.add_checkbutton(label='2D',command=change_model, variable = D2)
        barre_de_menu.add_cascade(label='Choix du modèle', menu=menu_modele)
        
        # Création d'un menu fichier et ajout d'items
        fichier_menu = tk.Menu(barre_de_menu) 
        fichier_menu.add_command(label='Ouvrir',command=ouvrir) 
        fichier_menu.add_command(label='Sauvegarder',command=sauvegarder) 
        fichier_menu.add_command(label='Redémarrer,command=reboot_programme') 
        fichier_menu.add_separator() 
        fichier_menu.add_command(label='Quitter',command=main_w.destroy)
        barre_de_menu.add_cascade(label='Fichier', menu=fichier_menu)
        
        elts_finis_menu = tk.Menu(barre_de_menu)
        elts_finis_menu.add_command(label="Ouvrir l'interface Résistance des matériaux,command=switch_elts_finis") 
        elts_finis_menu.add_separator()
        elts_finis_menu.add_command(label='Importer les Inputs d\'Éléments finis,command=import_elts_finis') 
        elts_finis_menu.add_command(label='Exporter les Inputs d\'Éléments finis,command=export_elts_finis') 
        barre_de_menu.add_cascade(label='Résistance des Matériaux', menu=elts_finis_menu)
        
        autres_menu = tk.Menu(barre_de_menu) 
        autres_menu.add_command(label='Aide,command=aide') 
        autres_menu.add_command(label='Conditions de fonctionnement,command=ctds_de_fct') 
        autres_menu.add_separator() 
        autres_menu.add_command(label='Crédit',command=credit)
        barre_de_menu.add_cascade(label='Autres', menu=autres_menu)
    
        
    Liste_listboxNoeuds = []
    Liste_listboxPoutres = []
    
    PanedwindowPortique = ttk.Panedwindow(main_w, orient="horizontal")
    
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
                    for i in range(len(liste_poutres)):
                        if liste_noeuds[Liste_listboxNoeuds[0].curselection()[0]][0] in liste_poutres[i][1]:
                            del liste_poutres[i]
                            update_poutres(i)
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
            
            def infosNoeud():
                if Liste_listboxNoeuds[0].curselection()!=():
                    index = Liste_listboxNoeuds[0].curselection()[0]
                    strTitle = 'Informations sur le nœud : '+liste_noeuds[index][0]
                    strCorp = 'Nom : '+liste_noeuds[index][0]+'\n\nCoordonnées du nœud (x, y, z):\n'+str(liste_noeuds[index][1])+'\n\nDegrés de liberté du nœud (X, Y, Z, L, M, N):\n'+str(liste_noeuds[index][2])
                    strCorp2 = '\n\nListe des poutres auxquelles ce noeud appartient :\n'
                    for i in liste_poutres:
                        if liste_noeuds[index][0] in i[1]:
                            strCorp2 += i[0]+'\n'
                    tk.messagebox.showinfo(strTitle, strCorp+'\n\nChargements au nœud (Fx, Fy, Fz, Mx, My, Mz):\n'+str(liste_noeuds[index][3][0:6])+'\n\nRessorts au nœud (Kx, Ky, Kz):\n'+str(liste_noeuds[index][3][6:9])+strCorp2)
                else:
                    tk.messagebox.showerror('Erreur', 'Aucun nœud sélectionné.')
                    
            tk.Label(frameNoeud, text='Ajouter des nœuds :').grid(row=0)
            tk.Label(frameNoeud, text='Position selon X (m) :').grid(row=1)
            tk.Label(frameNoeud, text='Position selon Y (m) :').grid(row=3)
            tk.Label(frameNoeud, text='Position selon Z (m) :').grid(row=5)
            Xnoeud = tk.Entry(frameNoeud)
            Xnoeud.insert(0,'0')
            Xnoeud.grid(row=2)
            Ynoeud = tk.Entry(frameNoeud)
            Ynoeud.insert(0,'0')
            Ynoeud.grid(row=4)
            Znoeud = tk.Entry(frameNoeud)
            Znoeud.insert(0,'0')
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
            tk.Button(frameNoeud, text='Infos du nœud', command=infosNoeud).grid(row=10)
            tk.Button(frameNoeud, text='Renommer nœud', command=RenommerNoeud, state=tk.DISABLED).grid(row=11)
            tk.Button(frameNoeud, text='Supprimer nœud', command=SupprimerNoeud).grid(row=12)
            
        ongletsInput.add(frameNoeud)
        ongletsInput.tab(0, text='Nœuds',image=Noeud_rouge, compound=tk.LEFT)
        frameChargements = tk.Frame(ongletsInput)
        
        if True or 'Chargements / Degrés de liberté':
            Fleche_rouge = tk.PhotoImage(file="images\\fleche_rouge.png").subsample(20,20)
            Fleche_verte = tk.PhotoImage(file="images\\fleche_verte.png").subsample(16,16)
            
            def choix_liaison(evt):
                if Combobox.current()>=0:
                    update_deg_liberte(ListeLibertes[Combobox.current()])
                
            def update_deg_liberte(libertes):
                for i in range(len(libertes)):
                    ListeCheck[i].state([('' if libertes[i] else '!')+'selected'])
                change_model()
            
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
                        # forces et moments
                        liste_noeuds[selectd_index][3] = [float(listeEntry[0].get()), float(listeEntry[1].get()), float(listeEntry[2].get()), float(listeEntry[3].get()), float(listeEntry[4].get()), float(listeEntry[5].get())]
                        # ressort
                        liste_noeuds[selectd_index][4] = [float(listeEntryR[0].get()), float(listeEntryR[1].get()), float(listeEntryR[2].get())]
                        
                        update_deg_liberte((0,0,0,0,0,0))
                        Combobox.set('')
                        for i in listeEntry:
                            i.delete(0,tk.END)
                            i.insert(0,'0')
                        for i in listeEntryR:
                            i.delete(0,tk.END)
                            i.insert(0,'0')
                        Liste_listboxNoeuds[1].see(selectd_index)
                        Liste_listboxNoeuds[1].selection_clear(selectd_index)
                        Liste_listboxNoeuds[1].selection_set(selectd_index+1)
                        
                        valid_chargement()
                    else:
                        tk.messagebox.showerror('Erreur', 'Une donnée ne peut pas être interprétée comme float')
                else:
                    tk.messagebox.showerror('Erreur', 'Aucun nœud sélectionné')
            
            def valid_chargement():
                vert = True
                for i in liste_noeuds:
                    if i[2]==None:
                        vert = False
                        break
                if vert:
                    ongletsInput.tab(1, image = Fleche_verte, compound=tk.LEFT)
                else:
                    ongletsInput.tab(1, image = Fleche_rouge, compound=tk.LEFT)
                
            tk.Label(frameChargements, text='Définir les propriétés des nœuds :').grid(row=0) 
            tk.Label(frameChargements, text='Choix du nœud :').grid(row=1)
            Liste_listboxNoeuds.append(tk.Listbox(frameChargements, selectmode = tk.SINGLE, exportselection=False))
            Liste_listboxNoeuds[1].grid(row=2)
            
            frameDeplacements = tk.LabelFrame(frameChargements, text='Degrés de liberté du nœud')
            frameDeplacements.grid(row=3)
            ListeCheck = []
            temp_text=("Bloquage selon X","Bloquage selon Y","Bloquage selon Z","Bloquage en rotation selon X","Bloquage en rotation selon Y","Bloquage en rotation selon Z")
            for i in range(6):
                ListeCheck.append(ttk.Checkbutton(frameDeplacements, text = temp_text[i], command= change_model))
                ListeCheck[i].state(['!alternate'])
                ListeCheck[i].bind("<Button-1>", lambda evt: Combobox.set(''))
                ListeCheck[i].grid(row=i%3, column = i//3)
            tk.Label(frameDeplacements, text = 'liaisons standard :').grid(row=3, column = 0,sticky=tk.E)
            Listeliaisons = ['Encastrement','Rotule','Libre']
            ListeLibertes = [(1,1,1,1,1,1),(1,1,1,0,0,0),(0,0,0,0,0,0)]
            Combobox = ttk.Combobox(frameDeplacements,values = Listeliaisons, state = "readonly")
            Combobox.grid(row=3, column = 1,sticky=tk.W)
            Combobox.bind('<<ComboboxSelected>>', choix_liaison)
            
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
                            if not(float(i.get())) and i.cget("state")!=tk.DISABLED:
                                plein = False
                                tk.messagebox.showerror('Erreur', 'Aucune propriété de poutre ne peut être nulle.')
                                i.focus()
                                i.select_range(0,tk.END)
                                break
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
                        temp_poutre.append([float(i.get()) for i in listeRepartie])
                        absent = True
                        for i in liste_poutres:
                            if temp_poutre[1]==i[1]:
                                absent = False
                                tk.messagebox.showerror('Erreur', 'Cette poutre existe déjà. Elle a pour nom :' + temp_poutre[0])
                                break
                        if absent:
                            liste_poutres.append(temp_poutre)
                            update_poutres(len(liste_poutres)-1)
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
            
            def suppr_poutre():
                if Liste_listboxPoutres[0].curselection()!=():
                    del liste_poutres[Liste_listboxPoutres[0].curselection()[0]]
                    update_poutres(Liste_listboxPoutres[0].curselection()[0])
                else:
                    tk.messagebox.showerror('Erreur', 'Aucune poutre sélectionnée.')
            
            def infosPoutre():
                if Liste_listboxPoutres[0].curselection()!=():
                    temp_poutre = liste_poutres[Liste_listboxPoutres[0].curselection()[0]]
                    strTitle = 'Informations sur la poutre : '+temp_poutre[0]
                    strCorp = 'Nom : '+str(temp_poutre[0])+'\n\nNoms des nœud aux extrémités (nom1, nom2):\n'+str(temp_poutre[1])+'\n\nAire de la section (m²): '+str(temp_poutre[2])+'\n\nInertie de la poutre (m^4): '+str(temp_poutre[3])
                    tk.messagebox.showinfo(strTitle, strCorp+'\n\nModule de Young de la section (Pa): '+str(temp_poutre[4])+'\n\nCharges réparties (N/m): '+str(temp_poutre[5]))
                else:
                    tk.messagebox.showerror('Erreur', 'Aucun nœud sélectionné.')
            
            def selectionner_geométrie():
                listargs = (('b',),('b','b1'),('b','h'),('b','h','b1','h1'),('b','h','b1','b2','h1'),('b','h','b1','h1'),('b','h','b1','h1'),('b','h','b1','b2','h1'),('b','h'),('R',),('R','R1'),('R',),('R',),('D2','D1'),('b','h'),('D2','D1'))
                def choix_geo(evt):
                    if ComboG.current()>=0:
                        img1 = tk.PhotoImage(file="images\\section "+ComboG.get()+".png").subsample(2,2)
                        imageL.configure(image= img1 )
                        imageL.image=img1
                        for i in range(len(listlabel)):
                            listEntry[i].delete(0,tk.END)
                            listEntry[i].insert(0,'0')
                            try:
                                listlabel[i].config(text= listargs[ComboG.current()][i])
                                listEntry[i].config(state= tk.NORMAL)
                            except IndexError:
                                listlabel[i].config(text= '')
                                listEntry[i].config(state= tk.DISABLED)
                def choix_sec():
                    valide = True
                    for i in range(len(listlabel)):
                        if listlabel[i].cget('text')!='' and float(listEntry[i].get())==0:
                            valide = False
                            listEntry[i].select_range(0,tk.END)
                            break
                    if valide and ComboG.current()>=0:
                        entrees = []
                        for i in range(len(listlabel)):
                            if listlabel[i].cget('text')!='':
                                entrees.append(float(listEntry[i].get()))
                        inertie, aire = getInertie(ComboG.current(), entrees)
                        listeEntrees[0].delete(0,tk.END)
                        listeEntrees[0].insert(0,str(aire))
                        listeEntrees[1].delete(0,tk.END)
                        listeEntrees[1].insert(0,str(inertie))
                
                geometrie = tk.Toplevel()
                geometrie.geometry("380x270+0+8") # dimentions dimXxdimY+écartAuBordX+écartAuBordY
                geometrie.title("Choix de la section et calcul de l'inertie") # titre
                frameG = tk.Frame(geometrie)
                frameG.pack(side=tk.LEFT, expand = tk.Y, fill = tk.BOTH)
                tk.Label(frameG, text = 'Choix du type de section :').grid(row = 0)
                imageL=tk.Label(frameG, compound=tk.LEFT)
                imageL.grid(column=1, rowspan = 8)
                ComboG = ttk.Combobox(frameG, values = ('Carré','Carré creux','Rectangle','Rectangle creux','Profil I','Profil T','Profil L','Profil Z','Triangle rectangle','Cercle','Cercle creux','Demi-cercle','Quart de cercle','Ovale','Croix','Losange'), state = "readonly")
                ComboG.grid(row=1)
                ComboG.bind('<<ComboboxSelected>>', choix_geo)
                
                listlabel = []
                listEntry =[]
                for i in range(5):
                    listlabel.append(tk.Label(frameG, text=''))
                    listlabel[i].grid(row = 2*i+2)
                    listEntry.append(tk.Entry(frameG))
                    listEntry[i].insert(0,'0')
                    listEntry[i].grid(row = 2*i+3)
                tk.Button(frameG, text='Appliquer section', command=choix_sec).grid(row=12)
                # geometrie.mainloop()
                    
            def ComboChangeMateriau(evt):
                if Combomateriau.current()>=0:
                    listeEntrees[2].delete(0,tk.END)
                    listeEntrees[2].insert(0,list_Young[Combomateriau.current()])
            list_Young = [210000000000, 203000000000, 69000000000, 83000000000, 124000000000, 289000000000, 209000000000, 124000000000, 41500000000, 196000000000, 100000000000, 45000000000, 214000000000, 78000000000, 168000000000, 116000000000, 78000000000, 27000000000, 14000000000, 450000000000, 1000000000000, 60000000000, 26000000000, 69000000000, 12000000000, 20000000000, 16000000000, 12000000000, 12000000000, 12400000000, 13000000000, 10000000000, 10000000000, 9500000000, 190000000000, 34500000000, 1100000000000, 2380000000, 2300000000, 3500000000]
            Poutre_rouge = tk.PhotoImage(file="images\\Poutre_rouge.png").subsample(6,6)
            Poutre_verte = tk.PhotoImage(file="images\\Poutre_verte.png").subsample(10,10)
            
            tk.Label(framePoutre, text='Définir les liaisons entre les nœuds et leurs propriétés :').grid(row=0) 
            tk.Label(framePoutre, text='Liste des poutres :').grid(row=1)
            Liste_listboxPoutres.append(tk.Listbox(framePoutre, selectmode=tk.SINGLE))
            Liste_listboxPoutres[0].grid(row=2)
            tk.Button(framePoutre, text="Infos poutre", command=infosPoutre).grid(row=3)
            tk.Button(framePoutre, text="Supprimer poutre", command=suppr_poutre).grid(row=4)
            tk.Label(framePoutre, text='Choix des nœuds à lier :').grid(row=5)
            Liste_listboxNoeuds.append(tk.Listbox(framePoutre, selectmode=tk.MULTIPLE, exportselection=False))
            Liste_listboxNoeuds[2].grid(row=6)
            tk.Button(framePoutre, text = "Sélectionner géométrie", command = selectionner_geométrie).grid(row=7)
            tk.Label(framePoutre, text='Aire de la section (m²) :').grid(row=8)
            tk.Label(framePoutre, text='Inertie de la poutre (m^4) :').grid(row=10)
            tk.Label(framePoutre, text='Module de Young (Pa) :').grid(row=12)
            listeEntrees = []
            def next_Props(index):
                if index==2:
                    listeRepartie[0].focus()
                    listeRepartie[0].select_range(0,tk.END)
                else:
                    listeEntrees[index+1].focus()
                    listeEntrees[index+1].select_range(0,tk.END)
            for i in range(3):
                listeEntrees.append(tk.Entry(framePoutre))
                listeEntrees[i].insert(0,'0')
                listeEntrees[i].grid(row = 9+i*2)
                listeEntrees[i].bind('<Return>', lambda evt, index=i:next_Props(index))
            Combomateriau = ttk.Combobox(framePoutre, values = ['Acier de construction', 'Acier inox 18-10', 'Aluminium (Al)', 'Argent (Ag)', 'Bronze', 'Chrome (Cr)', 'Cobalt (Co)', 'Cuivre (Cu)', 'Etain (Sn)', 'Fer (Fe)', 'Laiton (80% Cu, 20% Zn)', 'Magnésium (Mg)', 'Nickel (Ni)', 'Or (Au)', 'Platine (Pt)', 'Titane (Ti)', 'Zinc (Zn)', 'Béton', 'Brique', 'Carbure de Silice (SiC)', 'Diamant (C)', 'Granite', 'Marbre', 'Verre', 'Acajou', 'Bambou', 'Bois de rose (Brésil)', 'Bois de rose (Inde)', 'Chêne', 'Contreplaqué', 'Epicéa', 'Erable', 'Frêne', 'Séquoia', 'Fibre de carbone', 'Kevlar', 'Nanotubes (Carbone)', 'Plexiglass', 'Polycarbonate', 'Résine epoxy'], state = "readonly")
            Combomateriau.bind('<<ComboboxSelected>>', ComboChangeMateriau)
            Combomateriau.grid(row = 14)
            frameRepartie = tk.LabelFrame(framePoutre, text = 'Charge répartie sur la poutre')
            frameRepartie.grid(row=15)
            listeRepartie = []
            tk.Label(frameRepartie, text = 'Charge normale répartie (N/m) :').grid(row=0, column = 0) # ajouter ressort en torsion ?
            # tk.Label(frameRepartie, text = '').grid(row=1, column = 0) # Charge répartie selon Y (N/m) :
            # tk.Label(frameRepartie, text = '').grid(row=2, column = 0) # Charge répartie selon Z (N/m) :
            def next_Repartie(evt, index):
                if index==0:
                    appliquer_chargements()
                else:
                    listeRepartie[index+1].focus()
                    listeRepartie[index+1].select_range(0,tk.END)
            for i in range(1):
                listeRepartie.append(tk.Entry(frameRepartie))
                listeRepartie[i].insert(0,'0')
                listeRepartie[i].grid(row=i, column = 1)
                listeRepartie[i].bind('<Return>', lambda evt, index=i:next_Repartie(evt,index))
            tk.Button(framePoutre, text = 'Ajouter poutre', command = ajouter_poutre).grid(row= 16)
            
        ongletsInput.add(framePoutre)
        ongletsInput.tab(2, text='Poutres',image=Poutre_rouge, compound=tk.LEFT)
            
    PanedwindowPortique.add(ongletsInput)
    
    if True or 'Output': # juste pour structurer le programme
        
        dataframesP = []
        def Calculer():
            # global dataframesP
            def afficher_results(graphresult):
                for i in range(len(graphresult)):
                    if len(ongletsOutput.tabs())-1<i+1:
                        listFrame.append(tk.Frame(ongletsOutput))
                        liste_figure.append(Figure(figsize=(16, 9), dpi=80))
                        liste_graph.append(liste_figure[i].add_subplot(111))
    
                        liste_frame.append(FigureCanvasTkAgg(liste_figure[i], master=listFrame[i]))
                        
                        
                        NavigationToolbar2Tk(liste_frame[i], listFrame[i]).update()
                        liste_frame[i].get_tk_widget().pack()
                        ongletsOutput.add(listFrame[i])
                        
                    ongletsOutput.tab(i+1, text=graphresult[i][0], compound=tk.LEFT)
                    liste_graph[i].cla()
                    liste_graph[i].set_xlabel('x')
                    liste_graph[i].set_ylabel(graphresult[i][0])
                        # if len(graphresult[i][j+1])>2:
                        #     pass
                        #     img = (plt.imread("images\\encastrement.jpg"), plt.imread("images\\rotule.jpg"))
                            
                        #     imgliaison = 
                        #     fig, ax = plt.subplots()
                        #     ax.imshow(img, extent=[0, 400, 0, 300])
                    
                    for j in range(len(graphresult[i])-1):
                        
                        liste_graph[i].plot(graphresult[i][j+1][0],graphresult[i][j+1][1],graphresult[i][j+1][2])
                    liste_frame[i].draw()
                    
            # afficher_results('Strint \ntest', [['graphi1',[[0,1,2,3],[1,3,5,7]],[[0,1,2,3,4,5,6],[0,1,0,1,0,2,0]]],['graphi2',[[0,1,2,3],[0,1,4,9]]]])
            
            vert = True
            for i in liste_noeuds:
                if i[2]==None:
                    vert = False
                    break
            temp_noeuds= []
            for i in liste_poutres:
                for j in i[1]:
                    if not(j in temp_noeuds):
                        temp_noeuds.append(j)
            if len(liste_noeuds)==len(temp_noeuds) and vert and len(liste_noeuds)>=2:
                nombrepointsentre2noeuds = 1
                if modele.get() == 1:
                    N_element = len(liste_noeuds)
                    listeabcisse = []
                    type_appui = []
                    for i in liste_noeuds:
                        listeabcisse.append(i[1][0])
                        temp = i[2][0] +i[2][1] +i[2][5]
                        if temp == 0:
                            type_appui.append("encastrement")
                        elif temp == 1:
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
                    try :
                        if int(tailleMaillage.get())<=1:
                            nombrepointsentre2noeuds = int(tailleMaillage.get())
                    except TypeError:
                        tk.messagebox.showerror('Erreur', "La donnée taille de maillage ne peut pas être interprétée comme int")
                    
                    graphs, dataframes = liste_des_demandes_utilisateur(N_element,listeabcisse,nombrepointsentre2noeuds,I,E,type_appui,listedebutchargerepartie,listeressort,liste_force)
                    afficher_results(graphs)
                    dataframesP.append(dataframes)
                    temp_nomdata=[]
                    for i in dataframes:
                        temp_nomdata.append(i[0])
                    Combodata.config(values= temp_nomdata)
                    
                elif modele.get() == 2:
                    graphs, dataframes = Calculer_Barre(liste_noeuds, liste_poutres)
                    afficher_results(graphs)
                    dataframesP.append(dataframes)
                    temp_nomdata=[]
                    for i in dataframes:
                        temp_nomdata.append(i[0])
                    Combodata.config(values= temp_nomdata)
                    
                elif modele.get() == 3:
                    try :
                        if int(tailleMaillage.get())<=1:
                            nombrepointsentre2noeuds = int(tailleMaillage.get())
                    except TypeError:
                        tk.messagebox.showerror('Erreur', "La donnée taille de maillage ne peut pas être interprétée comme int")
                    graphs, dataframes = CalculerPortique(liste_noeuds, liste_poutres, nombrepointsentre2noeuds)
                    afficher_results(graphs)
                    dataframesP.append(dataframes)
                    temp_nomdata=[]
                    for i in dataframes:
                        temp_nomdata.append(i[0])
                    Combodata.config(values= temp_nomdata)
                    
            else:
                tk.messagebox.showerror('Erreur', "Les données d'entrée sont incomplètes")
        
        ongletsOutput = ttk.Notebook(PanedwindowPortique)
        
        PanedwindowCalc = ttk.Panedwindow(ongletsOutput, orient="horizontal")
        Calculframe = tk.Frame(PanedwindowCalc)
        tk.Label(Calculframe, text = "nombre de point de maillage :").grid(row=0)
        tailleMaillage = tk.Entry(Calculframe)
        tailleMaillage.grid(row=1)
        def ComboChangeModel(evt):
            if Combomodel.current()>=0:
                modele.set(Combomodel.current()+1)
                change_model()
        def refresh_struct():
            temp_X = []
            temp_Y = []
            a.cla()
            for i in liste_poutres:
                for j in liste_noeuds:
                    if i[1][0]==j[0]:
                        temp_X.append(j[1][0])
                        temp_Y.append(j[1][1])
                    elif i[1][1]==j[0]:
                        temp_X.append(j[1][0])
                        temp_Y.append(j[1][1])
            a.plot(temp_X,temp_Y,'-.', c="red", marker='o')
            graph.draw()
        def disp_dataframe(Ndataframe):
            newWindow = tk.Toplevel()
            frame = tk.Frame(newWindow)
            frame.pack(fill='both', expand=True)
            print(dataframesP,'691')
            pt = Table(frame, dataframe=dataframesP[0][Ndataframe][1])
            pt.show()
            pt.showIndex()
        Combomodel = ttk.Combobox(Calculframe, values = ('Modèle Poutre', 'Modèle Barre / Treillis', 'Modèle Portique'), state = "readonly")
        Combomodel.bind('<<ComboboxSelected>>', ComboChangeModel)
        Combomodel.grid(row = 2)
        tk.Button(Calculframe,text = 'Recharger la structure', command = refresh_struct).grid(row = 4)
        listFrame = []
        liste_figure = []
        liste_graph = []
        liste_frame = []
        tk.Button(Calculframe,text = 'Lancer le calcul', command = Calculer).grid(row = 5, rowspan = 2, sticky=tk.N+tk.S)
        def changedataframe(evt):
            if Combodata.current()>=0:
                disp_dataframe(Combodata.current())
        Combodata = ttk.Combobox(Calculframe, values = (), state = "readonly")
        Combodata.bind('<<ComboboxSelected>>', changedataframe)
        Combodata.grid(row = 7)
        img = tk.PhotoImage(file="images\\Logo_EPF.png").subsample(2,2)
        tk.Label(Calculframe,image = img, compound=tk.LEFT).grid(row = 8)
        PanedwindowCalc.add(Calculframe)
        ongletsOutput.add(PanedwindowCalc)
        canvasStruc = tk.Frame(PanedwindowCalc)
        PanedwindowCalc.add(canvasStruc)
        f = Figure(figsize=(16, 9), dpi=80)
        a = f.add_subplot(111)
        graph = FigureCanvasTkAgg(f, master=canvasStruc)
        NavigationToolbar2Tk(graph, canvasStruc).update()
        graph.get_tk_widget().pack()
        ongletsOutput.tab(0, text='Lancer le calcul', compound=tk.LEFT)
    PanedwindowPortique.add(ongletsOutput)
    PanedwindowPortique.pack(side=tk.LEFT, expand = tk.Y, fill = tk.BOTH)
    change_model()
    main_w.mainloop()


liste_noeuds=[]
liste_poutres=[]
main()
