#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
from docs import *

class Interface:
    def __init__(self, adresse_photo):
        self.fichier_input = ""
        self.voir_simulation = False
        self.parseur = ""
        self.adresse_photo = ""

    def creer_interface_lancement(self):
        fen1 = Tk()
        fen1.configure(bg='white')
        canvas = Canvas(fen1, width=600, height=300)
        photo = PhotoImage(file=self.adresse_photo)
        canvas.create_image(50, 50, anchor=NW, image=photo)
        canvas.pack(side=TOP and RIGHT)
        canvas.configure(bg='white')

        label = Label(fen1, text="Quel fichier utiliser pour la simulation ?", bg='white')

        retour = IntVar()  # cree une variable entiere pour recevoir la valeur retour
        retour.set(3)  # le bouton forever_alone est le choix par defaut (value=2)

        weekend = Radiobutton(fen1, text="weekend", variable=retour, value=1, bd=2, bg='white')
        overlap = Radiobutton(fen1, text="overlap", variable=retour, value=2, bd=3, bg='white')
        forever_alone = Radiobutton(fen1, text="forever_alone", variable=retour, value=3, bd=3, bg='white')
        constellation = Radiobutton(fen1, text="constellation", variable=retour, value=4, bd=3, bg='white')


        quitter = Button(fen1, text="Lancer le programme", command=fen1.quit, width=25, height=1)

        label.pack(padx=10, pady=5)
        weekend.pack()
        overlap.pack()
        forever_alone.pack()
        constellation.pack()
        quitter.pack(padx=10, pady=10, side=RIGHT and BOTTOM)

        fen1.mainloop()

        if retour.get() == 1:
            self.fichier_input = "weekend"
        elif retour.get() == 2:
            self.fichier_input = "overlap"
        elif retour.get() == 3:
            self.fichier_input = "forever_alone"
        else:
            self.fichier_input = "constellation"

    def creer_interface_fin(self, temps_exec):
        fen2 = Tk()
        fen2.configure(bg='white')

        temps_en_secondes = Label(fen2, text="La simulation a duré " + str(round(temps_exec, 2)) + " secondes.",
                                  bg='white')
        temps_en_minutes = Label(fen2, text="La simulation a duré " + str(temps_exec // 60) + " minutes et " + str(
            round(temps_exec % 60, 2)) + " secondes.", bg='white')
        suite = Label(fen2, text="En quittant cette fenêtre : ", bg='white')
        quitter = Button(fen2, text="Quitter", command=fen2.quit)

        retour = IntVar()  # creation de variable-retour
        voir_simulation = Checkbutton(fen2, variable=retour,
                                      text="Je veux voir le résultat de la simulation graphique", bg='white')

        if temps_exec <= 60:
            temps_en_secondes.pack(padx=10, pady=10)
        else:
            temps_en_minutes.pack(padx=10, pady=10)

        suite.pack(padx=10, pady=5)
        voir_simulation.pack(padx=10, pady=5)
        quitter.pack(padx=10, pady=5)

        fen2.mainloop()

        return retour.get()

        # # recuperation de la valeur lors de la sortie de la boucle mainloop():
        # if retour.get() == 1:  # la variable 'retour' = 1 si la case est cochee, 0 sinon
        #     liste_photos = parseur.recup_output()
        #     graphique = Graphique(nombre_tours, liste_satellites, None, liste_photos)
        #     graphique.initialisation()
        # else:
        #     print("blop")

    def assigne_x_a_fichier_input(self, x):
        self.fichier_input = str(x)

    def voir_simulation(self, x):
        self.voir_simulation = x

# Tests des fonctions
if __name__ == "__main__":
    interface = Interface("docs/Logo_polyhash_code_signe.png")
    temps_exec = 80
    interface.creer_interface_lancement()
    print(interface.fichier_input)
    print(interface.creer_interface_fin(80))

