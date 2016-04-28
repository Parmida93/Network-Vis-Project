__author__ = 'ghahr'

import random
import numpy as np
from sklearn.cluster import KMeans

def random_sampling(data, sampledDataSize):
    sampledData = []
    for i in range(sampledDataSize):
        index = random.randint(0, len(data)-1)
        sampledData.append(data[index])
    return sampledData


def k_mean_clustering(data):
    k = 8
    k_range = range(1,14)
    newData = np.array(data)
    # centroids,labels,inertia = cluster.k_means(newData,n_clusters=k)
    kmeans_var = KMeans(init='k-means++', n_clusters=k, n_init=10).fit(newData)
    centroids = kmeans_var.cluster_centers_
    labels = kmeans_var.labels_
    return centroids, labels


def reservoir_sampling(data, k):
    result = []
    for i in range(0, k):
        result.append(data[i])
    for i in range(k, len(data)):
        j = random.randint(0, i - 1)
        if(j <= k):
            result[j] = data[i]
    return result
