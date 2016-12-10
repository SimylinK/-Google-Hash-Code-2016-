#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Classes.Photo import Photo


class ZoneGlobe:
    """Classe représentant une zone de la planète.

        Attributs :
        id_lat, id_long : Servent à identifier la zone dans la grille construite
        latitude_min - latitude_max : plage de latitude couverte
        longitude_min - longitude_max : plage de longitudes converte
        photos_a_prendre : liste de photos se trouvant dans la zone et n'étant pas encore prises
        photos_prises : liste de photos se trouvant dans la zone et étant déjà prises"""

    def __init__(self, latitude_min, latitude_max, longitude_min, longitude_max):
        self.latitude_min = latitude_min
        self.latitude_max = latitude_max
        self.longitude_min = longitude_min
        self.longitude_max = longitude_max
        self.photos_a_prendre = []
        self.photos_prises = []

    def ajouter_photo(self, photo):
        self.photos_a_prendre.append(photo)


if __name__ == "__main__":
    # Création d'une ZoneGlobe
    zg = ZoneGlobe(-20000, 20000, -20000, 20000)

    # Test de la méthode ajouter_photo
    zg.ajouter_photo(Photo(19500, -5042, None))
