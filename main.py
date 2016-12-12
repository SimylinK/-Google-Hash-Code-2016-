#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module d'entrée pour la mise en oeuvre du projet Poly#.
"""

from Classes.Parseur import Parseur
from Classes.Distributeur import Distributeur
from Classes.Graphique import Graphique


if __name__ == '__main__':
    parseur = Parseur()
    nombre_tours, liste_satellites, liste_collections, globe = parseur.initialisation()
    distrib = Distributeur(nombre_tours, liste_satellites, liste_collections, globe)
    nb_photos_prises = distrib.algo_opti()
    parseur.creer_output(distrib.globe.liste_zones, nb_photos_prises)


    # Exécution de l'interface graphique pour lire un fichier output

    # liste_photos = parseur.recup_output()
    # graphique = Graphique(nombre_tours, liste_satellites, None, liste_photos, globe.lat_zone)
    # graphique.initialisation()


