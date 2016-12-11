#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module d'entrée pour la mise en oeuvre du projet Poly#.
"""
from tkinter import *
from Classes.Parseur import Parseur
from Classes.Distributeur import Distributeur
from Classes.Graphique import Graphique
import time

if __name__ == '__main__':

    #Fenetre pour l'interface graphique avec l'utilisateur avant le début du programme
    fen = Tk()
    fen.configure(bg = 'white')

    def assigne_x_a_fichier_input(x):
        global fichier_input
        fichier_input = str(x)

    assigne = lambda x: assigne_x_a_fichier_input(x)

    canvas = Canvas(fen, width=600, height=300)
    photo = PhotoImage(file="docs/Logo_polyhash_code_signe.png")
    canvas.create_image(50, 50, anchor=NW, image=photo)
    canvas.pack(side = TOP and RIGHT)
    canvas.configure(bg = 'white')

    label = Label(fen, text= "Quel fichier utiliser pour la simulation ?", bg='white')
    weekend = Button(fen, text = "weekend", command = lambda x = "weekend": assigne(x), width=10, height=1)
    overlap = Button(fen, text = "overlap", command = lambda x ="overlap": assigne(x), width=10, height=1)
    forever_alone = Button(fen, text = "forever_alone", command = lambda x ="forever_alone": assigne(x), width=10, height=1)
    constellation = Button(fen, text = "constellation", command = lambda x ="constellation": assigne(x), width=10, height=1)
    quitter = Button(fen, text = "Lancer le programme", command = fen.quit, width=25, height=1)

    label.pack(padx = 10, pady = 5)
    weekend.pack(padx=10, pady=5)
    overlap.pack(padx=10, pady=5)
    forever_alone.pack(padx=10, pady=5)
    constellation.pack(padx=10, pady=5)
    quitter.pack(padx=10, pady=10, side = RIGHT and BOTTOM)

    fen.mainloop()

    #Execution du programme

    time.clock()
    parseur = Parseur('/donneesTest/' + fichier_input + '.in')
    nombre_tours, nombre_satellites, liste_satellites, liste_collections, globe = parseur.initialisation()
    distrib = Distributeur(nombre_tours, nombre_satellites, liste_satellites, liste_collections, globe)
    nb_photos_prises = distrib.algo_opti()
    parseur.creer_output(globe.liste_zones, nb_photos_prises)
    temps_exec = time.clock()
    if temps_exec <= 60:
        print("Le temps d'exécution fut de " + str(temps_exec) + " secondes")
    else:
        print("Le temps d'exécution fut de " + str(temps_exec/60) + " minutes")

    #Fenetre pour l'interface graphique avec l'utilisateur après le programme
    voir_simulation = False

    def voir_simulation(x):
        global voir_simulation
        voir_simluation = x

    vrai_ou_faux = lambda x: voir_simulation(x)

    fen2 = Tk()
    fen2.configure(bg='white')

    temps_en_secondes = Label(fen2, text = "La simulation a duré " + str(round(temps_exec, 2)) + " secondes.", bg='white')
    temps_en_minutes = Label(fen2, text="La simulation a duré " + str((temps_exec)//60) + " minutes et " + str((round(temps_exec%60),2)) + " secondes.", bg='white')
    suite = Label(fen2, text = "Maintenant, vous voulez : ", bg='white')
    quitter = Button(fen2, text="Quitter", command = fen2.quit)

    retour = IntVar()  # creation de variable-retour
    voir_simulation = Checkbutton(fen2, variable=retour, text="Je veux voir le résultat de la simulation graphique en quittant cette fenêtre")


    if temps_exec <= 60:
        temps_en_secondes.pack(padx = 10, pady = 10)
    else :
        temps_en_minutes.pack(padx=10, pady=10)

    suite.pack(padx = 10, pady = 5)
    voir_simulation.pack(padx = 10, pady = 5)
    quitter.pack(padx = 10, pady = 5)

    fen2.mainloop()

    # recuperation de la valeur lors de la sortie de la boucle mainloop():
    if retour.get() == 1:  # la variable 'retour' = 1 si la case est cochee, 0 sinon
        liste_photos = parseur.recup_output()
        graphique = Graphique(nombre_tours, liste_satellites, None, liste_photos)
        graphique.initialisation()
    else :
        print("blop")

    # Exécution de l'interface graphique pour lire un fichier output

    # if voir_simulation == True:
    #     liste_photos = parseur.recup_output()
    #     graphique = Graphique(nombre_tours, liste_satellites, None, liste_photos)
    #     graphique.initialisation()
