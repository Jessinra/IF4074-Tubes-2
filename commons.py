import numpy as np

def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))