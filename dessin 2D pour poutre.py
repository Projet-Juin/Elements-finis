# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 16:42:08 2020

@author: ombli
"""
import matplotlib.pyplot as plt
from matplotlib import patches
import math
import numpy as np
import matplotlib.pyplot as pyplot


#entrees :
liste_abscisses=[1,5,9]
liste_type_appui=["encastrement","rien","rotule"]
liste_forces=[10,0,0,50,0,0]

#code :
liste_ordonnee=[]
for k in range(len(liste_abscisses)):
    liste_ordonnee.append(0)

figure = pyplot.figure(figsize = (10, 10))
axes = figure.add_subplot(111)



pyplot.plot(liste_abscisses, liste_ordonnee, color='r', linestyle=':', marker='o')

for k in range(len(liste_abscisses)):
    if liste_type_appui[k]=='encastrement':
        pyplot.scatter(liste_abscisses[k], liste_ordonnee[k]-0.0002, s = 1000, c = 'g', marker = 's', edgecolors = 'b',label="encastrement")

    if liste_type_appui[k]=="rotule":
        pyplot.scatter(liste_abscisses[k], liste_ordonnee[k]-0.0002, s = 1000, c = 'g', marker = '^', edgecolors = 'b',label="rotule")

    if liste_type_appui[k]=="rien":
        pyplot.scatter(liste_abscisses[k], liste_ordonnee[k]-0.0002, s = 1000, c = 'g', marker = 'o', edgecolors = 'b',label="appui simple")

    if not liste_forces[2*k]==0:
        pyplot.annotate('        ', xy=(liste_abscisses[k], liste_ordonnee[k]),xycoords='data',xytext=(0.12, 1), textcoords='axes fraction',arrowprops=dict(facecolor='black', shrink=0.5),horizontalalignment='right', verticalalignment='top',)
    if not liste_forces[2*k+1]==0:
       pyplot.annotate('        ',xy=(liste_abscisses[k]+0.5, liste_ordonnee[k]-0.0003), xycoords='data', xytext=(-70,30), textcoords='offset points',arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=10,angleB=90,rad=20"),fontsize=10)


pyplot.ylim(-0.25, 1.5)
pyplot.legend()
pyplot.show()