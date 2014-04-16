import random
from numpy import linspace

class MetaModel:
	use_models = 10
	models = set()
	vars = {}
	weights = {}

	@classmethod
	def add_model(cls, model, keywords={}):
		'''
		Provide an sklearn model, plus any keywords you want to optimize over. The keywords are given
		in the form of a dict of keyword:[list, of, choices].
		'''
		cls.models.add(model)
		cls.vars[model] = keywords
		cls.weights[model] = 1.0
		
	def __init__(self):
		self.randomize()
		while not self.valid:
			self.randomize()

	@property
	def values(self):
		values = {}
		for k in self.cont_vars.keys():
			values[k] = self.genes[k]
		for k, func in self.functions.items():
			values[k] = func(self)
		for k, v in self.disc_vars.items():
			if self.genes[k]:
				values[k] = v[0]
			else:
				values[k] = v[1]
		return values

	@property
	def valid(self):
		keys = self.cont_vars.keys() 
		keys += self.functions.keys()
		keys += self.disc_vars.keys()
		keys += self.constants.keys()
		if not len(set(keys)) == len(keys):
			print 'Some gene names are duplicates!'
			exit(-1)
		return all( constraint(self) for constraint in self.constraints )

	def randomize(self):
		for k, vals in self.cont_vars.items():
			self.genes[k] = random.choice(linspace(self.cont_vars[k][0], 
			self.cont_vars[k][1], 1e3))
			for k in self.disc_vars:
				self.genes[k] = random.choice(self.disc_vars[k])

	def __str__(self):
		return json.dumps({
			'functions':self.functions,
			'cont_vars':self.cont_vars,
			'disc_vars':self.disc_vars,
			'constants':self.constants,
			'constraints':self.constraints,
			'genes':self.genes})

	def load(self, jstring):
		jdict = json.loads(jstring)
		self.functions = jdict['functions']
		self.cont_vars = jdict['cont_vars']
		self.disc_vars = jdict['disc_vars']
		self.constants = jdict['constants']
		self.constraints = jdict['constraints']
		self.genes = jdict['genes']
		
### model optimization specific

	def fit(self, X=None, y=None):
		for model in self.models:
			model.fit(X, y)
			
	def predict(self, X=None):
		