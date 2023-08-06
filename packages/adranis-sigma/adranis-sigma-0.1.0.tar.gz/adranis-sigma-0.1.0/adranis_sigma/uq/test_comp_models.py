""" Computational models that are used during unit testing
"""
import numpy as np


def XsinX(X):
    X = np.array(X, ndmin=2)
    return X * np.sin(X)


def hat2d(X):
    # 2D hat function
    # see https://www.uqlab.com/reliability-2d-hat-function
    X = np.array(X, ndmin=2)
    t1 = np.square(X[:, 0] - X[:, 1])
    t2 = 8 * np.power(X[:, 0] + X[:, 1] - 4, 3)
    return 20 - t1 - t2
