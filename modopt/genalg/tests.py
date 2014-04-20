# modopt/genalg/tests.py

import random
import numpy as np
import unittest

from species import Organism, Species, Genome

class GenAlgTestCase(unittest.TestCase):
    def genome_test(self):
        genome = Genome({
            'A':range(10),
            'B':'abcdefg',
            'C':np.linspace(0, 1, 100)})
        gene_str = genome.write()
        new_genome = Genome.read(gene_str)
        seq = genome.get_genes()

    def species_test(self):
        genome = Genome({
            'A':range(10),
            'B':'abcdefg',
            'C':np.linspace(0, 1, 100)})
        species = Species(genome)

    def organism_test(self):
        genome = Genome({
            'A':range(10),
            'B':'abcdefg',
            'C':np.linspace(0, 1, 100)})
        species = Species(genome)
        organism = species.spawn_organism()
