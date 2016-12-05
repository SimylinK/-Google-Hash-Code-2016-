#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Imports servant à :
    - à réutiliser les classes définies dans les autres fichiers :
        import Photo : classe Photo
        import Collection : classe Collection
        import Satellite : classe Satellite
        import ZoneGlobe : classe ZoneGlobe.
"""

from Photo import Photo
from Collection import Collection
from Satellite import Satellite
from ZoneGlobe import ZoneGlobe
import math


class Parseur:
    """Classe chargée de :
    transformer le fichier d'input en informations utilisables :
        variables, instances de classes..

    Demande à l'utilisateur les chemins des fichiers input et output.
    Lorsque la simulation totale est terminée :
        renvoie le chemin du fichier output.
    """

    # Constantes :
    LAT_ZONE = 0  # Paramètres à changer pour modifier la taille des zones, calculé ensuite
    LONG_ZONE = 0
    TAILLE_LAT = 648000  # Taille de la Terre en arcsecondes
    TAILLE_LONG = 1295999
    NB_ZONES_LAT = 0  # Calculé ensuite
    NB_ZONES_LONG = 0

    def __init__(self):
        self.chemin_input = self.demander_input()
        self.chemin_output = self.demander_output() + '.out'
        self.liste_zones = []

    def demander_input(self):
        chemin = ' '
        while chemin == ' ':  # Vérification que le chemin n'est pas laissé vide
            chemin = input("Chemin absolu du fichier input : ")
        return chemin

    def demander_output(self):
        chemin = ' '
        while chemin == ' ':  # Vérification que le chemin n'est pas laissé vide
            chemin = input("Chemin absolu du fichier output : ")
        return chemin

    def creation_zones(self):
        """Méthode chargée de créer les différentes zones du globe"""
        # IDEE : (lat objet-1)/(lat zone) + self.NB_ZONES_LAT//2 = indice i de objet dans la liste
        # On ajoute -1 pour le problème à la borne supérieure
        print("Création des zones")
        reste_lat = self.TAILLE_LAT % self.LAT_ZONE
        reste_long = self.TAILLE_LONG % self.LONG_ZONE

        liste_zones = []  # Liste de listes de zones. Tous les éléments d'une sous-liste possèdent la même latitude

        for i in range(-324000, 324000 - reste_lat, self.LAT_ZONE):
            liste_longitude = []
            for j in range(-648000, 647999 - reste_long, self.LONG_ZONE):
                liste_longitude.append(ZoneGlobe(i, i + self.LAT_ZONE, j, j + self.LONG_ZONE))
            liste_zones.append(liste_longitude)

        # S'il reste des zones de tailles inférieures, on les ajoute ici
        if reste_lat != 0:
            # On boucle sur la longitude, on ajoute donc une nouvelle sous-liste:
            liste_ajoutee = []
            for i in range(-648000, 647999, self.LONG_ZONE):
                if i + self.LONG_ZONE > 647999:
                    liste_ajoutee.append(ZoneGlobe(324000 - reste_lat, 324000, i, 647999))
                else:
                    liste_ajoutee.append(ZoneGlobe(324000 - reste_lat, 324000, i, i + self.LONG_ZONE))
            liste_zones.append(liste_ajoutee)

        if reste_long != 0:
            # On ajoute à la fin de chaque sous-liste la dernière zone
            indice = 0
            for i in range(-324000, 324000, self.LAT_ZONE):
                #  Pour éviter d'ajouter deux fois la case de latitude et longitude maximales:
                if indice < self.NB_ZONES_LAT:
                    if i + self.LAT_ZONE > 324000:
                        liste_zones[indice].append(ZoneGlobe(i, 324000, 647999 - reste_long, 647999))
                    else:
                        liste_zones[indice].append(ZoneGlobe(i, i + self.LAT_ZONE, 647999 - reste_long, 647999))
                    indice += 1

        return liste_zones

    def recup(self):
        """Méthode chargée de : Récupérer les informations du fichier d'input et de les transformer en instances
        de classes.
        """
        print("Lecture du fichier d'input")
        fichier_input = open(self.chemin_input, 'r')
        nb_tours = int(fichier_input.readline().rstrip())  # rstrip est utilisé pour ne pas prendre "\n" en compte.
        nb_satellites = int(fichier_input.readline().rstrip())

        liste_satellites = []  # On transforme chaque ligne en une instance de la classe Satellite
        id = 0
        max = 0 # Sert à calculer le max_déplacement_satellite sur tous les satellites
        for i in range(0, nb_satellites):
            chaine = fichier_input.readline().rstrip()
            satellite = self.satellite_par_chaine(id, chaine)
            liste_satellites.append(satellite)
            id += 1
            if satellite.max_deplacement_camera > max:
                max = satellite.max_deplacement_camera

        #  On met à jour les constantes
        self.LAT_ZONE = max  # Ainsi, le satellite ne peut pas prendre de caméra dans plus de 9 zones en même temps
        self.LONG_ZONE = max
        self.NB_ZONES_LAT = math.ceil(self.TAILLE_LAT / self.LAT_ZONE)  # On ne compte pas la dernière zone plus petite
        self.NB_ZONES_LONG = math.ceil(self.TAILLE_LONG / self.LONG_ZONE)

        # On lance ensuite la création des zones
        self.liste_zones = self.creation_zones()



        # On transforme les lignes suivantes en instances des classes Photo et Collection

        nb_collections = int(fichier_input.readline().rstrip())
        liste_collections = []  # Liste qui contiendra les collections
        for i in range(nb_collections):  # On fait l'opération sur toutes les collections
            chaine_collection = fichier_input.readline().rstrip()
            collection = self.collection_par_chaine(chaine_collection)
            for j in range(collection.nb_photos):  # À chaque collection, on ajoute ses photos
                chaine_photo = (fichier_input.readline().rstrip())
                photo = self.photo_par_chaine(chaine_photo, collection)
                lat = math.floor(((photo.latitude - 1) / self.LAT_ZONE)) + self.NB_ZONES_LAT // 2
                long = math.floor(((photo.longitude - 1) / self.LONG_ZONE)) + self.NB_ZONES_LONG // 2
                self.liste_zones[lat][long].ajouter_photo(photo)
                collection.ajouter_photo(photo)
            for k in range(collection.nb_intervalles):  # À chaque collection, on ajoute ses intervalles
                chaine_intervalle = (fichier_input.readline().rstrip())
                intervalle = self.intervalle_par_chaine(chaine_intervalle)
                collection.ajouter_intervalle(intervalle)
            liste_collections.append(collection)
        fichier_input.close()

        return nb_tours, nb_satellites, liste_satellites, liste_collections

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
        """Transforme une ligne du fichier input en une instance de la classe Collection"""
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
        """Transforme une ligne du fichier input en un intervalle"""
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
        """"Transforme une ligne du fichier input en une instance de la classe Satellite"""
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

    def creer_output(self, liste_zones, nb_photos_prises):
        fichier_output = open(self.chemin_output, "w")  # le "w" fait qu'on réécrit sur le fichier précedent
        fichier_output.write(str(nb_photos_prises) + "\n")
        for liste in range(len(liste_zones)):
            for zone in range(len(liste_zones[liste])):
                for photo in range(len(liste_zones[liste][zone].photos_prises)):
                    fichier_output.write(str(liste_zones[liste][zone].photos_prises[photo].latitude) + " ")
                    fichier_output.write(str(liste_zones[liste][zone].photos_prises[photo].longitude) + " ")
                    fichier_output.write(str(liste_zones[liste][zone].photos_prises[photo].prise_tour) + " ")
                    fichier_output.write(str(liste_zones[liste][zone].photos_prises[photo].prise_par_id) + "\n")
