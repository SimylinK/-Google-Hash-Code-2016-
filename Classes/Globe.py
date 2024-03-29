#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Classes.ZoneGlobe import ZoneGlobe
import math


class Globe:
    """Classe chargée de partitionner le globe et de stocker chaque partition (zone) dans une liste de liste : liste_zones."""
    def __init__(self, cote_zone):
        """
        :param cote_zone: Le côté des zones.
        """
        self.lat_zone = cote_zone
        self.long_zone = cote_zone
        self.taille_lat = 648000  # Taille totale de la Terre en latitude
        self.taille_long = 1295999  # Taille totale de la Terre en longitude
        self.nb_zones_lat = math.ceil(self.taille_lat / self.lat_zone)  # Nombre de zones dans chaque "ligne".
        self.nb_zones_long = math.ceil(self.taille_long / self.long_zone)   # Nombre de zones dans chaque "colonne".
        self.liste_zones = self.creation_zones()

    def creation_zones(self):
        """Méthode chargée de créer les différentes zones du globe"""
        # IDEE réutilisée par la suite: (lat(objet) + 324000)// lat_zone = indice en latitude dans liste_zones
        print("Création des zones")
        reste_lat = self.taille_lat % self.lat_zone
        reste_long = self.taille_long % self.long_zone

        liste_zones = []  # Liste de listes de zones. Tous les éléments d'une sous-liste possèdent la même latitude

        #  On crée les zones de taille cote_zone
        for i in range(-324000, 324000 - reste_lat, self.lat_zone):
            liste_longitude = []
            for j in range(-648000, 647999 - reste_long, self.long_zone):
                liste_longitude.append(ZoneGlobe(i, i + self.lat_zone, j, j + self.long_zone))
            liste_zones.append(liste_longitude)

        # S'il reste des zones de tailles inférieures, on les ajoute ici
        if reste_lat != 0:
            # On boucle sur la longitude, on ajoute donc une nouvelle sous-liste:
            liste_ajoutee = []
            for i in range(-648000, 647999, self.long_zone):
                if i + self.long_zone > 647999:
                    liste_ajoutee.append(ZoneGlobe(324000 - reste_lat, 324000, i, 647999))
                else:
                    liste_ajoutee.append(ZoneGlobe(324000 - reste_lat, 324000, i, i + self.long_zone))
            liste_zones.append(liste_ajoutee)

        if reste_long != 0:
            # On ajoute à la fin de chaque sous-liste la dernière zone
            indice = 0
            for i in range(-324000, 324000, self.lat_zone):
                if i + self.lat_zone > 324000:
                    liste_zones[indice].append(ZoneGlobe(i, 324000, 647999 - reste_long, 647999))
                else:
                    liste_zones[indice].append(ZoneGlobe(i, i + self.lat_zone, 647999 - reste_long, 647999))
                indice += 1

        # Pour éviter d'ajouter deux fois la case de latitude et longitude maximales:
        if reste_lat != 0 and reste_long != 0:
            liste_zones[self.nb_zones_lat - 1].pop()

        return liste_zones

    def calcul_indice(self, objet):
        """
        Méthode qui calcule les indices d'un objet dans liste_zones en fonction de ses coordonnées
        :param objet: Une instance de classe possédant une latitude et une longitude
        :return: indice_lat, indice_long : deux entiers
        """

        indice_lat = (objet.latitude + 324000) // self.lat_zone
        if objet.latitude == 324000:
            indice_lat -= 1
        indice_long = (objet.longitude + 648000) // self.long_zone
        if objet.longitude == 647999:
            indice_long -= 1
        return indice_lat, indice_long

    def photos_autour_zone(self, indice_lat, indice_long):
        """
        Méthode qui renvoie la liste des photos comprises dans une zone et ses adjacentes (les 8 autour).
        :param indice_lat: indice en latitude de la zone
        :param indice_long: indice en longitude de la zone
        :return: liste_photos: Une liste d'instances de la classe photo.
        """
        liste_photos = list(self.liste_zones[indice_lat][indice_long].photos_a_prendre)
        # indices maximaux de liste_zones
        max_lat = self.nb_zones_lat - 1
        max_long = self.nb_zones_long - 1

        if indice_lat == 0:
            # Coin bas gauche
            # On prend les indices finaux en latitude pour zones en-dessous
            if indice_long == 0:
                # On prend les indices finaux en longitude pour zones à gauche
                liste_photos += self.liste_zones[1][0].photos_a_prendre  # zone au-dessus
                liste_photos += self.liste_zones[1][1].photos_a_prendre  # zone au-dessus à droite
                liste_photos += self.liste_zones[0][1].photos_a_prendre  # zone à droite
                liste_photos += self.liste_zones[max_lat][1].photos_a_prendre  # en bas à droite
                liste_photos += self.liste_zones[max_lat][0].photos_a_prendre  # en bas
                liste_photos += self.liste_zones[max_lat][max_long].photos_a_prendre  # en bas à gauche
                liste_photos += self.liste_zones[0][max_long].photos_a_prendre  # zone à gauche
                liste_photos += self.liste_zones[1][max_long].photos_a_prendre  # zone au-dessus à gauche

                # Coin bas droit
            elif indice_long == max_long:
                # On prend les indices de début en longitude pour les zones à droite
                liste_photos += self.liste_zones[1][indice_long].photos_a_prendre  # zone au-dessus
                liste_photos += self.liste_zones[1][0].photos_a_prendre  # zone au-dessus à droite
                liste_photos += self.liste_zones[0][0].photos_a_prendre  # zone à droite
                liste_photos += self.liste_zones[max_lat][0].photos_a_prendre  # en bas à droite
                liste_photos += self.liste_zones[max_lat][indice_long].photos_a_prendre  # en bas
                liste_photos += self.liste_zones[max_lat][indice_long - 1].photos_a_prendre  # en bas à gauche
                liste_photos += self.liste_zones[0][indice_long - 1].photos_a_prendre  # zone à gauche
                liste_photos += self.liste_zones[1][indice_long - 1].photos_a_prendre  # zone au-dessus à gauche

                # Bord bas
            else:
                liste_photos += self.liste_zones[1][indice_long].photos_a_prendre  # zone au-dessus
                liste_photos += self.liste_zones[1][indice_long + 1].photos_a_prendre  # zone au-dessus à droite
                liste_photos += self.liste_zones[0][indice_long + 1].photos_a_prendre  # zone à droite
                liste_photos += self.liste_zones[max_lat][indice_long + 1].photos_a_prendre  # en bas à droite
                liste_photos += self.liste_zones[max_lat][indice_long].photos_a_prendre  # en bas
                liste_photos += self.liste_zones[max_lat][indice_long - 1].photos_a_prendre  # en bas à gauche
                liste_photos += self.liste_zones[0][indice_long - 1].photos_a_prendre  # zone à gauche
                liste_photos += self.liste_zones[1][indice_long - 1].photos_a_prendre  # zone au-dessus à gauche

        elif indice_lat == max_lat:
            #  Coin haut gauche
            #  On prend l'indice 0 en latitude pour les zones au-dessus
            if indice_long == 0:
                #  On prend les indices finaux en longitude pour les zones à gauche
                liste_photos += self.liste_zones[0][0].photos_a_prendre  # zone au-dessus
                liste_photos += self.liste_zones[0][1].photos_a_prendre  # zone au-dessus à droite
                liste_photos += self.liste_zones[indice_lat][1].photos_a_prendre  # zone à droite
                liste_photos += self.liste_zones[indice_lat - 1][1].photos_a_prendre  # en bas à droite
                liste_photos += self.liste_zones[indice_lat - 1][0].photos_a_prendre  # en bas
                liste_photos += self.liste_zones[indice_lat - 1][max_long].photos_a_prendre  # en bas à gauche
                liste_photos += self.liste_zones[indice_lat][max_long].photos_a_prendre  # zone à gauche
                liste_photos += self.liste_zones[0][max_long].photos_a_prendre  # zone au-dessus à gauche

            # Coin haut droit
            elif indice_long == max_long:
                # On prend les indices de début en longitude pour les zones à droite
                liste_photos += self.liste_zones[0][indice_long].photos_a_prendre  # zone au-dessus
                liste_photos += self.liste_zones[0][0].photos_a_prendre  # zone au-dessus à droite
                liste_photos += self.liste_zones[indice_lat][0].photos_a_prendre  # zone à droite
                liste_photos += self.liste_zones[indice_lat - 1][0].photos_a_prendre  # en bas à droite
                liste_photos += self.liste_zones[indice_lat - 1][indice_long].photos_a_prendre  # en bas
                liste_photos += self.liste_zones[indice_lat - 1][indice_long - 1].photos_a_prendre  # en bas à gauche
                liste_photos += self.liste_zones[indice_lat][indice_long - 1].photos_a_prendre  # zone à gauche
                liste_photos += self.liste_zones[0][indice_long - 1].photos_a_prendre  # zone au-dessus à gauche

            # Bord haut
            else:
                liste_photos += self.liste_zones[0][indice_long].photos_a_prendre  # zone au-dessus
                liste_photos += self.liste_zones[0][indice_long + 1].photos_a_prendre  # zone au-dessus à droite
                liste_photos += self.liste_zones[indice_lat][indice_long + 1].photos_a_prendre  # zone à droite
                liste_photos += self.liste_zones[indice_lat - 1][indice_long + 1].photos_a_prendre  # en bas à droite
                liste_photos += self.liste_zones[indice_lat - 1][indice_long].photos_a_prendre  # en bas
                liste_photos += self.liste_zones[indice_lat - 1][indice_long - 1].photos_a_prendre  # en bas à gauche
                liste_photos += self.liste_zones[indice_lat][indice_long - 1].photos_a_prendre  # zone à gauche
                liste_photos += self.liste_zones[0][indice_long - 1].photos_a_prendre  # zone au-dessus à gauche

        # Bord gauche
        elif indice_long == 0:
            #  On prend les indices finaux en longitude pour les zones à gauche
            liste_photos += self.liste_zones[indice_lat + 1][0].photos_a_prendre  # zone au-dessus
            liste_photos += self.liste_zones[indice_lat + 1][1].photos_a_prendre  # zone au-dessus à droite
            liste_photos += self.liste_zones[indice_lat][1].photos_a_prendre  # zone à droite
            liste_photos += self.liste_zones[indice_lat - 1][1].photos_a_prendre  # en bas à droite
            liste_photos += self.liste_zones[indice_lat - 1][0].photos_a_prendre  # en bas
            liste_photos += self.liste_zones[indice_lat - 1][max_long].photos_a_prendre  # en bas à gauche
            liste_photos += self.liste_zones[indice_lat][max_long].photos_a_prendre  # zone à gauche
            liste_photos += self.liste_zones[indice_lat + 1][max_long].photos_a_prendre  # zone au-dessus à gauche

        # Bord droit
        elif indice_long == max_long:
            # On prend les indices de début en longitude pour les zones à droite
            liste_photos += self.liste_zones[indice_lat + 1][indice_long].photos_a_prendre  # zone au-dessus
            liste_photos += self.liste_zones[indice_lat + 1][0].photos_a_prendre  # zone au-dessus à droite
            liste_photos += self.liste_zones[indice_lat][0].photos_a_prendre  # zone à droite
            liste_photos += self.liste_zones[indice_lat - 1][0].photos_a_prendre  # en bas à droite
            liste_photos += self.liste_zones[indice_lat - 1][indice_long].photos_a_prendre  # en bas
            liste_photos += self.liste_zones[indice_lat - 1][indice_long - 1].photos_a_prendre  # en bas à gauche
            liste_photos += self.liste_zones[indice_lat][indice_long - 1].photos_a_prendre  # zone à gauche
            liste_photos += self.liste_zones[indice_lat + 1][indice_long - 1].photos_a_prendre  # zone au-dessus à gauche

        # Cas général sans problème de bornes
        else:
            liste_photos += self.liste_zones[indice_lat + 1][indice_long].photos_a_prendre  # zone au-dessus
            liste_photos += self.liste_zones[indice_lat + 1][indice_long + 1].photos_a_prendre  # zone au-dessus à droite
            liste_photos += self.liste_zones[indice_lat][indice_long + 1].photos_a_prendre  # zone à droite
            liste_photos += self.liste_zones[indice_lat - 1][indice_long + 1].photos_a_prendre  # en bas à droite
            liste_photos += self.liste_zones[indice_lat - 1][indice_long].photos_a_prendre  # en bas
            liste_photos += self.liste_zones[indice_lat - 1][indice_long - 1].photos_a_prendre  # en bas à gauche
            liste_photos += self.liste_zones[indice_lat][indice_long - 1].photos_a_prendre  # zone à gauche
            liste_photos += self.liste_zones[indice_lat + 1][indice_long - 1].photos_a_prendre  # zone au-dessus à gauche

        return liste_photos
