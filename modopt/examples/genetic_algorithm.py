import numpy as np
import sys
import os, os.path

ga_path = os.path.abspath(__file__)
ga_path = os.path.dirname(ga_path)
ga_path = os.path.dirname(ga_path)

sys.path.insert(0, ga_path)
from genalg import Organism, Species, Genome

target = {'a':4, 'b':1, 'c':7}
print 'Attempting to reproduce:'
print target
tarr = np.array([ target[x] for x in ['a','b', 'c']])

def objective(a,b,c):
    """
    Returns the "rms" error for variables a, b and c with respect to three
    pre-assigned values A, B and C
    """
    arr = np.array([a,b,c])
    return np.average((arr - tarr)**2)**0.5

genome = {'a':np.linspace(0,10,1000), 
          'b':np.linspace(0,10,1000), 
          'c':np.linspace(0,10,1000)}

genome = Genome(genome)
spec = Species(genome, objective=objective)
spec.f_replace = 0.9
spec.p_mutate = 0.4
spec.evolve()

print 'found:'
print spec.best, spec.best.fitness
