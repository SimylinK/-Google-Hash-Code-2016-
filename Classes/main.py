from Collection import Collection
from Satellite import Satellite
from Parseur import Parseur
from ZoneGlobe import ZoneGlobe
from Photo import Photo
from Distributeur import Distributeur
import math

parseur = Parseur()
nombre_tours, nombre_satellites, liste_satellites, liste_collections = parseur.recup()
distrib = Distributeur(nombre_tours, nombre_satellites, liste_satellites, liste_collections,parseur.liste_zones)
nb_photos_prises = distrib.algo_opti()
parseur.creer_output(parseur.liste_zones,nb_photos_prises)