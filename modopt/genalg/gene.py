# modopt/genalg/gene.py

import random

class Gene(object):
    """
    Fundamental unit of genetic information.

    """
    def __init__(self, values, key=None):
        self.values = values
        self.key = key

    def mutate(self):
        return random.choice(self.values)