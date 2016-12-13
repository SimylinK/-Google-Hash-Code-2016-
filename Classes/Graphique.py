#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from Classes.Satellite import Satellite

class Graphique:
    """
    Classe chargée de :
    Afficher l'éxecution des satellites sur une interface graphique
    """

    def __init__(self, nb_tours, liste_satellites, globe, liste_photos_prises, taille_zone):
        """
        :param nb_tours: le nombre de tours que la simulation va durer
        :param liste_satellites: liste des instances de classe Satellite
        :param globe: une instance de la classe Globe
        :param liste_photos_prises: liste de listes qui contient des informations sur les photos ayant été prises
        :param taille_zone: taille d'un côté d'une zone du globe
        """
        # Tk() doit être fait avant "StringVar()"
        self.fenetre = Tk(className='#HashCode | Visualisation de la simulation')

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
        self.taille_zone = taille_zone
        self.reste_tours = True  # Signifie qu'il reste des tours et permet de lancer "Finir simulation"


    def initialisation(self):
        """
        Méthode chargée de :
        Mettre en place l'affichage
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

        # Trait
        panel_principal.add(Canvas(self.fenetre, width=10, height=3, background='blue'))

        # Affichage "avancer de"
        panel_principal.add(Label(self.fenetre, text="Avancer de : "))
        valeur_avancer = IntVar()
        panel_principal.add(Spinbox(self.fenetre, textvariable=valeur_avancer, from_=0, to=self.tour_max - self.tour))
        panel_principal.add(Button(self.fenetre, text='Avancer',
                                   command=lambda: self.tours_suivants(valeur_avancer.get())))

        # Trait
        panel_principal.add(Canvas(self.fenetre, width=10, height=3, background='blue'))

        # Affichage "reculer de"
        panel_principal.add(Label(self.fenetre, text="Reculer de : "))
        valeur_reculer = IntVar()
        panel_principal.add(Spinbox(self.fenetre, textvariable=valeur_reculer, from_=0, to=self.tour_max - self.tour))
        panel_principal.add(Button(self.fenetre, text='Reculer',
                                   command=lambda: self.tours_precedents(valeur_reculer.get())))

        # Trait
        panel_principal.add(Canvas(self.fenetre, width=10, height=3, background='blue'))

        # Affichage de "Aller au tour : "
        panel_principal.add(Label(self.fenetre, text="Aller au tour : "))
        valeur_aller = IntVar()
        panel_principal.add(Spinbox(self.fenetre, textvariable=valeur_aller, from_=0, to=self.tour_max))
        panel_principal.add(Button(self.fenetre, text='Exécuter', command=lambda: self.aller_tour(valeur_aller)))

        # Affichage de "Finir la simulation"
        panel_principal.add(Button(self.fenetre, text='Finir la simulation', command=lambda: self.avancer()))

        # Pour éviter d'étirer l'élément juste au-dessus
        panel_principal.add(Label(self.fenetre, text=""))
        panel_principal.pack()

        self.canvas.pack()

        self.dessiner_photos()

        self.fenetre.mainloop()

    def tours_suivants(self, nb_tours=1):
        """
        Méthode chargée de :
        Faire avancer un tour pour les satellites, et remettre en place les dessins
        """
        if self.tour < self.tour_max:  # self.tour_max est le dernier tour
            if self.tour + nb_tours > self.tour_max:  # self.tour_max ne doit pas être dépassé
                nb_tours = self.tour_max - self.tour

            for i in range(nb_tours):

                for satellite in self.liste_satellites:
                    satellite.tour_suivant()
                self.effacer_dessins()
                self.dessiner_satellites()
                self.tour += 1
                # Boucle pour afficher les photos prises à ce tour
                while (self.index_liste_photos < len(self.liste_photos_prises)
                       and self.liste_photos_prises[self.index_liste_photos][2] == self.tour):
                    photo = self.liste_photos_prises[self.index_liste_photos]
                    self.dessiner_croix(photo[0], photo[1], "blue")
                    self.index_liste_photos += 1
                self.compteur_tour.set(str(self.tour))
        else:
            self.reste_tours = False
    def tours_precedents(self, nb_tours=1):
        """
        Méthode chargée de :
        Faire revenir la carte à un tour précédent
        :param nb_tours: nombre de tours à reculer
        """
        if self.tour > 0:  # le tour 0 est le tour minimum
            if self.tour > nb_tours:
                self.tour -= nb_tours  # Cas normal
            else:
                nb_tours = self.tour  # nb_tour fait revenir avant le tour 0
                self.tour = 0

            self.compteur_tour.set(str(self.tour))
            # On regarde combien de photo il faut enlever
            nb_photos_enlever = 0
            index = self.index_liste_photos - 1
            while index >= 0 and self.liste_photos_prises[index][2] > self.tour:
                index -= 1
                nb_photos_enlever += 1
            self.index_liste_photos = index + 1

            # On efface les photos en trop
            for i in range(nb_photos_enlever):
                croix1 = self.liste_dessins_photos.pop()
                croix2 = self.liste_dessins_photos.pop()
                self.canvas.delete(croix1)
                self.canvas.delete(croix2)

            # Les satelites reculent de nb_tours
            for i in range(nb_tours):
                for satellite in self.liste_satellites:
                    satellite.tour_precedent()
            self.effacer_dessins()
            self.dessiner_satellites()

    def aller_tour(self, tour):
        """
        Méthode chargée de :
        Permettre de faire avancer ou reculer jusqu'à un tour
        :param tour: un entier dans [0, self.tour_max]
        """
        nb_tours = abs(tour.get() - self.tour)
        if tour.get() > self.tour:
            self.tours_suivants(nb_tours)
        else:
            self.tours_precedents(nb_tours)

    def dessiner_rond(self, latitude, longitude):
        """
        Méthode chargée de :
        Dessine un rond a une latitude et longitude
        :param latitude: un entier dans [-324000;324000]
        :param longitude: un entier dans [-648000;647999]
        """
        latitude_pixel = self.latitude_vers_pixel(latitude)
        longitude_pixel = self.longitude_vers_pixel(longitude)

        rond = self.canvas.create_oval(longitude_pixel, latitude_pixel, (longitude_pixel + 10), (latitude_pixel + 10),
                                       fill="red", width=2, outline="black")
        self.liste_dessins.append(rond)

    def dessiner_croix(self, latitude, longitude, couleur):
        """
        Méthode chargée de :
        Dessine une croix a une latitude et une longitude
        :param latitude: un entier dans [-324000;324000]
        :param longitude: un entier dans [-648000;647999]
        :param couleur: une couleur normée : "blue","red"...
        """
        latitude_pixel = self.latitude_vers_pixel(latitude)
        longitude_pixel = self.longitude_vers_pixel(longitude)

        croix1 = self.canvas.create_line(longitude_pixel - 5, latitude_pixel - 5, longitude_pixel + 5,
                                         latitude_pixel + 5, width=5, fill=couleur)
        croix2 = self.canvas.create_line(longitude_pixel - 5, latitude_pixel + 5, longitude_pixel + 5,
                                         latitude_pixel - 5, width=5, fill=couleur)

        self.liste_dessins_photos.append(croix1)
        self.liste_dessins_photos.append(croix2)

    def latitude_vers_pixel(self, latitude):
        """
        Méthode chargée de :
        Transformer une latitude en sa position sur la map en pixel
        :param latitude: un entier dans [-324000;324000]
        :return: un entier dans [8;738]
        """
        latitude += 324000
        latitude_pixel = ((latitude * 730) // 648000)  # sur une échelle de 0 a 765
        return 730 - latitude_pixel + 8  # La latitude est inversée, et la map commence a 8

    def longitude_vers_pixel(self, longitude):
        """
        Méthode chargée de :
        Transformer une longitude en sa position sur la map en pixel
        :param longitude: un entier dans [-648000;64799]
        :return: un entier dans [19;1474]
        """
        longitude += 648000
        longitude_pixel = ((longitude * 1455) // 1296000)  # sur une échelle de 0 a 12196000

        if longitude < 40500:  # si on dépasse à gauche
            longitude_pixel += 1410  # on revient tout à droite de la map
        else:
            longitude_pixel -= 45  # la longitude zéro est décalé de 45
        return longitude_pixel + 19  # la map commence a 19

    def effacer_dessins(self):
        """
        Méthode chargée de :
        Effacer tous les dessins présents sur le canvas
        """
        for dessin in self.liste_dessins:
            self.canvas.delete(dessin)
        self.liste_dessins = []

    def dessiner_satellites(self):
        """
        Méthode chargée de :
        Dessine les satellites sur le canvas
        """
        for satellite in self.liste_satellites:
            self.dessiner_rond(satellite.latitude, satellite.longitude)

    def dessiner_cadrillage(self):
        """
        Méthode chargée de :
        Dessine le cadrillage, mais ne pas utiliser car c'est moche
        """
        pas_lat = self.latitude_vers_pixel(324000 - self.taille_zone)
        pas_long = 2 * pas_lat
        for i in range(8, 738, pas_lat):
            # On dessine une ligne de latitude
            x0 = 19
            y0 = i
            x1 = 1474
            y1 = i + pas_lat
            self.canvas.create_line(x0, y0, x1, y1)

        for j in range(19, 1474, pas_long):
            x0 = j
            y0 = 8
            x1 = j + pas_long
            y1 = 738
            self.canvas.create_line(x0, y0, x1, y1)

    def dessiner_photos(self):
        for photo in self.liste_photos_prises:
            self.dessiner_croix(photo[0], photo[1], "gray")

    def avancer(self):
        """
        Méthode chargée de :
        Méthode qui permet de faire avancer jusqu'à la fin de la simulation
        """
        if self.reste_tours:
            self.tours_suivants(100)
            self.fenetre.after(10, self.avancer)

    def stopper(self):
        """
        Méthode chargée de :
        Arrête la simulation
        """
        self.reste_tours = False


# Tests divers
if __name__ == "__main__":
    # Création des satellite
    # Paris : 175872   8455
    s1 = Satellite(0, 0, -640000, 100, 10, 5000)
    liste_satellites = [s1]

    # Création d'un Globe
    globe = None

    # Création des photos
    liste_photos = []

    # Création d'un Graphique
    tour = 10
    taille_zone = 5000
    g = Graphique(tour, liste_satellites, globe, liste_photos, taille_zone)

    # Tests
    g.initialisation()
