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
        self.max_deplacement_camera = max_deplacement_camera
        #  range_deplacement représente la zone qui peut-être atteinte à un certain tour par la caméra
        self.range_deplacement_camera = [[self.latitude - self.vitesse_camera, self.latitude + self.vitesse_camera],
                                         [self.longitude - self.vitesse_camera, self.longitude + self.vitesse_camera]]

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
            self.range_deplacement_camera = [[self.latitude - self.vitesse_camera, self.latitude + self.vitesse_camera],
                                             [self.longitude - self.vitesse_camera,
                                              self.longitude + self.vitesse_camera]]

    def distance_latitude(self, latitude):
        """Calcule la distance en arcsecondes entre la latitude satellite et une latitude
        :return: latitude, entier positif """
        # Pas besoin de tester les pôles car il n'y a pas de photo à plus de 85° N ou S.
        return abs(self.latitude - latitude)

    def distance_longitude(self, longitude):
        """Calcule la distance en arcsecondes entre la longitude satellite et une longitude
                :return: entier positif égal à cette distance"""

        if abs(longitude - self.longitude) > self.max_deplacement_camera:
            """ Dans ce cas on passe par -648000 et 647999 en longitude """
            if longitude < self.longitude:
                dist_long = longitude + 1296000 - self.longitude
            else:
                dist_long = self.longitude + 1296000 - longitude
        else:
            dist_long = abs(self.longitude - longitude)

        return dist_long


# Tests des fonctions
if __name__ == "__main__":
    # Création d'un satellite
    s1 = Satellite(0, -320000, -648000, 0, 0, 5000)

    # Test distance_latitude. Attention : ne fonctionne pas après un passage par pôle, mais pas important
    lat = -50000
    y = s1.distance_latitude(lat)
    print("Distance entre " + str(lat) + " et " + str(s1.latitude) + " = " + str(y))

    #  Test distance_longitude
    long = 647950
    x = s1.distance_longitude(long)
    print("Distance entre " + str(long) + " et " + str(s1.longitude) + " = " + str(x))

    # Test range_deplacement_camera
    s2 = Satellite(0, 50, 100, 400, 50, 4000)
    print(str(s2.latitude), str(s2.longitude))
    s2.tour_suivant()
    print(str(s2.range_deplacement_camera))
