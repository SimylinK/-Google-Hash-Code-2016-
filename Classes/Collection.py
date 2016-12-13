#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Classes.Photo import Photo


class Collection:
    """
        Classe chargée de stocker des informations sur les collections d'images.
    """

    def __init__(self, nb_points, nb_photos, nb_intervalles):
        """
        :param nb_points: le nombre de points rapportés par la collection si on la complète
        :param nb_photos: le nombre de points d'intérêt à photograpier
        :param nb_intervalles: le nombre d'intervalles dans lesquels on peut photographier
        """
        self.nb_points = nb_points
        self.nb_photos = nb_photos
        self.nb_intervalles = nb_intervalles
        self.liste_intervalles = []  # Liste des intervalles pour la collection
        self.liste_photos = []  # Liste d'instances de la classe Photo, qu'on initialise vide et remplit ensuite
        self.ratio_rentabilite = self.donner_ratio(nb_points, nb_photos)  # Représente le poids de la collection
        self.complete = False  # Booléen qui indique si la collection est complétée ou non

    def donner_ratio(self, nb_points, nb_photos):
        """
            Méthode chargée de :
            Calculer le ratio de rentabilité.
        """
        ratio = nb_points / nb_photos
        return ratio

    def ajouter_photo(self, photo):
        """
        Méthode qui ajoute une instance de la classe Photo à la collection.
        :param photo:instance de la classe Photo
        """
        self.liste_photos.append(photo)

    def ajouter_intervalle(self, intervalle):
        """
        Méthode qui ajoute un intervalle à la collection.
        :param intervalle: liste de deux entiers
        """
        self.liste_intervalles.append(intervalle)

    def update(self):
        """
        Méthode qui met à jour la collection et indique en retour si elle est complète.
        :return: Un booléen qui indique si la collection est complète
        """
        self.nb_photos -= 1
        if self.nb_photos == 0:
            self.complete = True
        return self.complete

"""Tests divers."""
if __name__ == "__main__":
    nb_points = 192
    nb_photos = 1
    nb_intervalles = 1
    # Création d'une collection
    c1 = Collection(nb_points, nb_photos, nb_intervalles)

    # Test de la méthode ajouter_photo
    # 97797 -340859
    c1.ajouter_photo(Photo(97797, -340859, c1))

    # Test de la méthode ajouter_intervalle
    # 0 604799
    c1.ajouter_intervalle([0, 604799])

    # Test de la méthode donner_ratio
    ratio = c1.donner_ratio(nb_points, nb_photos)
    print("Ratio de rentabilité de la collection : " + str(ratio))
