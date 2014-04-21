import numpy as np
import sys
import os, os.path

ga_path = os.path.abspath(__file__)
ga_path = os.path.dirname(ga_path)
ga_path = os.path.dirname(ga_path)

sys.path.insert(0, ga_path)
from genalg import Organism, Species, Genome

target = {'a':4, 'b':1, 'c':7, 'd':3, 'e':9, 'f':1}
print 'Attempting to reproduce:'
print target
tarr = np.array([ target[x] for x in sorted(target.keys()) ])

def objective(a,b,c,d,e,f):
    """
    Returns the "rms" error for variables a, b and c with respect to three
    pre-assigned values A, B and C
    """
    arr = np.array([a,b,c,d,e,f])
    return np.average((arr - tarr)**2)

genome = {'a':np.linspace(0,10,1000), 
          'b':np.linspace(0,10,1000), 
          'c':np.linspace(0,10,1000),
          'd':np.linspace(0,10,1000),
          'e':np.linspace(0,10,1000),
          'f':np.linspace(0,10,1000),
          }

genome = Genome(genome)
spec = Species(genome, objective=objective)
spec.evolve(300)

print 'found:'
print spec.best
