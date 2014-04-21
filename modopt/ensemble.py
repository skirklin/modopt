import random

import numpy as np
from sklearn.base import RegressorMixin, BaseEstimator
from sklearn import cross_validation

class EnsembleRegressor(RegressorMixin, BaseEstimator):
    """Basic EnsembleRegressor model.

    Parameters
    ----------
    models : seq
        Models to constitute the ensemble

    weights : seq, len(weights) == len(models)
        Relative importance of constituent models. If 

    keywords: seq, len(keywords) == len(models)
        Keyword arguments to supply to constituent models. Should be a list of
        dicts. 

    """
    models = []
    weights = []
    keywords = []

    def __init__(self, models, weights=None, keywords=None, train_size=0.5):
        if weights is None:
            weights = np.array([ 1.0 for i in models ])
        assert len(weights) == len(models)
        self.weights = np.array(weights) / sum(weights)
        if keywords is None:
            keywords = [ {} for i in models ]
        self.models = [ m(**kw) for m, kw in zip(models, keywords) ]
        
        self.train_size = train_size
        
    def fit(self, X, y):
        for model in self.models:
            X1, X2, y1, y2 = cross_validation.train_test_split(X, y, 
                    train_size=self.train_size)
            model.fit(X1, y1)
        return self
            
    def predict(self, X):
        predictions = []
        for model, weight in zip(self.models, self.weights):
            predictions.append(model.predict(X)*weight)
        predictions = np.sum(predictions, 0)
        return predictions
