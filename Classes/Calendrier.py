#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Imports servant à :
    - à réutiliser les classes définies dans les autres fichiers :
        import Collection : classe Collection
        import Satellite : classe Satellite.
"""

from Collection import Collection
from Satellite import Satellite


class Calendrier:
    """Classe chargée de :
    distribuer les photos entre les satellites et des les associer dans un calendrier
    """
