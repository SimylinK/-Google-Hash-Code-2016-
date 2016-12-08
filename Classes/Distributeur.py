#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from Satellite import Satellite


class Distributeur:
    """Classe chargée de :
    distribuer les photos entre les satellites et des les associer dans un calendrier
    """
    # Constantes :
    TAILLE_LAT = 648000  # Taille de la Terre en arcsecondes
    TAILLE_LONG = 1295999

    def __init__(self, nb_tours, nb_satellites, liste_satellites, liste_collections, liste_zones, LAT_ZONE, LONG_ZONE):
        self.nb_tours = nb_tours
        self.nb_satellites = nb_satellites
        self.liste_satellites = liste_satellites
        self.liste_collections = liste_collections  # Liste de toutes les collections
        self.liste_zones = liste_zones
        self.LAT_ZONE = LAT_ZONE # Calculés par parseur
        self.LONG_ZONE = LONG_ZONE
        self.NB_ZONES_LAT = math.ceil(self.TAILLE_LAT / LAT_ZONE)  # On ne compte pas la dernière zone plus petite
        self.NB_ZONES_LONG = math.ceil(self.TAILLE_LONG / LONG_ZONE)

    def algo_opti(self):
        """
        Méthode principale du programme
        celle qui va distribuer les photos aux satellites
        """
        print("Lancement de la simulation")
        nb_photos_prises = 0
        for tour in range(self.nb_tours):
            for satellite in self.liste_satellites:
                #  Pas de photo prise à plus de 85° Nord ou Sud = 36000 arcsecondes pour 10°
                #  On se contente d'update sa camera et de le faire avancer
                if satellite.latitude > 306000 or satellite.latitude < -306000:
                    satellite.update_camera()
                    satellite.tour_suivant()
                else:
                    # On prédit si on prend une photo au tour suivant
                    lat_choisie, long_choisie = self.prediction(satellite, tour)
                    if lat_choisie:
                        satellite.reset_camera()
                        nb_photos_prises += 1
                    else:
                        # Mise à jour de range_déplacement_camera
                        satellite.update_camera()
                    satellite.tour_suivant(lat_choisie, long_choisie)

        return nb_photos_prises

    def prediction(self, satellite, tour):
        """Méthode qui la latitude et la longitude de la meilleure photo atteignable au tour suivant pour un satellite et un tour donnés
        lat et long sont les indices de la zone dans laquelle se trouve le satellite"""

        # On crée un satellite intermédiaire
        sat = Satellite(satellite.id, satellite.latitude, satellite.longitude, satellite.vitesse, satellite.vitesse_camera, satellite.max_deplacement_camera)
        sat.range_deplacement_camera = satellite.range_deplacement_camera
        sat.latitude_camera = satellite.latitude_camera
        sat.longitude_camera = satellite.longitude_camera

        # On simule un avancement d'un tour de ce satellite
        sat.tour_suivant()

        #  Calcul de la Zone dans laquelle se trouve le satellite
        lat = (satellite.latitude + 324000) // self.LAT_ZONE
        if satellite.latitude == 324000:
            lat -= 1

        long = (satellite.longitude + 648000) // self.LONG_ZONE
        if satellite.longitude == 648000:
            long -= 1

        photos_prenables = []
        choix = False

        for photo in self.liste_zones[lat][long].photos_a_prendre:
            for intervalle in photo.collection.liste_intervalles:
                if intervalle[0] <= tour + 1 <= intervalle[1]:
                    # On teste si dans l'intervalle de mouvement qu'on avait, il y a une photo
                    if (sat.latitude_camera - sat.range_deplacement_camera[0][0] <= photo.latitude <= sat.latitude_camera +
                        sat.range_deplacement_camera[0][1] and sat.longitude_camera - sat.range_deplacement_camera[1][0]
                        <= photo.longitude <= sat.longitude_camera + sat.range_deplacement_camera[1][1]):
                        # La photo est bien prenable :
                        photos_prenables.append(photo)
                        choix = True

        if choix:
            photo_choisie = sorted(photos_prenables, key=lambda k: [k.collection.ratio_rentabilite], reverse=True)[0]
            photo_choisie.prise_par_id = satellite.id
            photo_choisie.prise_tour = tour + 1
            self.liste_zones[lat][long].photos_a_prendre.remove(photo_choisie)
            self.liste_zones[lat][long].photos_prises.append(photo_choisie)

            return photo_choisie.latitude, photo_choisie.longitude

        else:
            return None, None
