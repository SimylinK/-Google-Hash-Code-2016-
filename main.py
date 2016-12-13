#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Imports servant à instancier les classes
"""
from Classes.Interface import Interface
from Classes.Parseur import Parseur
from Classes.Distributeur import Distributeur
from Classes.Graphique import Graphique

"""
    Module d'entrée pour la mise en oeuvre du projet.
"""

if __name__ == '__main__':

    # Creation interface au lancement
    
    interface_debut = Interface()
    interface_debut.creer_interface_lancement()

    # Execution du programme

    parseur = Parseur(chemin_input='/donneesTest/' + interface_debut.fichier_input + '.in')
    nombre_tours, liste_satellites, liste_collections, globe = parseur.initialisation()
    distrib = Distributeur(nombre_tours, liste_satellites, liste_collections, globe)
    nb_photos_prises = distrib.algo_opti()
    parseur.creer_output(globe.liste_zones, nb_photos_prises)

    # Creation interface après l'execution

    interface_debut.creer_interface_fin(parseur.temps_exec)
    print(interface_debut.voir_simulation)

    if interface_debut.voir_simulation :
        parseur = Parseur('/donneesTest/' + interface_debut.fichier_input + '.in')
        nombre_tours, liste_satellites, liste_collections, globe = parseur.initialisation()
        liste_photos = parseur.recup_output()
        graphique = Graphique(nombre_tours, liste_satellites, None, liste_photos, globe.lat_zone)
        graphique.initialisation()

