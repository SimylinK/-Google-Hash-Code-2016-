#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Satellite:
    def __init__(self, id, latitude_depart, longitude_depart, vitesse, vitesse_camera,
                 max_deplacement_camera):
        self.id = id
        self.latitude = latitude_depart
        self.longitude = longitude_depart
        self.latitude_camera = latitude_depart  # longitude et latitude de camera au départ sont la position satellite
        self.longitude_camera = longitude_depart
        self.vitesse = vitesse
        self.vitesse_camera = vitesse_camera
        self.max_deplacement_camera = max_deplacement_camera

    def tour_suivant(self):
        """ Calcule la position suivante du satellite
        """
        vitesse = self.vitesse
        lat = self.latitude + vitesse
        long = self.longitude - 15
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
        self.latitude = lat
        self.longitude = long

    def __calcul_positions_camera(self, tour):
        """ Calcul la position de la caméra pour les X premiers tour
        :param tour: le nombre de tour à calculer, entier positif
        """
        self.position_camera.append([])
        self.position_camera[0].append(self.latitude_camera)
        self.position_camera[0].append(self.longitude_camera)
        vitesse_camera = self.vitesse_camera

        for i in range(1, tour):
            self.position_camera.append([])

            lat_a = self.position[i][0] + vitesse_camera
            lat_b = self.position[i][0] - vitesse_camera
            long_a = self.position[i][1] + vitesse_camera
            long_b = self.position[i][1] - vitesse_camera

            # latitude borne A
            # Passage au-dessus du pôle nord
            if lat_a > 324000:
                lat_a = 324000 - (lat_a - 324000)
            # Passage au-dessus du pôle sud
            elif lat_a < -324000:
                lat_a = -324000 + (abs(lat_a) - 324000)

            # latitude borne B
            # Passage au-dessus du pôle nord
            if lat_b > 324000:
                lat_b = 324000 - (lat_b - 324000)
                long -= 648000
            # Passage au-dessus du pôle sud
            elif lat_b < -324000:
                lat_b = -324000 + (abs(lat_b) - 324000)

            # long_a est compris entre -648000 et 647999
            if long_a < -648000:
                long_a = 648000 - (-long_a - 648000)
            # long_b est compris entre -648000 et 647999
            if long_b < -648000:
                long_b = 648000 - (-long_b - 648000)

            self.position_camera[i].append([lat_a, lat_b])
            self.position_camera[i].append([long_a, long_b])

            # on élargie la zone de déplacement possible, jusqu'a atteindre le déplacement maximal
            vitesse_camera += vitesse_camera
            if vitesse_camera > self.max_deplacement_camera:
                vitesse_camera = self.max_deplacement_camera

            """
            partie d'affichage des tests
            """
            print("tour ", i)
            print("latitude satellite : ", self.position[i][0])
            print("intervalle latitude : ", self.position_camera[i][0])
            print("longitude satellite : ", self.position[i][1])
            print("intervalle longitude : ", self.position_camera[i][1])
            print("vitesse : ", vitesse_camera)
            print("")

sat = Satellite(0,1,2,3,4,5)
