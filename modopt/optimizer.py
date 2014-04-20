import random
import os
import sys
import itertools
import numpy as np
from collections import *
import time

class Optimizer:
    """
    Optimizer objects hold all of the information and instructions for fitting
    the potential.

    Fit Options
    ===========
    fit_size[default=20]: how many data points to fit to
    test_size[default=0]: how many data points to test against independently
    pop_size[default=100]: how many organisms per generation
    weights[default={'energy':10, 'stress':1, 'force':1}]: a dictionary
        containing the relative weights of force, stress and energy errors

    GA Options
    ==========
    tourn_size[default=5]: how many organisms to compete for procreation
    f_replace[default=1.0]: how many organisms to keep back from the previous
        generation, to 'seed' the next one
    p_mutate[default=0.1]: chance of mutating any given gene during breeding.
    first_generation_factor[default=500]: size of the first generation to get a
        pool of reasonably good structures to start with.

    """

    fit_size = 20
    tourn_size = 5
    pop_size = 100
    f_replace = 1.0
    p_mutate = 0.1
    first_generation_factor = 500
    rescale_threshold = 0.05
    sliding_threshold = 0.25

    def __init__(self, model=None, train=None, test=None):
        if model is None or train is None:
            print 'Need to assign a model and a Data set to train'
            exit(-1)
        ### core attributes
        self.model = model
        self.train = train
        
        self.organisms = []
        
    @property
    def best(self):
        evaled = [ self.organisms[o] for o in self.generations[-1]]
        return sorted( evaled, key=lambda x: x.fitness )[0] 
    
    @property
    def all_genes(self):
        genes = []
        for org in self.organisms.values():
            genes.append(org[k] for k in self.keys)
        genes = np.array(genes)
        return genes.T
    
    @property
    def keys(self):
        if not self.organisms:
            self.spawn()
        return self.organisms[0].genes.keys()
        
    ### Selection operators
    def _tournament_select(self):
        orgs=[]
        for i in range(self.tourn_size):
            orgs.append(random.choice(self.generations[-1]))
        orgs = sorted(orgs, key=lambda k: self.organisms[k].fitness)
        return self.organisms[orgs[0]]
    
    def _roulette_select(self):
        total = sum([ self.organisms[k].fitness for k in self.generations[-1] ])
        score = random.random()
        orgs = sorted(self.generations[-1], key=lambda k: self.organisms[k].fitness)
        current = 0.0
        for k in orgs:
            current += self.organsims[k].fitness/total
            if current > score:
                return self.organisms[k]
                    
    def select(self):
        return self._tournament_select()
        
    ### mating operators
    def _mix_mate(self, org1, org2):
        child = self.spawn()
        for k in self.model.cont_vars:
            p1_frac = random.random()
            child.genes[k] = p1_frac*org1.genes[k]+(1-p1_frac)*org2.genes[k]
        for k in self.model.disc_vars:
            if random.random() < 0.5:
                child.genes[k] = org1[k]
            else:
                child.genes[k] = org2[k]
        return child
        
    def mate(self, org1, org2):
        child = self._mix_mate(org1, org2)
        while not child.valid:
            child = self._mix_mate(org1, org2)
        return child
        
    ### mutation operators
    def _mutate(self, org):
        if isinstance(org, int):
            org = self.organisms(org)
        for k in org.cont_vars:
            if random.random() < self.p_mutate:
                org.genes[k] = random.choice(np.linspace(org.cont_vars[k][0], 
                    org.cont_vars[k][1], 1e3))
        for k in org.disc_vars:
            if random.random() < self.p_mutate:
                org.genes[k] = random.choice(org.disc_vars[k])
        return org
        
    def mutate(self, org):
        org = self._mutate(org)
        while not org.valid:
            self._mutate(org)
        return org

    ### Population management

    def spawn(self):
        org = self.model()
        org.id = len(self.organisms)
        self.organisms[org.id] = org
        return org

    def initialize_population(self):
        gen = []
        while len(gen) < self.first_generation_factor*self.pop_size:
            child = self.spawn()
            gen.append(child.id)
        self.generations= [gen]

    def create_generation(self):
        gen = []
        for i in range(int(round(self.pop_size*(1-self.f_replace)))):
            gen.append(self.generations[-1][i])

        while len(gen) < self.pop_size:
            parent1 = self.select()
            parent2 = self.select()
            child = self.mate(parent1, parent2)
            child = self.mutate(child)
            gen.append(child.id)

        self.generations.append(gen)

    ### Optional optimization stuff

    def rescale(self):
        if len(self.organisms) < 1000:
            return
        for k, data in zip(self.genes, self.keys()):
            if k not in self.model.cont_vars:
                continue


    def shift(self):
        if len(self.organisms) < 1000:
            return
        for k, data in zip(self.genes, self.keys()):
            if k in self.model.cont_vars:
                self.model.cont_vars[k] = prune_range(data)
            if k in self.model.disc_vars:
                self.model.disc_vars[k] = prune_values(data)

    def refine_model(self):
        self.rescale()
        self.shift()

    ### data logging

    def update_best(self):
        self.best.save('best.pot')

    def summarize(self):
        print ' - Best fitness:', self.best.fitness
        print ' - Run time:', self.laps[-1]-self.laps[-2], ' seconds' 

    def output(self):
        self.update_best()
        self.summarize()

    ### Actual run command

    def __call__(self, generations=300):
        '''
        GA cycle:

        self.initialize_population()
        self.evaluate()
        self.output()

        for gen in range(generations):
            self.procreate()
            self.evaluate()
            self.output()
        '''
        print 'Generation 0:\n================'
        print ' - Initializing'

        self.laps = [time.time()]
        self.initialize_population()
        self.evaluate()
        self.laps.append(time.time())

        for gen in range(generations):
            print 'Generation %s:\n================' % len(self.generations)
            self.procreate()
            self.evaluate()
            self.laps.append(time.time())
            self.output()
            #self.refine_model()
