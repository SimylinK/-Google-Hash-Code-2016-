#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Classes.Satellite import Satellite


class Distributeur:
    """Classe chargée de :
    distribuer les photos entre les satellites et les associer dans un calendrier
    """

    def __init__(self, nb_tours, nb_satellites, liste_satellites, liste_collections, globe):
        self.nb_tours = nb_tours
        self.nb_satellites = nb_satellites
        self.liste_satellites = liste_satellites
        self.liste_collections = liste_collections  # Liste de toutes les collections
        self.globe = globe
        self.ratio_moyen = self.moyenne_ratio()
        self.seuil_ratio = self.ratio_moyen * 15 / 100

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
                    satellite.tour_suivant(lat_choisie, long_choisie)
                    if lat_choisie:
                        satellite.reset_camera()
                        nb_photos_prises += 1
                    else:
                        # Mise à jour de range_déplacement_camera
                        satellite.update_camera()

        return nb_photos_prises

    def prediction(self, satellite, tour):
        """Méthode qui renvoie  la latitude et la longitude de la meilleure photo atteignable au tour suivant pour un satellite et un tour donnés
        lat et long sont les indices de la zone dans laquelle se trouve le satellite"""

        # On crée un satellite intermédiaire
        sat = satellite.clone()

        # On simule un avancement d'un tour de ce satellite
        sat.tour_suivant()

        #  Calcul des indices de ce dernier dans liste_zones
        lat, long = self.globe.calcul_indice(sat)

        photos_prenables = []
        choix = False

        # On boucle sur toutes les photos qu'on peut prendre, donc celles de notre zone et de ses adjacentes
        photos_autour_zone = self.globe.photos_autour_zone(lat, long)

        for photo in photos_autour_zone:
            # On teste si dans l'intervalle de mouvement qu'on avait, il y a une photo
            if sat.peut_prendre(photo, tour):
                # La photo est bien prenable :
                if photo.collection.ratio_rentabilite > self.seuil_ratio:
                    photos_prenables.append(photo)
                    choix = True

        if choix:
            photo_choisie = sorted(photos_prenables, key=lambda k: [k.collection.ratio_rentabilite], reverse=True)[0]
            photo_choisie.prise_par_id = satellite.id
            photo_choisie.prise_tour = tour + 1

            # Calcul des indices de la photo choisie dans liste_zones
            photo_indice_lat, photo_indice_long = self.globe.calcul_indice(photo_choisie)

            self.globe.liste_zones[photo_indice_lat][photo_indice_long].photos_a_prendre.remove(photo_choisie)
            self.globe.liste_zones[photo_indice_lat][photo_indice_long].photos_prises.append(photo_choisie)

            return photo_choisie.latitude, photo_choisie.longitude

        else:
            return None, None

    def moyenne_ratio(self):
        somme = 0
        for collection in self.liste_collections:
            somme += collection.ratio_rentabilite
        somme /= len(self.liste_collections)
        return somme