# modopt/genalg/population.py

import random

from organism import Organism

class Population:
    """
    A collection of Organisms.

    """
    ### population options
    pop_size = 0.0
    organism = Organism
    f_replace = 0.5
    
    ### mutation
    p_mutate = 0.1
    
    ### Selection
    tourn_size = 4
    

    def __init__(self):
        self.organisms = [ self.organism() for i in range(self.pop_size) ]

    def __getitem__(self, index):
        return self.organisms[index]

    def __len__(self):
        return len(self.organisms)

    def sort(self):
        self.organsims = sorted(self.organisms, key=lambda org: org.fitness)
        
    def best(self):
        self.sort()
        return self[0]

    def cull_the_weak(self, n_survivors):
        self.sort()
        return self[:n_survivors]
        
    def select(self, method='roulette'):
        if method == 'tournament':
            return self.tournament_select()
        elif method == 'roulette':
            return self.roulette_select()

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
        new_pop = Population()
        for org in self:
            org.fitness_function()
        
        while len(new_pop) < len(self):
            return
    
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
        