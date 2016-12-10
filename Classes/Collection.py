#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Classes.Photo import Photo


class Collection:
    """
        Classe composée de :
        Un certain nombre de photos qu'il faudra prendre pour avoir les
        points qui lui sont associés.
    """

    def __init__(self, nb_points, nb_photos, nb_intervalles):
        self.nb_points = nb_points
        self.nb_photos = nb_photos
        self.nb_intervalles = nb_intervalles
        self.liste_intervalles = []  # Liste des intervalles pour la collection
        self.liste_photos = []  # Liste d'instances de la classe Photo, qu'on initialise vide et remplit ensuite
        self.ratio_rentabilite = self.donner_ratio(nb_points, nb_photos)

    def donner_ratio(self, nb_points, nb_photos):
        """
            Méthode chargée de :
            Calculer le ratio de rentabilité.
        """
        ratio = nb_points / nb_photos
        return ratio

    def ajouter_photo(self, photo):
        """
        :param photo:instance de la classe Photo

            Méthode ajoute une instance de la classe Photo à la collection.
        """
        self.liste_photos.append(photo)

    def ajouter_intervalle(self, intervalle):
        """
            Méthode ajoute un intervalle à la collection.
        """
        self.liste_intervalles.append(intervalle)


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
