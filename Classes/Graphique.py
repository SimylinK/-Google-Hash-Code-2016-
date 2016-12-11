from tkinter import *

from Classes.Satellite import Satellite

class Graphique:
    """Classe chargée de :
    Afficher l'éxecution des satellites sur une interface graphique
    """

    def __init__(self, nb_tours, nb_satellites, liste_satellites, globe):
        self.nb_tours = nb_tours
        self.nb_satellites = nb_satellites
        self.liste_satellites = liste_satellites
        self.globe = globe
        self.canvas = None
        self.liste_dessins = []
        self.tour = 0
        self.compteur_tour = None

    def initialisation(self):
        """ Met en place l'affichage
        """
        fenetre = Tk()

        # Placement de la map monde
        self.canvas = Canvas(fenetre, width=1500, height=752)
        photo = PhotoImage(file="../docs/map_monde3.png")
        # Taille de 1500 * 752 px
        # La map commence en x : 19 et y : 8
        # La map termine en x : 1474 et y : 738
        # Longitude 0 est en x : 701
        self.canvas.create_image(0, 0, anchor=NW, image=photo)

        self.dessiner_satellites()

        Label(fenetre, text="Tour : ").pack(side=LEFT, padx=5, pady=5)
        self.compteur_tour = Label(fenetre, text="0").pack(side=LEFT, padx=5, pady=5)
        Button(fenetre, text='Tour suivant', command=self.tour_suivant).pack(side=LEFT, padx=5, pady=5)

        self.canvas.pack()

        fenetre.mainloop()

    def tour_suivant(self):
        for satellite in self.liste_satellites :
            satellite.tour_suivant()
        self.effacer_dessins()
        self.dessiner_satellites()

    def dessin_rond(self, latitude, longitude):
        """ Dessine un rond a une latitude et longitude
        :param latitude: un entier dans [-324000;324000]
        :param longitude: un entier dans [-648000;647999]
        """
        latitude_pixel = self.latitude_vers_pixel(latitude)
        longitude_pixel = self.longitude_vers_pixel(longitude)

        rond = self.canvas.create_oval(longitude_pixel, latitude_pixel, (longitude_pixel + 5), (latitude_pixel + 5), fill="red", width=2,
                                  outline="black")
        self.liste_dessins.append(rond)

    def latitude_vers_pixel(self, latitude):
        """ Transforme une latitude en sa position sur la map en pixel
        :param latitude: un entier dans [-324000;324000]
        :return: un entier dans [0;800]
        """
        latitude += 324000
        latitude_pixel = ((latitude * 730) // 648000) # sur une échelle de 0 a 765
        return 730 - latitude_pixel + 8# La latitude est inversée, et la map commence a 8

    def longitude_vers_pixel(self, longitude):
        """ Transforme une longitude en sa position sur la map en pixel
        :param longitude:
        :return:
        """
        longitude += 648000
        longitude_pixel = ((longitude * 1455) // 1296000)  # sur une échelle de 0 a 12196000

        if (longitude > 1337000): # si on dépasse à droite
            longitude_pixel -= 1500 # on revient tout à gauche de la map
        else :
            longitude_pixel -= 45  # la longitude zéro est décalé de 45
        return longitude_pixel + 19 # la map commence a 19

    def effacer_dessins(self):
        """ Efface tous les dessins présents sur le canvas
        """
        for dessin in self.liste_dessins :
            self.canvas.delete(dessin)
        self.liste_dessins = []

    def dessiner_satellites(self):
        """ Dessine les satellites sur le canvas
        """
        for satellite in self.liste_satellites :
            self.dessin_rond(satellite.latitude, satellite.longitude)

if __name__ == "__main__":
    # Création des satellite
    # Paris : 175872   8455
    s1 = Satellite(0, 175872, 8455, 100, 10, 5000)
    liste_satellites = []
    liste_satellites.append(s1)
    nb_satellites = len(liste_satellites)

    # Création d'un Globe
    globe = None

    # Création d'un Graphique
    tour = 10
    g = Graphique(tour, nb_satellites, liste_satellites, globe)

    # Tests
    g.initialisation()



    print("Hello World")