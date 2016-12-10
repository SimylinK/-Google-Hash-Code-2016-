#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module d'entrée pour la mise en oeuvre du projet Poly#.
"""

from Classes.Parseur import Parseur
from Classes.Distributeur import Distributeur
import time

if __name__ == '__main__':
    time.clock()
    parseur = Parseur('/donneesTest/weekend.in')
    nombre_tours, nombre_satellites, liste_satellites, liste_collections, globe = parseur.initialisation()
    distrib = Distributeur(nombre_tours, nombre_satellites, liste_satellites, liste_collections, globe)
    nb_photos_prises = distrib.algo_opti()
    parseur.creer_output(globe.liste_zones, nb_photos_prises)
    temps_exec = time.clock()
    if temps_exec <= 60:
        print("Le temps d'exécution fut de " + str(temps_exec) + " secondes")
    else:
        print("Le temps d'exécution fut de " + str(temps_exec/60) + " minutes")
