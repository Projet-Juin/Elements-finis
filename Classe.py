import numpy
import pandas

class Element(object):
    def __init__(self, List_noeud, Aire_section, Largeur_section, Hauteur_section, E, I, Coef_poisson, Longueur_poutre, Angle_section):

        #Importation de données
        self.List_noeud = List_noeud
        self.Noeud_label_i, self.Noeud_label_j = List_noeud
        self.Aire_section = Aire_section
        self.Largeur_section = Largeur_section
        self.Hauteur_section = Hauteur_section
        self.E = E
        self.I = I
        self.EI = E * I
        self.Coef_poisson = Coef_poisson
        self.Longueur_poutre = Longueur_poutre
        self.Angle_section = Angle_section

        self.k_barre = self.Aire_section * self.E / self.Longueur_poutre
        self.C = numpy.cos(self.Angle_section)
        self.S = numpy.sin(self.Angle_section)

        #Créer des matrices
        self.K_local_barre = self. __matrice_locale_barre(self.C, self.S, self.k_barre, self.List_noeud)
        self.K_local_poutre = self.__matrice_locale_poutre(self.Longueur_poutre, self.EI, self.List_noeud)

    #Créer la matrice locale pour barre
    def __matrice_locale_barre(self, C, S, K, A):
        kk = numpy.array([[0 for i in range(4)] for i in range(4)])
        kk[0][0] = C ** 2 * K
        kk[2][2] = C ** 2 * K
        kk[1][1] = S ** 2 * K
        kk[3][3] = S ** 2 * K
        kk[0][1] = C * S * K
        kk[1][0] = C * S * K
        kk[2][3] = C * S * K
        kk[3][2] = C * S * K
        kk[0][2] = - C ** 2 * K
        kk[2][0] = - C ** 2 * K
        kk[1][3] = - S ** 2 * K
        kk[3][1] = - S ** 2 * K
        kk[0][3] = - C * S * K
        kk[1][2] = - C * S * K
        kk[2][1] = - C * S * K
        kk[3][0] = - C * S * K

        #nommage des colonnes et des lignes
        A_colonnes = self.nommage_matrice_barre_colonnes(A)
        A_lignes = self.nommage_matrice_barre_lignes(A)
        kk = pandas.DataFrame(kk, columns=A_colonnes, index=A_lignes)
        return kk

    #Créer la matrice locale pour poutre
    def __matrice_locale_poutre(self, L, EI, A):
        kk = numpy.array([[12, 6 * L, -12, 6 * L], [0, 4 * L ** 2, -6 * L, 2 * L ** 2], [0, 0, 12, -6 * L], [0, 0, 0, 4 * L ** 2]])
        m = EI / L
        kk = [i * m for i in kk]

        # nommage des colonnes et lignes
        A_colonnes = self.nommage_matrice_poutre_colonnes(A)
        A_lignes = self.nommage_matrice_poutre_lignes(A)
        kk = pandas.DataFrame(kk, columns=A_colonnes, index=A_lignes)
        return kk

    def nommage_matrice_barre_colonnes(self, listnoeud):
        # Ici on créer une chaine composé des noms des colonnes des matrices barres
        A = []

        for i in range(len(listnoeud)):
            A.append("d" + str(listnoeud[i]) + "x")
            A.append("d" + str(listnoeud[i]) + "y")

        return A

    def nommage_matrice_barre_lignes(self, listnoeud):
        # Ici on créer une chaine composé des noms des lignes des matrices barres
        A = []

        for i in range(len(listnoeud)):
            A.append("F" + str(listnoeud[i]) + "x")
            A.append("F" + str(listnoeud[i]) + "y")

        return A

    def nommage_matrice_poutre_colonnes(self, listnoeud):
        # Ici on créer une chaine composé des noms des colonnes des matrices poutres
        A = []

        for i in range(len(listnoeud)):
            A.append("d" + str(listnoeud[i]) + "y")
            A.append("phi" +str(listnoeud[i]))

        return A

    def nommage_matrice_poutre_lignes(self, listnoeud):
        # Ici on créer une chaine composé des noms des lignes des matrices poutres
        A = []

        for i in range(len(listnoeud)):
            A.append("F" + str(listnoeud[i]) + "y")
            A.append("M" + str(listnoeud[i]))

        return A

class Noeud(object):
    def __init__(self, Fx, Fy, Mz):
        self.Fx = Fx
        self.Fy = Fy
        self.Mz = Mz

if __name__ == '__main__':
    ElementSet = []
    NoeudSet = []

    print("Combien d'elements? :")
    N_element = int(input())

    for i in range(N_element):

        #Les données utilisées ici sont celles qui ont été saisies précédemment.
        print("Aire_section :")
        Aire_section = float(input())
        print("Largeur_section :")
        Largeur_section = float(input())
        print("Hauteur_section :")
        Hauteur_section = float(input())
        print("Numero du 1er noeud :")
        Noeud_label_i = int(input())
        print("Numero du 2eme noeud :")
        Noeud_label_j = int(input())
        List_noeud = []
        List_noeud.append(Noeud_label_i)
        List_noeud.append(Noeud_label_j)
        print("Module de Young :")
        E = float(input())
        print("Moment d’inertie :")
        I = float(input())
        print("Coefficient de Poisson :")
        Coef_poisson = float(input())
        print("Angle_section :")
        Angle_section = float(input())
        print("Longueur_poutre :")
        Longueur_poutre = float(input())

        #Création d'objets
        Ele = Element(List_noeud, Aire_section, Largeur_section, Hauteur_section, E, I, Coef_poisson, Longueur_poutre, Angle_section)
        ElementSet.append(Ele)

        #exemple de sortie
        K_local_barre = Ele.K_local_barre
        K_local_poutre = Ele.K_local_poutre
        print("K_local_barre={}".format(K_local_barre))
        print("K_local_poutre={}".format(K_local_poutre))

    print("Combien de noeuds :")
    N_noeud = int(input())
    for i in range(N_noeud):
        print("Fx pour noeud", i+1, " : ")
        Fx = float(input())
        print("Fy pour noeud", i+1, " : ")
        Fy = float(input())
        print("Mz pour noeud", i+1, " : ")
        Mz = float(input())
        N = Noeud(Fx, Fy, Mz)
        NoeudSet.append(N)


