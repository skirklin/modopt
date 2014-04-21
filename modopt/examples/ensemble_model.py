import sys
import os, os.path
import numpy as np

from sklearn import cross_validation
from sklearn import datasets
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

ga_path = os.path.abspath(__file__)
ga_path = os.path.dirname(ga_path)
ga_path = os.path.dirname(ga_path)

sys.path.insert(0, ga_path)
from ensemble import EnsembleRegressor

## Get testing and training datasets
boston = datasets.load_boston()
X_train, X_test, y_train, y_test = cross_validation.train_test_split(
        boston.data, boston.target, train_size=0.5)

## Define the models and weights for the ensemble
models = [
        GradientBoostingRegressor,  GradientBoostingRegressor,
        GradientBoostingRegressor,  GradientBoostingRegressor
        ]# KNeighborsRegressor, KNeighborsRegressor, KNeighborsRegressor ]

#models = [ SVR ]

print 'Evaluating Ensemble train_size dependence:'
print '------------------------------------------'
for i in [0.2, 0.4, 0.6, 0.8]:
    print i, ':'
    ensemble = EnsembleRegressor(models, train_size=i)

    ## The EnsembleRegressor inherits from sklearn baseclasses, and supports many
    #       same function calls, e.g. fit, predict and score.
    ensemble.fit(X_train, y_train)
    print ', '.join([ '%0.3f' % m.score(X_test, y_test) for m in ensemble.models ])
    print 'Ensemble score:', ensemble.score(X_test, y_test)

