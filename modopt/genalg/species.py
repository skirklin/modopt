# modopt/genalg/species.py

import random
import json
import logging

from organism import Organism
from genome import Genome

logger = logging.getLogger(__name__)

class Species(object):
    ### population options
    pop_size = 100
    f_replace = 0.2
    
    ### mutation
    p_mutate = 0.3
    
    ### Selection
    tourn_size = 4

    ### history
    past = []
    
    def __init__(self, genome, objective=None):
        self.genome = genome
        self.population = [ self.spawn_organism() for i in range(self.pop_size) ]
        if not objective is None:
            self.objective = objective
        self.n_keep = self.pop_size - int(round(self.f_replace*self.pop_size))

    def __len__(self):
        return len(self.population)

    def __getitem__(self, index):
        return self.population[index]

    def sort(self):
        self.evaluate()
        self.population = sorted(self.population, key=lambda x: x.fitness)

    @property
    def best(self):
        self.sort()
        return self[0]

    def spawn_organism(self):
        org = Organism(self.genome.get_genes())
        org.species = self
        return org

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
        v = 0.0
        for org in self:
            v += org.fitness
            if v > score:
                return org

    def next_generation(self):
        new_gen = list(self.population[:self.n_keep])
        while len(new_gen) < self.pop_size:
            o1 = self.select()
            o2 = self.select()
            o3 = o1.mate(o2)
            o3.mutate(p_mutate=self.p_mutate)
            new_gen.append(o3)
        self.population = new_gen
        self.sort()

    def create_generation(self):
        max_ind = self.pop_size*(1-self.f_replace)
        gen = [ o for i, o in enumerate(self) if i < self.n_keep ]

        while len(gen) < self.pop_size:
            parent1 = self.select()
            parent2 = self.select()
            child = parent1.mate_with(parent2)
            child.mutate(self.p_mutate)
            gen.append(child)
        return gen

    def evaluate(self):
        for org in self:
            if org.fitness is None:
                org.fitness = self.objective(**org)

    def objective(self, **kwargs):
        """
        Placeholder for a custom function that takes an organisms genes as
        kwargs, and returns a fitness value (float).
        """
        raise NotImplementedError("Must specify a fitness function.")

    def track_progress(self):
        return True

    history = []
    def evolve(self, limit=100):
        self.evaluate()
        self.history.append(self.best)

        for i in range(limit):
            self.next_generation()
            self.evaluate()
            self.track_progress()
