#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Classes.Photo import Photo


class Arbre:
    def __init__(self, noeud_debut = None):
        """
            Classe chargée de :
            représenter l'abre de prédiction.
        """

        self.noeud_debut = noeud_debut

    def actualiser_arbre(self, lat, long, coll):
        """ Sert à actualiser l'arbre à chaque tour :
        on ne garde que la branche qui a été choisie, et on incrémente le bas de cette branche
        """
        for noeud in self.noeud_debut.fils:
            if (noeud.photo[0] == lat) and (noeud.photo[1] == long) and (noeud.photo[2] == coll):
                self.noeud = noeud
                noeud.incrementer()

    def descendre_n_profondeur(self, noeud, profondeur):
        if profondeur != 0:
            for fils in noeud.fils():
                fils.incrementer()
                self.descendre_n_profondeur(noeud.fils, profondeur - 1)
        if profondeur == 0:
            return None

    def initialiser_arbre(self, arbre, profondeur):
        """ Sert à initialiser l'arbre au debut :
        on crée toutes les branches de l'arbre jusqu'à une certaine profondeur
        """
        self.descendre_n_profondeur(arbre.noeud_debut, profondeur)

class Noeud:
    """
        Classe chargée de :
        représenter les différents tours de l'abre de prédiction.
    """
    def __init__(self, num_tour, type, pere = None):
        self.num_tour = num_tour
        self.type = type #le type peut-être "True = prendre photo" ou "False = ne rien faire = augmenter la range de la camera"
        self.pere = pere
        self.photo = [] #photo = [latitude, longitude, collection] qu'on peut prendre à tel tour
        self.fils = []

    def creer_fils(self, type):
        """ Sert à créer un fils de type True = "prend photo" ou False = "ne prend pas de photo"
        """
        if type:
            noeud = Noeud(self.num_tour + 1, True, pere = self)
            self.fils.append(noeud)
        else:
            noeud = Noeud(self.num_tour + 1, False, pere = self)
            self.fils.append(noeud)
        return noeud

    def incrementer(self): #ATTENTION A PHOTOS_PRENABLES QUI N'EXISTE PAS ENCORE ICI
        """ Sert à créer tous les fils d'un noeud"
        """
        self.creer_fils(False)
        for photo in photos_prenables: #celles qui pour l'instant sont dans distributeur
            self.creer_fils(True)



if __name__ == "__main__":
    photos_prenables = [Photo(4,5,1), Photo(8,3,1), Photo(7,2,1), Photo(40,5,3), Photo(4,8,2), Photo(4,7,3)]
    n = Noeud(0, True)
    a = Arbre(Noeud)

    print(n.type)
    print(n.type)
    print(n.type)