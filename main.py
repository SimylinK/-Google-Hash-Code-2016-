#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module d'entrée pour la mise en oeuvre du projet Poly#.
"""

from Parseur import Parseur
from Distributeur import Distributeur

if __name__ == '__main__':
    parseur = Parseur()
    nombre_tours, nombre_satellites, liste_satellites, liste_collections = parseur.recup()
    distrib = Distributeur(nombre_tours, nombre_satellites, liste_satellites, liste_collections, parseur.liste_zones, parseur.LAT_ZONE, parseur.LONG_ZONE)
    nb_photos_prises = distrib.algo_opti()
    parseur.creer_output(parseur.liste_zones, nb_photos_prises)
