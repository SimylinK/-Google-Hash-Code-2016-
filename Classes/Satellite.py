#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Satellite:
    """Classe chargée de :
    Représenter un satellite
    """

    def __init__(self, id, latitude_depart, longitude_depart, vitesse, vitesse_camera,
                 max_deplacement_camera):
        """
        :param id: un entier unique à chaque satellite
        :param latitude_depart: un entier dans [-324000;324000]
        :param longitude_depart: un entier dans [-648000;647999]
        :param vitesse: un entier représentant une vitesse en arcseconds par tour
        :param vitesse_camera: un entier représentant une vitesse en arcseconds par tour
        :param max_deplacement_camera: un entier positif représentant une distance en arcseconds
        """
        self.id = id
        self.latitude = latitude_depart
        self.longitude = longitude_depart
        self.latitude_camera = latitude_depart  # longitude et latitude de camera au départ sont la position satellite
        self.longitude_camera = longitude_depart
        self.vitesse = vitesse
        self.vitesse_camera = vitesse_camera
        self.vitesse_camera_relative = vitesse_camera
        self.max_deplacement_camera = max_deplacement_camera

    def tour_suivant(self, latitude_cam=None, longitude_cam=None):
        """ Calcule la position suivante du satellite
        et la prochaine position de la caméra si besoin ( si les valeurs sont différentes de None)
        """
        # Déplacement du Satellite
        lat = self.latitude + self.vitesse
        long = self.longitude - 15
        # Passage au-dessus du pôle nord
        if lat > 324000:
            lat = 324000 - (lat - 324000)
            long -= 648000
            self.vitesse = -self.vitesse
        # Passage au-dessus du pôle sud
        elif lat < -324000:
            lat = -324000 + (abs(lat) - 324000)
            long -= 648000
            self.vitesse = -self.vitesse
        # long est compris entre -648000 et 647999
        if long < -648000:
            long = 648000 - (-long - 648000)
        self.latitude = lat
        self.longitude = long

        # Déplacement de la caméra
        if latitude_cam:
            self.latitude_camera = latitude_cam
            self.longitude_camera = longitude_cam
        else:
            lat_cam = self.latitude_camera + self.vitesse
            long_cam = self.longitude_camera - 15

            # Passage au-dessus du pôle nord
            if lat_cam > 324000:
                lat_cam = 324000 - (lat_cam - 324000)
                long_cam -= 648000
            # Passage au-dessus du pôle sud
            elif lat_cam < -324000:
                lat_cam = -324000 + (abs(lat_cam) - 324000)
                long_cam -= 648000
            # long est compris entre -648000 et 647999
            if long_cam < -648000:
                long_cam = 648000 - (-long_cam - 648000)

            self.latitude_camera = lat_cam
            self.longitude_camera = long_cam

    def calcul_distance_satellite_camera(self):
        """ Calcul la distance entre le satellite et la position de la caméra
        Attention ne marche pas si a côté d'un pôle
        :return: 2 entiers positifs, (latitude, longitude)
        """
        """Calcul de la distance en longitude"""
        if (abs(self.longitude_camera - self.longitude) > self.max_deplacement_camera):
            """ Dans ce cas on passe par -648000 et 647999 en longitude """
            if (self.longitude_camera < self.longitude):
                dist_long = self.longitude_camera + 1296000 - self.longitude
            else:
                dist_long = self.longitude + 1296000 - self.longitude_camera
        else:
            dist_long = abs(self.longitude - self.longitude_camera)

        """Calcul de la distance en latitude"""
        distance_lat = abs(self.latitude - self.latitude_camera)

        return distance_lat, dist_long


if(__name__ == "__main__"):
    # Création d'un satellite
    s1 = Satellite(0, 0, -648000, 10, 5, 100)
    s1.latitude_camera = 6
    s1.longitude_camera = 647998

    # Test calcul_distance_satellite_camera
    lat, long = s1.calcul_distance_satellite_camera()
    print("lat = " + str(lat) + " ; (doit être égale a 6)")
    print("long = " + str(long) + " ; (doit être égale a 2)")
