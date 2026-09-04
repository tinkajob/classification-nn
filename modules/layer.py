import random
import numpy as np

class Layer:
    def __init__(self, layer_size):
        self.size = layer_size
        self.biases = [random.random()] * self.size
        