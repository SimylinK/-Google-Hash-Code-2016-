#!/usr/bin/env python3
# -*- coding: utf-8 -*-


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

    def dispersion_collection(self):
        liste_lat = []
        liste_long = []
        for photo in self.liste_photos:
            liste_lat.append(photo.latitude)
            liste_long.append(photo.longitude)
        diff_lat = max(liste_lat) - min(liste_lat)
        diff_long = max(liste_long) - min(liste_long)
        return [diff_lat, diff_long]