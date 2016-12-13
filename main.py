#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module d'entrée pour la mise en oeuvre du projet Poly#.
"""
from Classes.Interface import Interface
from Classes.Parseur import Parseur
from Classes.Distributeur import Distributeur
from Classes.Graphique import Graphique
from tkinter import *

import threading
import time

if __name__ == '__main__':

    #Creation interface au lancement
    
    interface_debut = Interface()
    interface_debut.creer_interface_lancement()

    #Execution du programme
    
    # Threads T1
    def thread_chargement():
        global fenetre_chargement
        fenetre_chargement = Tk()
        fenetre_chargement.configure(bg='white')
        label = Label(fenetre_chargement, text="...Chargement en cours, John Doe travaille...", bg='white',
                      font="Courier 16 bold")
        canvas = Canvas(fenetre_chargement, width=430, height=450)
        image_chargement = PhotoImage(file="C:\\Users\Mathilde\Desktop\projet2\docs\\John_Doe.png")
        canvas.create_image(50, 50, anchor=NW, image=image_chargement)
        label.pack()
        canvas.pack()
        canvas.configure(bg='white')

        fenetre_chargement.mainloop()

    # Threads T2
    def thread_programme():
        global temps_exec
        time.clock()
        parseur = Parseur(chemin_input='/donneesTest/' + interface_debut.fichier_input + '.in')
        nombre_tours, liste_satellites, liste_collections, globe = parseur.initialisation()
        distrib = Distributeur(nombre_tours, liste_satellites, liste_collections, globe)
        nb_photos_prises = distrib.algo_opti()
        parseur.creer_output(globe.liste_zones, nb_photos_prises)
        temps_exec = time.clock()

    # Création des Thread
    t1 = threading.Thread(target=thread_programme)
    t2 = threading.Thread(target=thread_chargement)

    # Démarrage des threads
    t1.start()
    t2.start()

    # Attente de terminaison des threads
    t1.join()
    fenetre_chargement.quit()
    t2.stop()
    time.sleep(2)

    #Creation interface après l'execution

    interface_debut.creer_interface_fin(temps_exec)

    if interface_debut.voir_simulation :
        parseur = Parseur('/donneesTest/' + interface_debut.fichier_input + '.in')
        nombre_tours, nombre_satellites, liste_satellites, liste_collections, globe = parseur.initialisation()
        liste_photos = parseur.recup_output()
        graphique = Graphique(nombre_tours, liste_satellites, None, liste_photos, globe.lat_zone)
        graphique.initialisation()

