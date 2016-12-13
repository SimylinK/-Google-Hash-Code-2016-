#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Photo:
    """
    Classe composée de :
    La latitude et la longitude de chaque photo.
    La collection à laquelle elle appartient
    """

    def __init__(self, latitude, longitude, collection):
        """
        :param latitude: entier : la latitude de la photo
        :param longitude: entier : la longitude de la photo
        :param collection: Instance de la classe Collection
        """
        self.latitude = latitude
        self.longitude = longitude
        self.collection = collection
        self.prise_par_id = None  # ID du satellite qui aura pris la photo
        self.prise_tour = None  # Tour pendant lequel la photo est prise
