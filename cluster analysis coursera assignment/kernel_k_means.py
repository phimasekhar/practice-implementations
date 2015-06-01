from utils import *
from math import exp


def kernel(data, sigma):
    nData = len(data)
    Gram = [[0] * nData for i in range(nData)]
    # TODO
    # Calculate the Gram matrix
    # Gram = nData*nData matrix
    for i in range(nData):
        for j in range(nData):
            Xi = data[i]
            Xj = data[j]
            Xij = squaredDistance(Xi, Xj)
            K_Xi_Xj = exp(-(Xij/(2.0*sigma**2)))
            Gram[i][j] = K_Xi_Xj

    return Gram
