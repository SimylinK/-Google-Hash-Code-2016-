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

    def __init__(self, nb_points, nb_photos, ratio_rentabilite):
        self.nb_points = nb_points
        self.nb_photos = nb_photos
        self.ratio_rentabilité = self.donner_ratio()

    def donner_ratio(self):
        """
            Méthode chargée de :
            Calculer le ratio de rentabilité.
        """
        ratio = nb_points/nb_photos
        return ratio
