from utils import *
import sys
import numpy as np


def computeSSE(data, centers, clusterID):
    # clusterID - cluster mapping for each data point
    sse = 0
    nData = len(data)
    for i in range(nData):
        c = clusterID[i]
        sse += squaredDistance(data[i], centers[c])
    return sse


def updateClusterID(data, centers):
    nData = len(data)

    clusterID = [0] * nData

    for i in range(nData):
        min_distance = sys.maxint
        nearest_clusterID = -1
        for j, center in enumerate(centers):
            distance = squaredDistance(data[i], center)
            if distance < min_distance:
                nearest_clusterID = j
                min_distance = distance
        clusterID[i] = nearest_clusterID

    # TODO
    # assign the closet center to each data point
    return clusterID

# K: number of clusters


def updateCenters(data, clusterID, K):
    nDim = len(data[0])
    centers = [[0] * nDim for i in range(K)]
    # centers is a list of K elements, each with nDimensions
    nData = len(data)
    # clusterID is a list of n elements specifying cluster assignments.
    cluster_elements = {}
    # cluster_elements maps
    for i in range(len(clusterID)):
        # arr = np.empty((nDim,))
        # cluster_elements.setdefault(clusterID[i], arr)
        # cluster_elements[clusterID[i]] = np.vstack(
        #    (cluster_elements[clusterID[i]], np.array(data[i])))
        cluster_elements.setdefault(clusterID[i], [])
        cluster_elements[clusterID[i]].append(data[i])

    for key in cluster_elements.keys():
        cluster_elements[key] = np.array(cluster_elements[key])

    for i, c in enumerate(centers):
        if i in cluster_elements.keys():
            centers[i] = np.mean(cluster_elements[i], axis=0)

        # TODO recompute the centers based on current clustering assignment
        # If a cluster doesn't have any data points, in this homework, leave it to
        # ALL 0s
    return centers


def kmeans(data, centers, maxIter=100, tol=1e-6):
    nData = len(data)

    if nData == 0:
        return []

    K = len(centers)

    clusterID = [0] * nData

    if K >= nData:
        for i in range(nData):
            clusterID[i] = i
        return clusterID

    nDim = len(data[0])

    lastDistance = 1e100

    for iter in range(maxIter):
        clusterID = updateClusterID(data, centers)
        centers = updateCenters(data, clusterID, K)

        curDistance = computeSSE(data, centers, clusterID)
        if lastDistance - curDistance < tol or (lastDistance - curDistance)/lastDistance < tol:
            print "# of iterations:", iter
            print "SSE = ", curDistance
            return clusterID

        lastDistance = curDistance

    print "# of iterations:", iter
    print "SSE = ", curDistance
    return clusterID
