# modopt/genalg/organism.py

import random
import json

class Organism(dict):
    """
    A collection of Genes.
    """

    fitness = None
    def mutate(self, p_mutate=0.1):
        for gene, current in self.items():
            if random.random() > p_mutate:
                continue
            self[gene] = random.choice(self.species.genome[gene])

    def mate(self, mate):
        child = Organism(self.items())
        child.species = self.species
        for gene in self:
            if random.random() < 0.5:
                child[gene] = mate[gene]
        return child
        
    def write(self):
        genes = json.dumps(self.items())
        genome = self.species.genome.write()
        return genes, genome

    @staticmethod
    def read(data):
        for k,v in json.loads(data):
            self[k] = v

