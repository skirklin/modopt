from modopt import *
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

'''
Okay, so this is a basic example for this code.
'''

#First: create the Data we will fit to. To start with, we will just use data
#       we can read in, but don't have to modify at all

train = Data('train.csv', target='label')
test = Data('test.csv')

#Next: build a MetaModel. This is basically the genome of our optimization
#       problem, and will contain information about what models to contain,
#       and how they will be related. To start with we will just use one of
#       each of a few basic models.
##
mm = MetaModel
mm.add_model(GradientBoostingClassifier,
             keywords={'max_depth':range(1,10),
                       'min_samples_split':range(2,10)})

mm.add_model(RandomForestClassifier,
             keywords={'min_samples_leaf':range(1,10),
                       'max_features':['auto','sqrt','log2']})
                                 
opt = Optimizer(model=mm, train=train)
