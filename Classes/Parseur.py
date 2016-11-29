#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Imports servant à :
    - à réutiliser les classes définies dans les autres fichiers :
        import Photo : classe Photo
        import Collection : classe Collection
        import Satellite : classe Satellite.
"""

from Photo import Photo
from Collection import Collection
from Satellite import Satellite


class Parseur:
    """Classe chargée de :
    transformer le fichier d'input en informations utilisables :
        variables, instances de classes..

    Demande à l'utilisateur les chemins des fichiers input et output.
    Lorsque la simulation totale est terminée :
        renvoie le chemin du fichier output.
    """

    def __init__(self):
        self.chemin_input = self.demander_input()
        self.chemin_output = self.demander_output()

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

    def recup(self):
        """Méthode chargée de : Récupérer les informations du fichier d'input.
        """

        fichier_input = open(self.chemin_input, 'r')
        nb_tours = int(fichier_input.readline().rstrip())  # rstrip est utilisé pour ne pas prendre "\n" en compte.
        nb_satellites = int(fichier_input.readline().rstrip())

        liste_satellites = []  # On transforme chaque ligne en une instance de la classe Satellite
        for i in range(0, nb_satellites):
            chaine = fichier_input.readline().rstrip()
            satellite = self.satellite_par_chaine(chaine, nb_tours)
            liste_satellites.append(satellite)

        # On transforme les lignes suivantes en instances des classes Photo et Collection

        nb_collections = int(fichier_input.readline().rstrip())
        liste_collections = []  # Liste qui contiendra les collections
        for i in range(nb_collections):  # On fait l'opération sur toutes les collections
            chaine_collection = fichier_input.readline().rstrip()
            collection = self.collection_par_chaine(chaine_collection)
            for j in range(collection.nb_photos):  # À chaque collection, on ajoute ses photos
                chaine_photo = (fichier_input.readline().rstrip())
                photo = self.photo_par_chaine(chaine_photo)
                collection.ajouter_photo(photo)
            for k in range(collection.nb_intervalles):  # À chaque collection, on ajoute ses intervalles
                chaine_intervalle = (fichier_input.readline().rstrip())
                intervalle = self.intervalle_par_chaine(chaine_intervalle)
                collection.ajouter_intervalle(intervalle)
            liste_collections.append(collection)
        fichier_input.close()

        return nb_tours, nb_satellites, liste_satellites, liste_collections

    def photo_par_chaine(self, caracteres):
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

        return Photo(liste_arguments[0], liste_arguments[1])

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

    def satellite_par_chaine(self, caracteres, nb_tours):
        """"Transforme une ligne du fichier input en une instance de la classe Satellite"""
        liste_arguments = [1, 2, 3, 4, 5,
                           nb_tours]  # On doit donner 5 arguments à Satellite pour la création d'une instance
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

        return Satellite(liste_arguments[0], liste_arguments[1], liste_arguments[2], liste_arguments[3],
                         liste_arguments[4], liste_arguments[5])


parseur = Parseur()
nombre_tours, nombre_satellites, liste_satellites, liste_collections = parseur.recup()
