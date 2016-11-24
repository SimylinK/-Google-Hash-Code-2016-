#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Satellite:
    def __init__(self, latitude_depart, longitude_depart, vitesse, vitesse_camera,
                 max_deplacement_camera, nombre_tours):
        self.latitude_depart = latitude_depart
        self.longitude_depart = longitude_depart
        self.vitesse = vitesse
        self.vitesse_camera = vitesse_camera
        self.max_deplacement_camera = max_deplacement_camera
        self.position = []  # positions[x][y] -> x=tour; y=0(latitude) ou 1(longitude)
        self.__calcul_positions(nombre_tours)

    def get_position(self, tour):
        """ Retourne la position du satellite a
        :param tour: entier positif
        :return: un tableau avec la latitude en 0 et la longitude en 1
        """
        return self.position[tour]

    def __calcul_positions(self, tour):
        """ Calcul la position du satellites pour les X premiers tour
        :param tour: le nombre de tour a calculer, entier positif
        """
        self.position.append([])
        self.position[0].append(self.latitude_depart)
        self.position[0].append(self.longitude_depart)
        vitesse = self.vitesse

        for i in range(1, tour):
            self.position.append([])
            lat = self.position[i - 1][0] + vitesse
            long = self.position[i - 1][1] - 15
            # Passage au-dessus du pôle nord
            if lat > 324000:
                lat = 324000 - (lat - 324000)
                long -= 648000
                vitesse = -vitesse
            # Passage au-dessus du pôle sud
            elif lat < -324000:
                lat = -324000 + (abs(lat) - 324000)
                long -= 648000
                vitesse = -vitesse
            # long est compris entre -648000 et 647999
            if long < -648000:
                long = 648000 - (-long - 648000)
            self.position[i].append(lat)
            self.position[i].append(long)
