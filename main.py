#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module d'entrée pour la mise en oeuvre du projet Poly#.
"""

from Classes.Parseur import Parseur
from Classes.Distributeur import Distributeur


if __name__ == '__main__':
    parseur = Parseur('/donneesTest/constellation.in')
    nombre_tours, nombre_satellites, liste_satellites, liste_collections, globe = parseur.initialisation()
    distrib = Distributeur(nombre_tours, nombre_satellites, liste_satellites, liste_collections, globe)
    nb_photos_prises = distrib.algo_opti()
    parseur.creer_output(distrib.globe.liste_zones, nb_photos_prises)
