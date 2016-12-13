#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Import servant seulement aux tests
"""
from Classes.Photo import Photo


class ZoneGlobe:
    """
    Classe représentant une zone de la planète, une case.
    """

    def __init__(self, latitude_min, latitude_max, longitude_min, longitude_max):
        """
        :param latitude_min: latitude minimale des objets présents dans cette case
        :param latitude_max: latitude maximale des objets présents dans cette case
        :param longitude_min: longitude minimale des objets présents dans cette case
        :param longitude_max: longitude maximale des objets présents dans cette case
        """
        self.latitude_min = latitude_min
        self.latitude_max = latitude_max
        self.longitude_min = longitude_min
        self.longitude_max = longitude_max
        self.photos_a_prendre = []  # Liste d'instances de la classe Photo, qui n'ont pas été prises
        self.photos_prises = []  # Liste d'instances de la classe Photo, qui ont été prises

    def ajouter_photo(self, photo):
        """
        Méthode qui ajoute une photo à la liste des photos à prendre
        """
        self.photos_a_prendre.append(photo)

"""Tests divers"""
if __name__ == "__main__":
    # Création d'une ZoneGlobe
    zg = ZoneGlobe(-20000, 20000, -20000, 20000)

    # Test de la méthode ajouter_photo
    zg.ajouter_photo(Photo(19500, -5042, None))
