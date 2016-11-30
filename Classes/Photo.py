#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Photo:
    """
        Classe composée de :
        La latitude et la longitude de chaque photo.
        La collection à laquelle elle appartient
    """
    
    def __init__(self, latitude, longitude, collection):
        self.latitude = latitude
        self.longitude = longitude
        self.collection = collection
        self.prise_par_id = None  # ID du satellite qui aura pris la photo
        self.prise_tour = None  # Tour pendant lequel la photo est prise
