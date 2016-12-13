#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Imports servant à :
    - à utiliser le module graphique tkinter :
        import tkinter
"""

from tkinter import *

class Interface:
    """
    Classe chargée de :
    Créer une interface utilisateur visant à choisir le fichier d'input.
    Créer une interface utilisateur visant à choisir si lancer ou non l'interface graphique de la map monde.
    """
    def __init__(self):
        self.fichier_input = ""
        self.voir_simulation = False

    def creer_interface_lancement(self):
        """
        Méthode chargée de :
        Créer une interface utilisateur visant à choisir le fichier d'input.
        """
        fen1 = Tk(className='#HashCode | Choix de la simulation') # Création de la fenêtre
        fen1.configure(bg='white') # Configuration des paramètres de la fenêtre
        canvas = Canvas(fen1, width=600, height=300) # Création du canvas
        photo = PhotoImage(file="docs/Logo_polyhash_code_signe.png") # Definition de la photo
        canvas.create_image(50, 50, anchor=NW, image=photo)
        canvas.pack(side=TOP and RIGHT)
        canvas.configure(bg='white')

        label = Label(fen1, text="Quel fichier utiliser pour la simulation ?", bg='white') # Affichage de texte de communication avec l'utilisateur

        retour = IntVar()  # Crée une variable entière pour recevoir la valeur retour
        retour.set(3)  # Le bouton forever_alone est le choix par defaut (value=3)

        #Création des boutons pour le choix du fichier d'input
        weekend = Radiobutton(fen1, text="weekend", variable=retour, value=1, bd=2, bg='white')
        overlap = Radiobutton(fen1, text="overlap", variable=retour, value=2, bd=3, bg='white')
        forever_alone = Radiobutton(fen1, text="forever_alone", variable=retour, value=3, bd=3, bg='white')
        constellation = Radiobutton(fen1, text="constellation", variable=retour, value=4, bd=3, bg='white')

        quitter = Button(fen1, text="Lancer le programme", command=fen1.quit, width=25, height=1)

        # Affichage des labels et boutons
        label.pack(padx=10, pady=5)
        weekend.pack()
        overlap.pack()
        forever_alone.pack()
        constellation.pack()
        quitter.pack(padx=10, pady=10, side=RIGHT and BOTTOM)

        fen1.mainloop() # Ouverture de la fenêtre
        fen1.destroy() #Destruction de la fenêtre après fermeture pour ne pas qu'elle reste affichée

        # Choix du fichier d'input en fonction de la valeur de retour
        if retour.get() == 1:
            self.fichier_input = "weekend"
        elif retour.get() == 2:
            self.fichier_input = "overlap"
        elif retour.get() == 3:
            self.fichier_input = "forever_alone"
        else:
            self.fichier_input = "constellation"

    def creer_interface_fin(self, temps_exec):
        """
        Méthode chargée de :
        Créer une interface utilisateur visant à choisir si lancer ou non l'interface graphique de la map monde.
        :param temps_exec: un flottant : le temps d'éxecution du programme principal
        """
        fen2 = Tk(className='#HashCode | Résultat de la simulation') # Création de la fenêtre
        fen2.configure(bg='white') # Configuration des paramètres de la fenêtre

        # Création des labels et boutons
        temps_en_secondes = Label(fen2, text="La simulation de " + self.fichier_input + " a duré " + str(
            round(temps_exec, 2)) + " secondes.",
                                  bg='white')
        temps_en_minutes = Label(fen2, text="La simulation a duré " + str(temps_exec // 60) + " minutes et " + str(
            round(temps_exec % 60, 2)) + " secondes.", bg='white')
        suite = Label(fen2, text="En quittant cette fenêtre : ", bg='white')
        quitter = Button(fen2, text="Quitter", command=fen2.quit)

        voir = IntVar()  # creation de variable-retour
        voir.set(1)
        voir_simulation = Checkbutton(fen2, variable=voir,
                                      text="Je veux voir la simulation graphique", bg='white')

        # Le type d'affichage du temps dépend de la durée de la simulation
        if temps_exec <= 60:
            temps_en_secondes.pack(padx=10, pady=10) # On affiche le temps en secondes si la simulation a duré moins de 1 minute
        else:
            temps_en_minutes.pack(padx=10, pady=10) # Sinon on l'affiche en minutes et secondes

        # Affichage des labels et boutons
        suite.pack(padx=10, pady=5)
        voir_simulation.pack(padx=10, pady=5)
        quitter.pack(padx=10, pady=5)

        fen2.mainloop() # Ouverture de la fenetre
        fen2.destroy() #Destruction de la fenêtre après fermeture pour ne pas qu'elle reste affichée

        if voir.get() == 1: # Si l'utilisateur a choisi de voir la simulation
            self.voir_simulation = True # On donne à la variable voir_simulation la valeur True

# Tests des fonctions
if __name__ == "__main__":
    interface1 = Interface()
    temps_exec = 80
    interface1.creer_interface_lancement()
    print(interface1.fichier_input)
    interface2 = Interface()
    print(interface2.creer_interface_fin(80))
    print(interface2.voir_simulation)