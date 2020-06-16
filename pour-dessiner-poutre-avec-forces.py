import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.proj3d import proj_transform
from mpl_toolkits.mplot3d.axes3d import Axes3D

from matplotlib.text import Annotation


from mpl_toolkits.mplot3d import Axes3D

class Annotation3D(Annotation):
    def __init__(self, text, xyz, *args, **kwargs):
        super().__init__(text, xy=(0,0), *args, **kwargs)
        self._xyz = xyz

    def draw(self, renderer):
        x2, y2, z2 = proj_transform(*self._xyz, renderer.M)
        self.xy=(x2,y2)
        super().draw(renderer)

def annotate3D(ax,text, xyz, *args, **kwargs):
    '''Add anotation `text` to an `Axes3d` instance.'''

    annotation= Annotation3D(text, xyz, *args, **kwargs)
    ax.add_artist(annotation)

#setattr(Axes3D,'annotate3D',_annotate3D)

def dessin_poutre_rectangulaire_avec_2_abscisses(largeur,hauteur,liste_abscisses):
    L=[]
    for k in  liste_abscisses:
        L.append([-largeur/2, k, -hauteur/2])
        L.append([largeur/2, k, -hauteur/2])
    for k in liste_abscisses:
        L.append( [-largeur/2, k, hauteur/2 ])
        L.append([largeur/2, k, hauteur/2])
    return L

def definir_les_points_importants(L):
    minimum_xyz=[10**5,10**5,10**5]
    maximum_xyz=[0,0,0]
    for x in range (len(L)):
        if L[x][0]<=minimum_xyz[0] :
            if L[x][1]<=minimum_xyz[1] :
                if L[x][2]<=minimum_xyz[2] :
                    xmin=L[x][0]
                    ymin=L[x][1]
                    zmin=L[x][2]
                    minimum_xyz=[xmin,ymin,zmin]
    for x in range (len(L)):
        if L[x][0]>=maximum_xyz[0] :
            if L[x][1]>=maximum_xyz[1] :
                if L[x][2]>=maximum_xyz[2] :
                    xmax=L[x][0]
                    ymax=L[x][1]
                    zmax=L[x][2]
                    maximum_xyz=[xmax,ymax,zmax]
    return xmin,ymin,zmin,xmax,ymax,zmax

largeur=2
hauteur=5
liste_abscisses=[1,3,5,9]
#pour trouver les points necessaires au tracé des surfaces
L=dessin_poutre_rectangulaire_avec_2_abscisses(largeur,hauteur,liste_abscisses)
L=np.asarray(L)
xmin,ymin,zmin,xmax,ymax,zmax=definir_les_points_importants(L)

points = np.array([[xmin,ymin,zmin],
[xmax, ymin, zmin ],
[xmax, ymax, zmin],
[xmin, ymax, zmin],
[xmin,ymin, zmax],
[xmax, ymin, zmax ],
[xmax, ymax, zmax],
[xmin, ymax, zmax]])
print(xmin,ymin,zmin,xmax,ymax,zmax)


fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

r = [-1,1]


X, Y = np.meshgrid(r, r)
# afficher tous les points associés aux noeuds
Z=points
ax.scatter(L[:, 0], L[:, 1], L[:, 2])

# liste des surfaces à tracer
verts = [[Z[0],Z[1],Z[2],Z[3]],
[Z[4],Z[5],Z[6],Z[7]],
[Z[0],Z[1],Z[5],Z[4]],
[Z[2],Z[3],Z[7],Z[6]],
[Z[1],Z[2],Z[6],Z[5]],
[Z[4],Z[7],Z[3],Z[0]],
[Z[2],Z[3],Z[7],Z[6]]]

# afficher les surfaces
ax.add_collection3d(Poly3DCollection(verts,
facecolors="cyan", linewidths=1, edgecolors="r", alpha=.25))
#                                    liaisons,couleur fond, epaisseur ligne,couleur pourtour,opacite

#afficher les forces ponctuelles
ax.annotate3D('force',(0,8,3),xytext=(0,30),textcoords='offset points',arrowprops = dict(ec='blue', fc='red',shrink=2.5))
#             nom,position point,direction fleche,,couleur fleche

#####################pour charges réparties
ax.plot([0,0],marker=r'$\downarrow$',color = 'red',ms=10,ys=[0,9],zs=[4])
"""
[donne les x des fleches]
ys : donne les positions des fleches selon y
zs : donne la position de z
color : couleur des fleches

"""
#################### pour les moments
ax.plot([0,0],marker=r'$\circlearrowleft$',color = 'green',ms=10,ys=[0,9],zs=[4])
"""
[donne les x des fleches]
ys : donne les positions des fleches selon y
zs : donne la position de z
color : couleur des fleches
"""

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.grid(False)
plt.show()