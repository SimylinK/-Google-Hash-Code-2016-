#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from Classes.Satellite import Satellite


class Graphique:
    """Classe chargée de :
    Afficher l'éxecution des satellites sur une interface graphique
    """

    def __init__(self, nb_tours, liste_satellites, globe, liste_photos_prises):
        self.fenetre = Tk()  # Tk() doit être fais avant "StringVar()"

        self.tour_max = nb_tours
        self.liste_satellites = liste_satellites
        self.globe = globe
        self.liste_photos_prises = liste_photos_prises

        self.canvas = None
        self.liste_dessins = []
        self.liste_dessins_photos = []
        self.tour = 0
        # compteur_tour va être associé à un label pour afficher les tours dynamiquement
        self.compteur_tour = StringVar()
        self.compteur_tour.set("0")
        self.index_liste_photos = 0

    def initialisation(self):
        """ Met en place l'affichage
        """

        # Placement de la map monde
        self.canvas = Canvas(self.fenetre, width=1500, height=752)
        photo = PhotoImage(file="docs/map_monde.png")
        # Taille de 1500 * 752 px
        # La map commence en x : 19 et y : 8
        # La map termine en x : 1474 et y : 738
        # Longitude 0 est en x : 701
        self.canvas.create_image(0, 0, anchor=NW, image=photo)

        self.dessiner_satellites()

        # Partie à gauche de la map
        panel_principal = PanedWindow(self.fenetre, orient=VERTICAL)
        panel_principal.pack(side=LEFT, expand=Y, fill=BOTH, pady=200, padx=2)

        # Affichage du tour
        panel_tour = PanedWindow(self.fenetre, orient=HORIZONTAL)
        panel_tour.add(Label(self.fenetre, text="Tour : "))
        panel_tour.add(Label(self.fenetre, textvariable=self.compteur_tour))
        panel_principal.add(panel_tour)

        # Affichage des boutons tour suivant et précédent
        panel_principal.add(Button(self.fenetre, text='Tour suivant', command=self.tours_suivants))
        panel_principal.add(Button(self.fenetre, text='Tour précédent', command=self.tours_precedents))


        # Pour éviter d'étirer l'élément juste au-dessus
        panel_principal.add(Label(self.fenetre, text=""))
        panel_principal.pack()

        self.canvas.pack()

        self.fenetre.mainloop()

    def tours_suivants(self, nb_tours=1):
        """ Fais avancer un tour pour les satellites, et remets en place les dessins
        """
        if (self.tour < self.tour_max) : # self.tour_max est le dernier tour
            if (self.tour + nb_tours > self.tour_max) : # self.tour_max ne doit pas être dépassé
                nb_tours = self.tour_max - nb_tours
                self.tour = self.tour_max

            for i in range (nb_tours):

                for satellite in self.liste_satellites:
                    satellite.tour_suivant()
                self.effacer_dessins()
                self.dessiner_satellites()
                self.tour += 1
                self.compteur_tour.set(str(self.tour))
                # Boucle pour afficher les photos prises à ce tour
                while ( self.index_liste_photos < len(self.liste_photos_prises)
                        and self.liste_photos_prises[self.index_liste_photos][2] == self.tour):
                    photo = self.liste_photos_prises[self.index_liste_photos]
                    self.dessiner_croix(photo[0], photo[1])

                    self.index_liste_photos += 1

    def tours_precedents(self, nb_tours=1):
        """ Fais revenir la carte a un tour précédent
        :param nb_tours: nombre de tours à reculer
        """
        if (self.tour > 0): # le tour 0 est le tour minimum
            if (self.tour > nb_tours):
                self.tour = self.tour - nb_tours # Cas normal
            else :
                nb_tours = self.tour # nb_tour fais revenir avant le tour 0
                self.tour = 0

            self.compteur_tour.set(str(self.tour))
            #On regarde combien de photo il faut enlever
            nb_photos_enlever = 0
            index = self.index_liste_photos - 1
            while(index >= 0 and self.liste_photos_prises[index][2] > self.tour):
                index -= 1
                nb_photos_enlever += 1
            self.index_liste_photos = index + 1

            # On efface les photos en trop
            for i in range(nb_photos_enlever):
                croix1 = self.liste_dessins_photos.pop()
                croix2 = self.liste_dessins_photos.pop()
                self.canvas.delete(croix1)
                self.canvas.delete(croix2)

            # Les satelittes reculent de nb_tours
            for i in range(nb_tours):
                for satellite in self.liste_satellites:
                    satellite.tour_precedent()
            self.effacer_dessins()
            self.dessiner_satellites()


    def dessiner_rond(self, latitude, longitude):
        """ Dessine un rond a une latitude et longitude
        :param latitude: un entier dans [-324000;324000]
        :param longitude: un entier dans [-648000;647999]
        """
        latitude_pixel = self.latitude_vers_pixel(latitude)
        longitude_pixel = self.longitude_vers_pixel(longitude)

        rond = self.canvas.create_oval(longitude_pixel, latitude_pixel, (longitude_pixel + 5), (latitude_pixel + 5),
                                       fill="red", width=2, outline="black")
        self.liste_dessins.append(rond)

    def dessiner_croix(self, latitude, longitude):
        """ Dessinne une croix a une latitude et une longitude
        :param latitude: un entier dans [-324000;324000]
        :param longitude: un entier dans [-648000;647999]
        """
        latitude_pixel = self.latitude_vers_pixel(latitude)
        longitude_pixel = self.longitude_vers_pixel(longitude)

        croix1 = self.canvas.create_line(longitude_pixel - 5, latitude_pixel - 5, longitude_pixel + 5, latitude_pixel + 5, width=5, fill="blue")
        croix2 = self.canvas.create_line(longitude_pixel - 5, latitude_pixel + 5, longitude_pixel + 5, latitude_pixel - 5, width=5, fill="blue")

        self.liste_dessins_photos.append(croix1)
        self.liste_dessins_photos.append(croix2)

    def latitude_vers_pixel(self, latitude):
        """ Transforme une latitude en sa position sur la map en pixel
        :param latitude: un entier dans [-324000;324000]
        :return: un entier dans [8;738]
        """
        latitude += 324000
        latitude_pixel = ((latitude * 730) // 648000)  # sur une échelle de 0 a 765
        return 730 - latitude_pixel + 8  # La latitude est inversée, et la map commence a 8

    def longitude_vers_pixel(self, longitude): # TODO : des satellites dépasssent à gauche
        """ Transforme une longitude en sa position sur la map en pixel
        :param longitude: un entier dans [-648000;64799]
        :return: un entier dans [19;1474]
        """
        longitude += 648000
        longitude_pixel = ((longitude * 1455) // 1296000)  # sur une échelle de 0 a 12196000

        if (longitude > 1337000):  # si on dépasse à droite
            longitude_pixel -= 1500  # on revient tout à gauche de la map
        else:
            longitude_pixel -= 45  # la longitude zéro est décalé de 45
        return longitude_pixel + 19  # la map commence a 19

    def effacer_dessins(self):
        """ Efface tous les dessins présents sur le canvas
        """
        for dessin in self.liste_dessins:
            self.canvas.delete(dessin)
        self.liste_dessins = []

    def dessiner_satellites(self):
        """ Dessine les satellites sur le canvas
        """
        for satellite in self.liste_satellites:
            self.dessiner_rond(satellite.latitude, satellite.longitude)

# TODO : afficher cadrillage globe (une checkbox ce serait cool)


if __name__ == "__main__":
    # Création des satellite
    # Paris : 175872   8455
    s1 = Satellite(0, 175872, 8455, 100, 10, 5000)
    liste_satellites = []
    liste_satellites.append(s1)

    # Création d'un Globe
    globe = None

    # Création des photos
    liste_photos = []

    # Création d'un Graphique
    tour = 10
    g = Graphique(tour, liste_satellites, globe, liste_photos)

    # Tests
    g.initialisation()
