#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy


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
        self.seuil_ratio = self.ratio_moyen * 15 / 100  # Valeur fixée arbitrairement à 15 pourcents
        self.collections_partielles = []  # Liste de collections prises partiellement

    def algo_opti(self):
        """
        Méthode principale du programme
        celle qui va distribuer les photos aux satellites
        """
        print("Lancement de la simulation")

        # On retire les photos qui sont sous le seuil
        for collection in self.liste_collections:
            if collection.ratio_rentabilite < self.seuil_ratio:
                for photo in collection.liste_photos:
                    indice_lat, indice_long = self.globe.calcul_indice(photo)
                    self.globe.liste_zones[indice_lat][indice_long].photos_a_prendre.remove(photo)

        # Ici, on exécute tant qu'il reste des collections prises partiellement
        completion_partielle = True
        iteration = 1
        max_iterations = 3  # Nombre maximal de fois que l'algorithme entrera dans le while
        collections_a_eliminer = 1  # Nombre de collections éliminées à chaque itération
        while completion_partielle:
            # Réinitialisation
            tour = 0
            nb_photos_prises = 0
            self.collections_partielles = []
            # Il faut réinitialiser les satellites, pour cela on les clone au tour 0
            liste_satellite_clone = copy.deepcopy(self.liste_satellites)
            print('Itération numéro ' + str(iteration) + " de l'algorithme")

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
                        globe_clone.liste_zones[i_lat][i_long].photos_a_prendre[i_photo] = photo  # On remet le bon pointeur
                        globe_clone.liste_zones[i_lat][i_long].photos_prises = []  # On efface les photos prises
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
                            satellite.reset_camera()
                            nb_photos_prises += 1

                        else:
                            # Mise à jour de range_déplacement_camera
                            satellite.update_camera()

            #  On regarde si des collections sont complétées partiellement et si oui on élimine la pire, sinon on termine l'algorithme
            if len(self.collections_partielles) != 0 and iteration < max_iterations:
                pire_collections = sorted(self.collections_partielles, key=lambda k: [k.ratio_rentabilite])[:collections_a_eliminer]  # On selectionne le nombre de collections à éliminer
                for pire_collection in pire_collections:
                    for pire_photo in pire_collection.liste_photos:
                        indice_lat, indice_long = self.globe.calcul_indice(pire_photo)
                        globe_clone.liste_zones[indice_lat][indice_long].photos_a_prendre.remove(pire_photo)
                self.globe = globe_clone  # Le globe est remplacé par celui sans les photos indésirables et on reboucle
                self.liste_satellites = liste_satellite_clone
                self.liste_collections = liste_collection_clone
                iteration += 1
            else:
                completion_partielle = False

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
        somme = 0
        for collection in self.liste_collections:
            somme += collection.ratio_rentabilite
        somme /= len(self.liste_collections)
        return somme
