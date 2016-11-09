#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Module de définition des structures de données de Poly#.
"""

# ajouter dans cette liste tous les symboles 'importables'
__all__ = ['Useless']


class Useless:
    """
        Une classe vraiment inutile.
    """
    def __str__(self):
        return "Poly# vide"


if __name__ == "__main__":
    inutile = Useless()
    print('J\'ai créé un {}.'.format(inutile))
