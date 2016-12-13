#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy


class Distributeur:
    """Classe chargée de :
    Décider de l'action à effectuer pour chaque tour pour chaque satellite
    """

    def __init__(self, nb_tours, liste_satellites, liste_collections, globe):
        self.nb_tours = nb_tours
        self.liste_satellites = liste_satellites
        self.liste_collections = liste_collections  # Liste de toutes les collections
        self.globe = globe
        self.ratio_moyen = self.moyenne_ratio()
        self.seuil_ratio = self.ratio_moyen * 15 / 100  # Valeur fixée arbitrairement à 15 pourcents
        self.collections_partielles = []  # Liste de collections prises partiellement
        self.meilleures_petites_collections = []

    def algo_opti(self):
        """
        Méthode principale du programme
        celle qui va distribuer les photos aux satellites
        """
        print("Lancement de la simulation")

        # Initialisation
        completion_partielle = True
        dernier_tour = False
        iteration = 1
        nb_photos_prises = 0

        # On retire les collections qui sont sous le seuil
        for collection in self.liste_collections:
            if collection.ratio_rentabilite < self.seuil_ratio:
                for photo in collection.liste_photos:
                    indice_lat, indice_long = self.globe.calcul_indice(photo)
                    self.globe.liste_zones[indice_lat][indice_long].photos_a_prendre.remove(photo)

        """
        On exécute tant qu'il reste des collections prises partiellement.
        """
        while completion_partielle:
            # Réinitialisation
            nb_photos_prises = 0
            self.collections_partielles = []
            # Il faut réinitialiser les satellites, pour cela on les clone au tour 0
            liste_satellite_clone = copy.deepcopy(self.liste_satellites)
            if not dernier_tour:
                print('    Itération numéro ' + str(iteration) + " de l'algorithme")
            else:
                print("  Dernier tour de l'algorithme")

            # Il faut réinitialiser les collections, on les clone au tour 0
            liste_collection_clone = copy.deepcopy(self.liste_collections)

            # Pour le globe, on fait une deepcopy puis on remet les mêmes pointeurs aux photos
            globe_clone = copy.deepcopy(self.globe)
            i_lat = 0  # Les indices dans lesquels se trouvera le pointeur de photo
            i_long = 0
            i_photo = 0
            for liste_latitude in self.globe.liste_zones:
                for liste_longitude in liste_latitude:
                    for photo in liste_longitude.photos_a_prendre:
                        # On remet le bon pointeur dans cette case
                        globe_clone.liste_zones[i_lat][i_long].photos_a_prendre[i_photo] = photo
                        i_photo += 1
                    i_long += 1
                    i_photo = 0  # L'indice du pointeur de photo revient à 0 quand on change de case
                i_lat += 1
                i_long = 0  # L'indice de longitude dans le tableau revient à 0 quand on change de latitude

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
                            # Si on prend une photo, on remet la range camera au minimum
                            satellite.reset_camera()
                            nb_photos_prises += 1

                        else:
                            # On augmente la range de déplacement caméra
                            satellite.update_camera()

            """
            On regarde si des collections sont complétées partiellement et si oui les élimine
            """
            if len(self.collections_partielles) != 0:
                # On selectionne les collections à éliminer
                mauvaises_collections = self.collections_partielles
                for pire_collection in mauvaises_collections:
                    for pire_photo in pire_collection.liste_photos:
                        indice_lat, indice_long = self.globe.calcul_indice(pire_photo)
                        globe_clone.liste_zones[indice_lat][indice_long].photos_a_prendre.remove(pire_photo)

                # On remplace le globe et les listes actuels par les clones et on reboucle
                self.globe = globe_clone
                self.liste_satellites = liste_satellite_clone
                self.liste_collections = liste_collection_clone
                iteration += 1
            else:
                completion_partielle = False

        return nb_photos_prises

    def prediction(self, satellite, tour):
        """
        Méthode qui renvoie la latitude et la longitude de la meilleure photo atteignable au tour suivant pour un satellite et un tour donnés
        """

        """
        On clone le satellite
        Comme cette méthode est appelée une fois par satellite par tour, on n'utilise pas le module copy qui est lourd
        On préfère utiliser une méthode implémentée, le satellite n'ayant pas besoin d'un deepcopy
        """
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
                photos_prenables.append(photo)
                choix = True

        if choix:
            # On sélectionne la photo en prenant celle au meilleur ratio
            photo_choisie = sorted(photos_prenables, key=lambda k: [k.collection.ratio_rentabilite], reverse=True)[0]
            # On met à jour les informations de cette photo
            photo_choisie.prise_par_id = satellite.id
            photo_choisie.prise_tour = tour + 1
            # Calcul des indices de la photo choisie dans liste_zones
            photo_indice_lat, photo_indice_long = self.globe.calcul_indice(photo_choisie)

            self.globe.liste_zones[photo_indice_lat][photo_indice_long].photos_a_prendre.remove(photo_choisie)
            self.globe.liste_zones[photo_indice_lat][photo_indice_long].photos_prises.append(photo_choisie)

            # On ajoute la collection à collections_partielles si elle n'y était pas encore
            if photo_choisie.collection not in self.collections_partielles:
                self.collections_partielles.append(photo_choisie.collection)
            # On fait deux choses à la fois : on update et on teste si la collection est complete
            if photo_choisie.collection.update():
                self.collections_partielles.remove(photo_choisie.collection)

            return photo_choisie.latitude, photo_choisie.longitude

        else:
            return None, None

    def moyenne_ratio(self):
        """Calcule la moyenne du ratio des collections"""
        somme = 0
        for collection in self.liste_collections:
            somme += collection.ratio_rentabilite
        somme /= len(self.liste_collections)
        return somme
