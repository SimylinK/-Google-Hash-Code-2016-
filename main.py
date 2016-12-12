#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module d'entrée pour la mise en oeuvre du projet Poly#.
"""
from Classes.Interface import Interface
from Classes.Parseur import Parseur
from Classes.Distributeur import Distributeur
from Classes.Graphique import Graphique
import time

if __name__ == '__main__':

    #Creation interface au lancement
    interface = Interface("docs/Logo_polyhash_code_signe.png")
    interface.creer_interface_lancement()


    #Execution du programme

    # time.clock()
    # parseur = Parseur('/donneesTest/' + interface.fichier_input + '.in')
    # nombre_tours, nombre_satellites, liste_satellites, liste_collections, globe = parseur.initialisation()
    # distrib = Distributeur(nombre_tours, nombre_satellites, liste_satellites, liste_collections, globe)
    # nb_photos_prises = distrib.algo_opti()
    # parseur.creer_output(globe.liste_zones, nb_photos_prises)
    # temps_exec = time.clock()
    # if temps_exec <= 60:
    #     print("Le temps d'exécution fut de " + str(temps_exec) + " secondes")
    # else:
    #     print("Le temps d'exécution fut de " + str(temps_exec/60) + " minutes")

    # Exécution de l'interface graphique pour lire un fichier output

    #Creation interface après l'execution

    # if voir_simulation == True:
    #     liste_photos = parseur.recup_output()
    #     graphique = Graphique(nombre_tours, liste_satellites, None, liste_photos)
    #     graphique.initialisation()
