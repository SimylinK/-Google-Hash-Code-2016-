#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Photo import Photo

class ActionCamera:
    """
        Classe composée de :
        Un certain nombre de photos qu'il faudra prendre pour avoir les
        points qui lui sont associés. 
    """

    def __init__(self, tour, mouvement_latitude = None,
                 mouvement_longitude = None):
        self.tour = tour
        self.mouvement_latitude = mouvement_latitude
        self.mouvement_longitude = mouvement_longitude
        self.photo = self.get_photo()


    def get_photo(self):
        return "blop" #je sais pas encore comment faire
        
