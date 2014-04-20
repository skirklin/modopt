# modopt/genalg/organism.py

import random

class Organism(object):
    """
    A collection of Genes.

    """
    genes = []

    def __init__(self):
        self.fitness = 0.0
        self.genotype = [ gene.mutate() for gene in self.genes ]

    def mutate(self, p_mutate=0.1):
        genes = []
        for gene in self.genes:
            if random.random() < p_mutate:
                genes.append(gene.mutate())
            else:
                genes.append(gene)
        self.genes = genes

    def mate(self, mate):
        child = Organism()
        genes = []
        for g1, g2 in zip(self.genes, mate.genes):
            if random.random() < 0.5:
                genes.append(g1)
            else:
                genes.append(g2)
        child.genes = genes
        return child
        
    def fitness_function(self):
        self.fitness = 1.0
        return self.fitness
