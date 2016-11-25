#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Imports servant à :
    - à réutiliser les classes définies dans les autres fichiers :
        import Photo : classe Photo
"""

from Photo import Photo

class Collection:
    """
        Classe composée de :
        Un certain nombre de photos qu'il faudra prendre pour avoir les
        points qui lui sont associés. 
    """

    def __init__(self, nb_points, nb_photos,nb_intervalles,):
        self.nb_points = nb_points
        self.nb_photos = nb_photos
        self.nb_intervalles = nb_intervalles
        self.liste_photos = []  # Liste d'instances de la classe Photo, qu'on initialise vide et remplit ensuite
        self.ratio_rentabilité = self.donner_ratio(nb_points,nb_photos)

    def donner_ratio(self,nb_points,nb_photos):
        """
            Méthode chargée de :
            Calculer le ratio de rentabilité.
        """
        ratio = nb_points/nb_photos
        return ratio

    def ajouter_photo(self,latitude,longitude):
        """
        :param latitude:
        :param longitude:

            Méthode qui crée une instance de la classe Photo et l'ajoute à la collection.
        """
        photo = Photo(latitude,longitude)
        self.liste_photos.append(photo)

