#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from Satellite import Satellite


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
                lat_choisie, long_choisie = self.prediction(satellite, tour, lat, long)
                if lat_choisie:
                    satellite.vitesse_camera_relative = satellite.vitesse_camera
                else:
                    satellite.vitesse_camera_relative += satellite.vitesse_camera
                satellite.tour_suivant(lat_choisie, long_choisie)
        return nb_photos_prises

    def prediction(self, satellite, tour, lat, long):
        # On simule un avancement d'un tour du satellite
        sat = Satellite(satellite.id, satellite.latitude, satellite.longitude, satellite.vitesse,
                        satellite.vitesse_camera_relative, satellite.max_deplacement_camera)
        sat.latitude_camera = satellite.latitude_camera
        sat.longitude_camera = satellite.longitude_camera
        sat.tour_suivant()
        photos_prenables = []
        choix = False
        # Mêmes tests que plus haut
        for photo in self.liste_zones[lat][long].photos_a_prendre:
            for intervalle in photo.collection.liste_intervalles:
                if intervalle[0] <= tour + 1 <= intervalle[1]:
                    # On teste si dans l'intervalle de mouvement qu'on avait, il y a une photo
                    if (sat.latitude_camera - sat.vitesse_camera <= photo.latitude <= sat.latitude_camera + sat.vitesse_camera
                        and sat.longitude_camera - sat.vitesse_camera <= photo.longitude <= sat.latitude_camera + sat.vitesse_camera
                        and sat.latitude - sat.max_deplacement_camera <= photo.latitude <= sat.latitude + sat.max_deplacement_camera
                        and sat.longitude - sat.max_deplacement_camera <= photo.longitude <= sat.longitude + sat.max_deplacement_camera):
                        # La photo est bien prenable :
                        photos_prenables.append(photo)
                        choix = True
        if choix:
            photo_choisie = sorted(photos_prenables, key=lambda k: [k.collection.ratio_rentabilite], reverse=True)[0]
            return photo_choisie.latitude, photo_choisie.longitude

        else:
            return None, None
