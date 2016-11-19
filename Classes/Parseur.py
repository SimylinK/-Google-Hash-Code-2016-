#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Imports servant à :
    - à réutiliser les classes définies dans les autres fichiers :
        import Photo : classe Photo
        import Satellite : classe Satellite.
"""

from Photo import Photo
from Satellite import Satellite


class Parseur:
    """Classe chargée de :
    transformer le fichier d'input en informations utilisables :
        variables, instances de classes..

    Demande à l'utilisateur les chemins des fichiers input et output.
    Lorsque la simulation totale est terminée :
        renvoie le chemin du fichier output.
    """

    def __init__(
            self, chemin_input=None, chemin_output=None):
        """Le fichier d'input original est converti en fichier pickle"""
        self.chemin_input = self.demander_input()
        self.chemin_output = self.demander_output()

    def demander_input(self):
        chemin = ' '
        while chemin[0] != '/' and chemin[0] != 'C':  # Vérification que le chemin est bien absolu.
            chemin = input("Chemin absolu du fichier input : ")
        return chemin

    def demander_output(self):
        chemin = ' '
        while chemin[0] != '/' and chemin[0] != 'C':  # Vérification que le chemin est bien absolu.
            chemin = input("Chemin absolu du fichier output : ")
        return chemin

    def recup(self):
        """Méthode chargée de :
        Récupérer le nombre de tours et le nombre de satellites
        Lancer la création des instances de la classe Satellite
        """

        fichier_input = open(self.chemin_input, 'r')
        nb_tours = fichier_input.readline().rstrip()  # rstrip est utilisé pour ne pas prendre "\n" en compte.
        nb_satellites = fichier_input.readline().rstrip()
        fichier_input.close()

        instances_sat = self.creation_satellites(int(nombre_satellites))
        return nb_tours, nb_satellites, instances_sat

    def creation_satellites(self, nombre):
        """
           Méthode chargée de créer les instances de satellites.
           nombre est un entier correspondant au nombre de satellites.
           La fonction retourne une liste contenant les instances de Satellite.
        """

        fichier_input = open(self.chemin_input, 'r')
        liste_satellites = []
        for i in range(0, 2 + nombre):
            if i == 0 or i == 1:  # On passe les deux premières lignes avant la création.
                fichier_input.readline()
            else:
                chaine = fichier_input.readline().rstrip()
                satellite = self.satellite_par_chaine(chaine)
                liste_satellites.append(satellite)

        return liste_satellites

    def satellite_par_chaine(self, caracteres):
        """"Transforme une ligne du fichier input en une instance de la classe Satellite"""
        liste_arguments = [1, 2, 3, 4, 5]  # On doit donner 5 arguments à Satellite pour la création d'une instance
        num_liste = 0  # ième argument de la liste
        argument = ""
        for j in range(len(caracteres)):
            if caracteres[j] != " ":
                argument += caracteres[j]
            else:  # Ici, l'argument est ajouté à liste_arguments
                liste_arguments[num_liste] = argument
                num_liste += 1
                argument = ""
        liste_arguments[num_liste] = argument  # Comme la ligne ne se termine pas par un espace, on rajoute le dernier

        return Satellite(liste_arguments[0], liste_arguments[1], liste_arguments[2], liste_arguments[3],
                         liste_arguments[4])


parseur = Parseur()
nombre_tours, nombre_satellites, liste = parseur.recup()
