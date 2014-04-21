modopt
======

Toolkit for creating and optimizing an arbitrary ensemble of sklearn models.

sklearn only supports ensembles of a single classifier type, with a single set 
of parameters. I made this package to allow creating ensembles of multiple 
types of models, or the same model but with different model parameters. Since this 
represents a very large optimization space (model weights, model parameters), it 
is bundled with a simple genetic algorithm code to allow for global optimization 
over a very large parameter space.

Still under active development. Currently only an EnsembleRegressor is working, but an
EnsembleClassifier and EnsembleCluster is coming. The genetic algorithm code is also 
working, but has not been integrated for actual model optimization yet. Work can also 
still be done to improve the performance of GA.
