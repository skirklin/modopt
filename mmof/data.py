import numpy as np
import os, os.path
from dateutil.parser import parse
import pandas as pd

class Data:
	'''
	Data objects must have an attribute 'X' and may have an attribute 'y', 
	which contain the descriptors, and assigned values respectively. In general
	this class may need to be built from the ground up for each new contest.
	'''

	def __init__(self, source_file, target=None):
		df = pd.read_csv(source_file)
		self.target = None
		if target is not None:
			self.target = df.pop(target)
		self.features = df
		
	@property
	def X(self):
		return np.array(self.features)
	
	@property
	def y(self):
		if self.target is not None:
			return np.array(self.target)