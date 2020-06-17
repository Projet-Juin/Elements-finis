# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 16:42:08 2020

@author: ombli
"""

from matplotlib import patches
import math
import numpy as np
import matplotlib.pyplot as pyplot


#entrees :
liste_abscisses=[1,5,9,11]
liste_type_appui=["encastrement","rien","rotule","encastrement"]
liste_forces=[10,0,0,50,0,0,0,0]

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
        pyplot.annotate('force', xy=(liste_abscisses[k], liste_ordonnee[k]),xycoords='data',xytext=(0.12, 1), textcoords='axes fraction',arrowprops=dict(facecolor='black', shrink=0.5),horizontalalignment='right', verticalalignment='top',)
 #   if not liste_forces[2*k+1]==0:
  #      pyplot.annotate('moment', xy = (1, 1),xytext = (1, 1),arrowprops = {'facecolor': 'red', 'shrink': 0.1})

        

plt.legend()
pyplot.show()