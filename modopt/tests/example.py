import sys, os.path
path = os.path.dirname(os.path.abspath(__file__))
path = os.path.dirname(path)
path = os.path.dirname(path)
sys.path.insert(0, path)
from modopt import *
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.datasets import load_boston

"""
To do:
    Use mldata tool with sklearn to get a standard test dataset.
"""

def boston_test():
    boston = load_boston()

    mm = MetaModel()
    mm.add_model(GradientBoostingClassifier,
                 keywords={'max_depth':range(1,10),
                           'min_samples_split':range(2,10)})

    mm.add_model(RandomForestClassifier,
                 keywords={'min_samples_leaf':range(1,10),
                           'max_features':['auto','sqrt','log2']})
                                     
    opt = Optimizer(model=mm, train=train)

    opt()

def optimizer_test():
    return True
