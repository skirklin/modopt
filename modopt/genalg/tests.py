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
        self.assertTrue(isinstance(seq, dict))
        for k, v in seq.items():
            self.assertTrue(v in genome[k])

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

        org1 = species.spawn_organism()
        org2 = species.spawn_organism()

        org3 = org1.mate(org2)
        org3.mutate()

    def optimizer_test(self):
        target = np.array([5,1,2])
        def objective(a,b,c):
            arr = np.array([a,b,c])
            return np.average((arr - target)**2)**0.5
        genome = {'a':range(10), 'b':range(10), 'c':range(1)}
        genome = Genome(genome)
        spec = Species(genome, objective=objective)
        spec.evaluate()
        spec.evolve()
