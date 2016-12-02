#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Satellite:
    """

    """

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

    def tour_suivant(self, latitude_cam=None, longitude_cam=None):
        """ Calcule la position suivante du satellite
        et la prochaine position de la caméra si besoin ( si les valeurs sont différentes de None)
        """
        # Déplacement du Satellite
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

        # Déplacement de la caméra
        self.latitude_camera += vitesse
        if latitude_cam:
            self.latitude_camera = latitude_cam

        self.longitude_camera -= 15
        if longitude_cam:
            self.longitude_camera = longitude_cam
