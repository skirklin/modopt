# modopt/genalg/species.py

import random
import json

from organism import Organism
from genome import Genome

class Species(object):
    ### population options
    pop_size = 100
    organism = Organism
    f_replace = 0.5
    
    ### mutation
    p_mutate = 0.1
    
    ### Selection
    tourn_size = 4
    
    def __init__(self, genome):
        self.genome = genome
        self.population = [ self.spawn_organism() for i in range(self.pop_size) ]

    def __len__(self):
        return len(self.population)

    def __getitem__(self, index):
        return self.population[index]

    def sort(self):
        self.population = sorted(self.population, key=lambda x: x.fitness)

    def best(self):
        self.sort()
        return self[0]

    def spawn_organism(self):
        org = Organism()
        org.species = self
        org.genes = self.genome.get_genes()

    def select(self, method='roulette'):
        if method == 'tournament':
            return self.tournament_select()
        elif method == 'roulette':
            return self.roulette_select()

    def cull_the_weak(self, n_survivors):
        self.sort()
        self.population = self.population[:n_survivors]
        return self.population
    
    def tournament_select(self):
        breeders = []
        for i in range(self.tourn_size):
            breeders.append(random.choice(self))
        return sorted(breeders, key=lambda org: org.fitness)

    def roulette_select(self):
        total = sum([ org.fitness for org in self ])
        score = random.random()*total
        self.sort()
        v = 0.0
        for org in self:
            v += org.fitness
            if v > score:
                return org

    def next_generation(self):
        raise NotImplementedError

    def create_generation(self):
        self.sort()
        max_ind = self.pop_size*(1-self.f_replace)
        gen = [ o for i, o in enumerate(self) if i < max_ind ]

        while len(gen) < self.pop_size:
            parent1 = self.select()
            parent2 = self.select()
            child = parent1.mate_with(parent2)
            child.mutate(self.p_mutate)
            gen.append(child)
        return gen
