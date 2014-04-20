# modopt/genalg/organism.py

import random
import json

class Organism(object):
    """
    A collection of Genes.
    """

    fitness = 0.0
    def mutate(self, p_mutate=0.1):
        for gene, current in self.genes.items():
            if random.random() > p_mutate:
                continue
            self.genes[gene] = random.choice(self.species.genome[gene])
        self.genes = genes

    def mate(self, mate):
        child = Organism()
        child.genes = dict(self.genes)
        for gene in self.genes:
            if random.random() < 0.5:
                child.genes[gene] = mate.genes[gene]
        return child
        
    def write(self):
        genes = json.dumps(self.genes)
        genome = self.species.genome.write()
        return genes, genome

    @staticmethod
    def read(data):
        self.genes = json.loads(data)

    def fitness_function(self, **kwargs):
        """
        Placeholder for a custom function that takes an organisms genes as
        kwargs, and returns a fitness value (float).
        """
        raise NotImplementedError("Must specify a fitness function.")

