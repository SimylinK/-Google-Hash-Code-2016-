#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Imports servant à :
    - à réutiliser les classes définies dans les autres fichiers :
        import Collection : classe Collection
        import Satellite : classe Satellite.
"""

import math


class Distributeur:
    """Classe chargée de :
    distribuer les photos entre les satellites et des les associer dans un calendrier
    """
    # Constantes :
    LAT_ZONE = 5000  # Paramètres à changer pour modifier la taille des zones
    LONG_ZONE = 10000
    TAILLE_LAT = 648000  # Taille de la Terre en arcsecondes
    TAILLE_LONG = 1295999
    NB_ZONES_LAT = math.ceil(TAILLE_LAT / LAT_ZONE)  # On ne compte pas la dernière zone plus petite
    NB_ZONES_LONG = math.ceil(TAILLE_LONG / LONG_ZONE)

    def __init__(self, nb_tours, nb_satellites, liste_satellites, liste_collections, liste_zones):
        self.nb_tours = nb_tours
        self.nb_satellites = nb_satellites
        self.liste_satellites = liste_satellites
        self.liste_collections = liste_collections  # Liste de toutes les collections
        self.liste_zones = liste_zones

    def algo_opti(self):
        """
        Méthode principale du programme
        celle qui va distribuer les photos aux satellites
        """
        print("Lancement de la simulation")
        nb_photos_prises = 0
        for tour in range(self.nb_tours):
            for satellite in self.liste_satellites:
                #  Calcul de la Zone dans laquelle se trouve le satellite
                lat = math.floor(((satellite.latitude - 1) / self.LAT_ZONE)) + self.NB_ZONES_LAT // 2
                long = math.floor(((satellite.longitude - 1) / self.LONG_ZONE)) + self.NB_ZONES_LONG // 2

                #  On boucle donc sur les photos dans cette zone seulement
                for photo in self.liste_zones[lat][long].photos_a_prendre:
                    #  Vérification qu'on est dans l'intervalle
                    for intervalle in photo.collection.liste_intervalles:
                        """Pas besoin de trop de tests : on ne peut logiquement être que dans 1 intervalle
                        à la fois"""
                        if intervalle[0] <= tour <= intervalle[1]:
                            """On teste ensuite si la photo est là où est la caméra
                            Pour le moment : position caméra = position satellite"""
                            if (satellite.latitude_camera == photo.latitude and
                                    satellite.longitude_camera == photo.longitude):
                                photo.prise_par_id = satellite.id
                                photo.prise_tour = tour
                                self.liste_zones[lat][long].photos_a_prendre.remove(photo)
                                self.liste_zones[lat][long].photos_prises.append(photo)
                                nb_photos_prises += 1
                satellite.tour_suivant()

        return nb_photos_prises
