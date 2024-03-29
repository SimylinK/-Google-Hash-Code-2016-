#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Imports servant à :
    - à réutiliser les classes définies dans les autres fichiers :
        import Photo : classe Photo
        import Collection : classe Collection
        import Satellite : classe Satellite
        import ZoneGlobe : classe ZoneGlobe
    - à aider à la simulation :
        import os : Permet d'obtenir le répertoire de travail actuel de l'utilisateur
        import time : Permet de calculer le temps de simulation
"""

import os
import time

from Classes.Collection import Collection
from Classes.Globe import Globe
from Classes.Photo import Photo
from Classes.Satellite import Satellite


class Parseur:
    """
    Classe chargée de :
    Transformer le fichier d'input en informations utilisables : variables et instances de classes.
    Écrire le fichier output.
    """

    # Constantes :
    REPERTOIRE = os.getcwd()

    def __init__(self, chemin_input=None):
        """
        :param chemin_input: donne le chemin du fichier d'input
        """
        self.chemin_output = self.REPERTOIRE + '/fichier_output.out'
        self.chemin_input = self.REPERTOIRE + chemin_input
        self.temps_exec = 0

    def initialisation(self):
        """
        Méthode chargée de :
        Récupérer les informations du fichier d'input et de les transformer en instances
        de classes.
        Créer le globe et la liste des zones.
        """
        time.clock()
        print("Lecture du fichier d'input")
        fichier_input = open(self.chemin_input, 'r')
        nb_tours = int(fichier_input.readline().rstrip())  # rstrip est utilisé pour ne pas prendre "\n" en compte.
        nb_satellites = int(fichier_input.readline().rstrip())

        liste_satellites = []  # On transforme chaque ligne en une instance de la classe Satellite
        id = 0
        max_deplacement = 0  # Sert à calculer le max_déplacement_satellite sur tous les satellites
        for i in range(0, nb_satellites):
            chaine = fichier_input.readline().rstrip()
            satellite = self.satellite_par_chaine(id, chaine)
            liste_satellites.append(satellite)
            id += 1
            if satellite.max_deplacement_camera > max_deplacement:
                max_deplacement = satellite.max_deplacement_camera

        # On crée le globe (avec les zones)
        globe = Globe(max_deplacement)

        # On transforme les lignes suivantes en instances des classes Photo et Collection
        nb_collections = int(fichier_input.readline().rstrip())
        liste_collections = []  # Liste qui contiendra les collections
        for i in range(nb_collections):  # On fait l'opération sur toutes les collections
            chaine_collection = fichier_input.readline().rstrip()
            collection = self.collection_par_chaine(chaine_collection)
            for j in range(collection.nb_photos):  # À chaque collection, on ajoute ses photos
                chaine_photo = (fichier_input.readline().rstrip())
                photo = self.photo_par_chaine(chaine_photo, collection)
                # On calcule les indices de la photo dans liste_zones
                indice_lat, indice_long = globe.calcul_indice(photo)
                # On ajoute cette photo à la zone correspondante
                globe.liste_zones[indice_lat][indice_long].ajouter_photo(photo)
                collection.ajouter_photo(photo)
            for k in range(collection.nb_intervalles):  # À chaque collection, on ajoute ses intervalles
                chaine_intervalle = (fichier_input.readline().rstrip())
                intervalle = self.intervalle_par_chaine(chaine_intervalle)
                collection.ajouter_intervalle(intervalle)
            liste_collections.append(collection)
        fichier_input.close()

        return nb_tours, liste_satellites, liste_collections, globe

    def photo_par_chaine(self, caracteres, collection):
        """Transforme une ligne du fichier input en une instance de la classe Photo"""
        liste_arguments = [1, 2]
        num_liste = 0
        argument = ""
        for i in range(len(caracteres)):
            if caracteres[i] != " ":
                argument += caracteres[i]
            else:  # Ici, l'argument est ajouté à liste_arguments
                liste_arguments[num_liste] = int(argument)  # On doit transformer chaque information en entier
                num_liste += 1
                argument = ""
        liste_arguments[num_liste] = int(argument)  # On ajoute le dernier

        return Photo(liste_arguments[0], liste_arguments[1], collection)

    def collection_par_chaine(self, caracteres):
        """
        Transforme une ligne du fichier input en une instance de la classe Collection
        :param caracteres: une chaine de caractères
        :return: Une instance de la classe Collection
        """
        liste_arguments = [1, 2, 3]
        num_liste = 0
        argument = ""
        for i in range(len(caracteres)):
            if caracteres[i] != " ":
                argument += caracteres[i]
            else:  # Ici, l'argument est ajouté à liste_arguments
                liste_arguments[num_liste] = int(argument)  # On doit transformer chaque information en entier
                num_liste += 1
                argument = ""
        liste_arguments[num_liste] = int(argument)  # On ajoute le dernier

        return Collection(liste_arguments[0], liste_arguments[1], liste_arguments[2])

    def intervalle_par_chaine(self, caracteres):
        """
        Transforme une ligne du fichier input en un intervalle
        :param caracteres: une chaine de caractères
        :return: intervalle : liste de deux entiers
        """
        liste_arguments = [1, 2]
        num_liste = 0
        argument = ""
        for i in range(len(caracteres)):
            if caracteres[i] != " ":
                argument += caracteres[i]
            else:  # Ici, l'argument est ajouté à liste_arguments
                liste_arguments[num_liste] = int(argument)  # On doit transformer chaque information en entier
                num_liste += 1
                argument = ""
        liste_arguments[num_liste] = int(argument)  # On ajoute le dernier

        return [liste_arguments[0], liste_arguments[1]]

    def satellite_par_chaine(self, id, caracteres):
        """"
        Transforme une ligne du fichier input en une instance de la classe Satellite
        :param caracteres: une chaine de caractères
        :return: Une instance de la classe Satellite
        """
        liste_arguments = [1, 2, 3, 4, 5,
                           ]  # On doit donner 5 arguments à Satellite pour la création d'une instance
        num_liste = 0  # ième argument de la liste
        argument = ""
        for j in range(len(caracteres)):
            if caracteres[j] != " ":
                argument += caracteres[j]
            else:  # Ici, l'argument est ajouté à liste_arguments
                liste_arguments[num_liste] = int(argument)  # On doit transformer chaque information en entier
                num_liste += 1
                argument = ""
        liste_arguments[num_liste] = int(argument)  # On ajoute le dernier

        return Satellite(id, liste_arguments[0], liste_arguments[1], liste_arguments[2], liste_arguments[3],
                         liste_arguments[4])

    def ligne_output_par_chaine(self, caracteres):
        """"
        Transforme une ligne du fichier output en une liste de 4 éléments
        :param caracteres: une chaine de caractères
        :return: liste de 4 arguments stockant des informations sur les photos"""
        liste_arguments = [1, 2, 3, 4]  # On doit donner 5 arguments à Satellite pour la création d'une instance
        num_liste = 0  # ième argument de la liste
        argument = ""
        for j in range(len(caracteres)):
            if caracteres[j] != " ":
                argument += caracteres[j]
            else:  # Ici, l'argument est ajouté à liste_arguments
                liste_arguments[num_liste] = int(argument)  # On doit transformer chaque information en entier
                num_liste += 1
                argument = ""
        liste_arguments[num_liste] = int(argument)  # On ajoute le dernier

        return [liste_arguments[0], liste_arguments[1], liste_arguments[2], liste_arguments[3]]

    def creer_output(self, liste_zones, nb_photos_prises):
        """
        Méthode chargée de créer le fichier output et d'afficher le temps d'exécution
        :param liste_zones: liste de listes : zones du globe
        :param nb_photos_prises: entier
        """
        fichier_output = open(self.chemin_output, "w")  # le "w" fait qu'on réécrit sur le fichier précedent
        fichier_output.write(str(nb_photos_prises) + "\n")
        for liste in liste_zones:
            for zone in liste:
                for photo in zone.photos_prises:
                    fichier_output.write(str(photo.latitude) + " ")
                    fichier_output.write(str(photo.longitude) + " ")
                    fichier_output.write(str(photo.prise_tour) + " ")
                    fichier_output.write(str(photo.prise_par_id) + "\n")
        temps_exec = time.clock()
        if temps_exec <= 60:
            print("Le temps d'exécution fut de " + str(temps_exec) + " secondes")
        else:
            print("Le temps d'exécution fut de " + str(temps_exec / 60) + " minutes")

        self.temps_exec = time.clock()

    def recup_output(self):
        """
        Méthode chargée de : Récupérer les informations d'un fichier d'output et de les transformer en instances
        de classes.
        :return: une liste contenant toutes les photos prises triées par le tour
        """
        liste_photos = []

        print("Lecture du fichier d'output")
        fichier_output = open(self.chemin_output, 'r')

        # rstrip est utilisé pour ne pas prendre "\n" en compte.
        nb_photos_prises = int(fichier_output.readline().rstrip())

        for i in range(0, nb_photos_prises):
            chaine_photo = (fichier_output.readline().rstrip())
            photo = self.ligne_output_par_chaine(chaine_photo)  # Pas besoin de préciser la Collection
            liste_photos.append(photo)

        fichier_output.close()

        # Trie des photos en fonction du tour
        liste_photos.sort(key=lambda k: [k[2]])

        return liste_photos
