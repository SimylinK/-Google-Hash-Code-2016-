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
        #  range_deplacement représente de combien on peut bouger dans chaque direction par rapport à la caméra
        self.range_deplacement_camera = [[self.vitesse_camera, self.vitesse_camera],
                                         [self.vitesse_camera, self.vitesse_camera]]

    def tour_suivant(self, latitude_cam=None, longitude_cam=None):
        """ Calcule la position suivante du satellite
        et la prochaine position de la caméra si besoin ( si les valeurs sont différentes de None)
        """
        # Déplacement du Satellite
        lat = self.latitude + self.vitesse
        long = self.longitude - 15
        # Passage au-dessus du pôle nord
        if lat > 324000:
            lat = 648000 - lat
            long -= 648000
            self.vitesse = -self.vitesse
        # Passage au-dessus du pôle sud
        elif lat < -324000:
            lat = -648000 - lat
            long += -648000
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
                lat_cam = 648000 - lat_cam
                long_cam -= 648000
            # Passage au-dessus du pôle sud
            elif lat_cam < -324000:
                lat_cam = -648000 - lat_cam
                long_cam += 648000
            # long est compris entre -648000 et 647999
            if long_cam < -648000:
                long_cam = 648000 - (-long_cam - 648000)

            self.latitude_camera = lat_cam
            self.longitude_camera = long_cam

    def distance_latitude(self, latitude):
        """Calcule l'écart entre le satellite et un point par rapport au satellite
        si positif, la latitude du satellite est supérieure à celle du point
        si négatif, la latitude du satellite est inférieure à celle du point
        :return: latitude, nombre entier"""
        # Pas besoin de tester les pôles car il n'y a pas de photo à plus de 85° N ou S.
        return self.latitude - latitude

    def distance_longitude(self,longitude):
        """Calcule l'écart entre le satellite et un point par rapport au satellite
            :return: longitude, nombre entier"""
        satellite = self.longitude

        if satellite >= 0:
            # Le satellite a une longitude positive ou nulle
            if longitude >= 0:
                # Le point a une longitude positive ou nulle
                dist_long = satellite - longitude
            else :
                # Le point a une longitude négative
                distance_absolue = min(abs(satellite - longitude),abs(648000 - satellite) + abs(-648000 - longitude))
                # Calcul de la plus courte distance entre passer par +180° ou pas
                if distance_absolue == abs(satellite - longitude):
                    # On ne passe pas par +180° pour aller du satellite au point
                    dist_long = satellite - longitude
                else:
                    # On passe par +180° pour aller du satellite au point
                    dist_long = -distance_absolue
        else:
            #  Le satellite a une longitude négative ou nulle
            if longitude <= 0:
                #  Le point a une longitude négative ou nulle
                dist_long = satellite - longitude
            else:
                # Le point a une longitude positive
                distance_absolue = min(abs(satellite - longitude), abs(-648000 - satellite) + abs(648000 - longitude))
                # Calcul de la plus courte distance entre passer par -180° ou pas
                if distance_absolue == abs(satellite - longitude):
                    #  On ne passe pas par -180° pour aller du satellite au point
                    dist_long = satellite - longitude
                else:
                    #  On passe par -180° pour aller du satellite au point
                    dist_long = distance_absolue

        return dist_long

    def distance_latitude_absolue(self, latitude):
        """Calcule la distance en arcsecondes entre la latitude satellite et une latitude
        :return: latitude, entier positif """
        # Pas besoin de tester les pôles car il n'y a pas de photo à plus de 85° N ou S.
        return abs(self.latitude - latitude)

    def distance_longitude_absolue(self, longitude):
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

    def reset_camera(self):
        """Méthode qui réinitialise range_deplacement_camera, à utiliser quand on prend une photo à un tour t"""
        self.range_deplacement_camera = [[0, 0],
                                         [0, 0]]
        self.update_camera()

    def update_camera(self):
        """Méthode qui met à jour range_deplacement_camera, à utiliser quand on ne prend pas de photo à un tour t"""
        max = self.max_deplacement_camera
        vitesse = self.vitesse_camera
        # Maximums de déplacement en fonction de la caméra
        lat_min = max - self.distance_latitude(self.latitude_camera)
        lat_max = max + self.distance_latitude(self.latitude_camera)
        long_min = max - self.distance_longitude(self.longitude_camera)
        long_max = max + self.distance_longitude(self.longitude_camera)

        if self.range_deplacement_camera[0][0] + vitesse > lat_min:
            self.range_deplacement_camera[0][0] = lat_min
        else:
            self.range_deplacement_camera[0][0] += vitesse

        if self.range_deplacement_camera[0][1] + vitesse > lat_max:
            self.range_deplacement_camera[0][1] = lat_max
        else:
            self.range_deplacement_camera[0][1] += vitesse

        if self.range_deplacement_camera[1][0] + vitesse > long_min:
            self.range_deplacement_camera[1][0] = long_min
        else:
            self.range_deplacement_camera[1][0] += vitesse

        if self.range_deplacement_camera[1][1] + vitesse > long_max:
            self.range_deplacement_camera[1][1] = long_max
        else:
            self.range_deplacement_camera[1][1] += vitesse


# Tests des fonctions
if __name__ == "__main__":
    # Création d'un satellite
    s1 = Satellite(0, 0, 647999, 0, 0, 5000)

    # Test distance_latitude. Attention : ne fonctionne pas après un passage par pôle, mais pas important
    lat = -50000
    y = s1.distance_latitude(lat)
    print("Latitude point par rapport à satellite : " + str(y))

    #  Test distance_longitude
    long = -648000
    x = s1.distance_longitude(long)
    print("Longitude point par rapport à satellite : " + str(x))

    # Test range_deplacement_camera
    s2 = Satellite(0, 0, 0, 100, 10, 20)
    print(str(s2.range_deplacement_camera))
    s2.update_camera()
    print(str(s2.range_deplacement_camera))
    s2.update_camera()  # Ici, ne va pas augmenter car il dépasserait le max
    print(str(s2.range_deplacement_camera))

    # Test update_camera avec tour_suivant
    print("-----------------------")
    s3 = Satellite(0, 0, 0, 100, 10, 50)
    s3.latitude_camera = 40
    s3.longitude_camera = 30
    print(str(s3.range_deplacement_camera))
    s3.update_camera()
    print(str(s3.range_deplacement_camera))
    s3.update_camera()
    print(str(s3.range_deplacement_camera))
    for i in range(500):
        s3.update_camera()
    print(str(s3.range_deplacement_camera))
    s3.reset_camera()
    print(str(s3.range_deplacement_camera))
    print("----------------------")
    s4 = Satellite(0, 0, -647975, -500, 0, 0)
    s4.tour_suivant()
    print(str(s4.latitude),str(s4.longitude))
    s4.tour_suivant()
    print(str(s4.latitude), str(s4.longitude))
    s4.tour_suivant()
    print(str(s4.latitude), str(s4.longitude))