#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module d'entrée pour la mise en oeuvre du projet Poly#.
"""

from Classes.Parseur import Parseur
from Classes.Distributeur import Distributeur
from Classes.Graphique import Graphique
import time

if __name__ == '__main__':
    time.clock()
    parseur = Parseur()
    nombre_tours, nombre_satellites, liste_satellites, liste_collections, globe = parseur.recup()
    liste_photos = parseur.recup_output()
    distrib = Distributeur(nombre_tours, nombre_satellites, liste_satellites, liste_collections, globe)
    nb_photos_prises = distrib.algo_opti()
    parseur.creer_output(globe.liste_zones, nb_photos_prises)
    temps_exec = time.clock()
    if temps_exec <= 60:
        print("Le temps d'exécution fut de " + str(temps_exec) + " secondes")
    else:
        print("Le temps d'exécution fut de " + str(temps_exec/60) + " minutes")


    # Exécution de l'interface graphique pour lire un fichier output

    # graphique = Graphique(nombre_tours, liste_satellites, None, liste_photos)
    # graphique.initialisation()
