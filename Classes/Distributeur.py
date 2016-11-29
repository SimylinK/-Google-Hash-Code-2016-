#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Imports servant à :
    - à réutiliser les classes définies dans les autres fichiers :
        import Collection : classe Collection
        import Satellite : classe Satellite.
"""

from Collection import Collection
from Satellite import Satellite


class Distributeur:
    """Classe chargée de :
    distribuer les photos entre les satellites et des les associer dans un calendrier
    """

    def __init__(self, nb_tours, nb_satellites, liste_satellites, liste_collections):
        self.nb_tours = nb_tours
        self.nb_satellites = nb_satellites
        self.liste_satellites = liste_satellites
        self.liste_collections = liste_collections  # Liste de toutes les collections
        self.liste_collections_choisies = []  # Liste des collections sélectionnées
        self.calendrierPossibilite = []

    def choix_collections(self):
        """
        Méthode qui permet d'ordonner les collections par importance
        """
        self.liste_collections_choisies = sorted(self.liste_collections, key=lambda x: x.ratio_rentabilite, reverse=True)

        return self.liste_collections_choisies

    def creer_calendrier(self, tour, longitude, latitude, photo):
        """
        :param tour:
        :param longitude:
        :param latitude:
        :param photo:

        Méthode qui permet d'instancier un calendrier
        """
        return calendrier

    def ecrire_output(self):
        """
        Méthode qui permet d'obtenir le calendrier sous forme de chaine de caractères pour l'écrire dans un fichier
        """
        return output

    def algo_opti(self):
        """
        Méthode principale du programme
        celle qui va distribuer les photos aux satellites
        """
        return None
