# modopt/genalg/genome.py

import numpy as np
import random
import json

class Genome(dict):
    def clean_data_types(self):
        for k,v in self.items():
            if isinstance(v, np.ndarray):
                self[k] = v.tolist()

    def write(self):
        self.clean_data_types()
        return json.dumps(self.items())

    @staticmethod
    def read(data):
        return Genome(json.loads(data))

    def get_genes(self):
        return dict((k, random.choice(v)) for k, v in self.items())

