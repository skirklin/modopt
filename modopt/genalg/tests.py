# modopt/genalg/tests.py

import random
import numpy as np
import unittest

from gene import Gene
from organism import Organism
from population import Population

class GeneTestCase(unittest.TestCase):
    
    def setUp(self):
        gene1 = Gene(range(10))
        gene2 = Gene('abcdefg')
        gene3 = Gene(np.linspace(0,1, 100))
        self.genes = [ gene1, gene2, gene3 ]
        
    def mutate_test(self):
        for gene in self.genes:
            self.assertTrue(gene.mutate() in gene.values)
            
class OrganismTestCase(unittest.TestCase):
    def setUp(self):
        gene1 = Gene(range(10))
        gene2 = Gene(range(20))
        gene3 = Gene('abcdefg')
        org = Organism
        org.genes = [gene1, gene2, gene3]
            
    def mate_test(self):
        return True

class PopulationTestCase(unittest.TestCase):
    def setUp(self):
        def func_factory(a, b, c, d):
            print '%s*x**3 + %s*x**2 + %s*x + %s' % (a,b,c,d)
            def func(x):
                return a*x**3 + b*x**2 + c*x + d
            return func
        if False:
            
            a = random.random()
            b = random.random()
            c = random.random()
            d = random.random()
            self.right = [a,b,c,d]
            soln = func_factory(a, b, c, d)
            
            xs = np.linspace(-10, 10, 100)
            ys = map(soln, xs)
            
            def fitness_function(self, a,b,c,d):
                func = func_factory(a,b,c,d)
                yps = map(func, xs)
                self.fitness = np.average(yps - ys)
            
            a_gene = Gene(random.random(), key='a')
            b_gene = Gene(random.random(), key='b')
            c_gene = Gene(random.random(), key='c')
            d_gene = Gene(random.random(), key='d')
            
            org = Organism
            org.genes = [a_gene, b_gene, c_gene, d_gene]
            org.fitness_function = fitness_function
            self.pop = Population(100, organsim=org)
            self.org = org

    def generation_test(self):
        #pop.next_generation()
        return True