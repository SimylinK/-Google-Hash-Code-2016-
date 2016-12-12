#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import time

class Interface:
    def __init__(self, adresse_photo = None):
        self.fichier_input = ""
        self.voir_simulation = False
        self.adresse_photo = ""

    def creer_interface_lancement(self):
        fen1 = Tk(className='#HashCode | Choix de la simulation')
        fen1.configure(bg='white')
        canvas = Canvas(fen1, width=600, height=300)
        photo = PhotoImage(file="docs/Logo_polyhash_code_signe.png")
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
        fen1.destroy()

        if retour.get() == 1:
            self.fichier_input = "weekend"
        elif retour.get() == 2:
            self.fichier_input = "overlap"
        elif retour.get() == 3:
            self.fichier_input = "forever_alone"
        else:
            self.fichier_input = "constellation"

    def creer_interface_fin(self, temps_exec):
        fen2 = Tk(className='#HashCode | Résultat de la simulation')
        fen2.configure(bg='white')

        temps_en_secondes = Label(fen2, text="La simulation de " + self.fichier_input + " a duré " + str(round(temps_exec, 2)) + " secondes.",
                                  bg='white')
        temps_en_minutes = Label(fen2, text="La simulation a duré " + str(temps_exec // 60) + " minutes et " + str(
            round(temps_exec % 60, 2)) + " secondes.", bg='white')
        suite = Label(fen2, text="En quittant cette fenêtre : ", bg='white')
        quitter = Button(fen2, text="Quitter", command=fen2.quit)

        voir = IntVar()  # creation de variable-retour
        voir.set(1)
        voir_simulation = Checkbutton(fen2, variable=voir,
                                      text="Je veux voir le résultat de la simulation graphique", bg='white')

        if temps_exec <= 60:
            temps_en_secondes.pack(padx=10, pady=10)
        else:
            temps_en_minutes.pack(padx=10, pady=10)

        suite.pack(padx=10, pady=5)
        voir_simulation.pack(padx=10, pady=5)
        quitter.pack(padx=10, pady=5)

        fen2.mainloop()
        fen2.destroy()

        if voir.get() == 1:
            self.voir_simulation = True

        print(voir.get())

        return voir.get()

# Tests des fonctions
if __name__ == "__main__":
    interface1 = Interface("docs/Logo_polyhash_code_signe.png")
    temps_exec = 80
    interface1.creer_interface_lancement()
    print(interface1.fichier_input)
    interface2 = Interface()
    print(interface2.creer_interface_fin(80))
    print(interface2.voir_simulation)
