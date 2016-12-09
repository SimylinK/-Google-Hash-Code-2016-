#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module d'entrée pour la mise en oeuvre du projet Poly#.
"""

from Parseur import Parseur
from Distributeur import Distributeur
import time

if __name__ == '__main__':
    time.clock()
    parseur = Parseur()
    nombre_tours, nombre_satellites, liste_satellites, liste_collections, globe = parseur.recup()
    distrib = Distributeur(nombre_tours, nombre_satellites, liste_satellites, liste_collections, globe)
    nb_photos_prises = distrib.algo_opti()
    parseur.creer_output(globe.liste_zones, nb_photos_prises)
    print("Le temps d'exécution fut de " + str(time.clock()) + " secondes")
