__author__ = 'ghahr'

import csv
import json
import math
import random
from matplotlib import pyplot
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import correlation

def readData(fileName):
    datasetDict = []
    dataset = []
    with open(fileName) as csvfile:
        reader = csv.DictReader(csvfile)
        print('here')
        nameOfAttributes = reader.fieldnames
        for row in reader:
            datasetDict.append(row)
            dataset.append(row.values())
            # print row.values()
        print('after')
    return datasetDict, dataset, nameOfAttributes


def write_in_file(fileName, data, columnNames):
    with open(fileName, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columnNames)

        writer.writeheader()
        for d in data:
            dict = {}
            for i in range(len(d)):
                dict[columnNames[i]] = d[i]
            writer.writerow(dict)

def preprocess_data(data, nameOfAttributes):
    newDataset = []
    # print data[0]
    avgValues = []
    size1 = len(data)
    size2 = len(data[0])
    newAttributes = []
    for i in range(size2):
        sum = 0
        count = 0
        flag = False
        for j in range(size1):
            try:
                if(data[j][i] != ''):
                    sum += float(data[j][i])
                    count += 1
            except ValueError:
                flag = True
                break
        if(flag == True or count == 0):
            avgValues.append("unknown")
        else:
            avgValues.append(sum/count)
            newAttributes.append(nameOfAttributes[i])
    for d in data:
        newD = []
        for i in range(len(d)):
            try:
                if(avgValues[i] != "unknown"):
                    if(d[i] == ''):
                        newD.append(avgValues[i])
                    else:
                        newD.append(float(d[i]))
            except ValueError:
                pass
        newDataset.append(newD)
    return newDataset, newAttributes


def printData(printedData):
    print(len(printedData))
    for i in range(len(printedData)):
        # print(printedData[i]('Year'))
        print(json.dumps(printedData[i]))

def random_sampling(dataset, labels, centroids, sampledDataSize):
    sampledData = []
    sampledLabels = []
    for i in range(sampledDataSize):
        index = random.randint(0, len(dataset)-1)
        sampledData.append(dataset[index])
        sampledLabels.append(labels[index])
    return sampledData, sampledLabels


def write_kmean_result_in_file(data):
    centroids, labels = k_mean_clustering(data)
    with open("kmean_result.csv", 'wb') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(labels)
        for c in centroids:
            spamwriter.writerow(c)

def read_k_mean_clustering():
    with open("kmean_result.csv") as csvfile:
        spamreader = csv.reader(csvfile)
        list_rows = []
        for row in spamreader:
            list_rows.append(row)
    return list_rows[0], list_rows[1:]

def adaptive_sampling(data, labels, centroids, sampledDataSize):
    for i in range(len(labels)):
        labels[i] = int(labels[i])
    probabilities = [0] * len(centroids)
    for l in labels:
        probabilities[l] += 1
    for i in range(len(probabilities)):
        probabilities[i] = probabilities[i] * 1.0 / len(labels)
    sampledData = []
    sampledLabels = []
    i = 0
    while(i<sampledDataSize):
        index = random.randint(0, len(data) - 1)
        if(random.random >= probabilities[labels[index]]):
            sampledData.append(data[index])
            sampledLabels.append(labels[index])
            i += 1
    return sampledData, sampledLabels

def k_mean_clustering(data):
    k = 8
    k_range = range(1,14)
    newData = np.array(data)
    # centroids,labels,inertia = cluster.k_means(newData,n_clusters=k)
    kmeans_var = KMeans(init='k-means++', n_clusters=k, n_init=10).fit(newData)
    centroids = kmeans_var.cluster_centers_
    labels = kmeans_var.labels_
    return centroids, labels

# http://scikit-learn.org/stable/auto_examples/decomposition/plot_pca_3d.html
def my_pca(data):
    X = np.array(data)
    pca = PCA(n_components=2)
    pca.fit(X)
    results2 = pca.transform(X)
    return results2

def find_intrinsic_dimensionality(data):
    X = np.array(data)
    pca = PCA(n_components=10)
    pca.fit(X)
    results = pca.explained_variance_ratio_
    return results

def split_array(myarray):
    X = []
    Y = []
    for el in myarray:
        X.append(el[0])
        Y.append(el[1])
    return X, Y

def euclidean_MDS(data):
    seed = np.random.RandomState(seed=3)
    similarities = euclidean_distances(data)
    mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=1)
    pos = mds.fit_transform(similarities)
    return pos

def cosine_MDS(data):
    seed = np.random.RandomState(seed=3)
    similarities = cosine_similarity(data, data)
    mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=4)
    pos = mds.fit_transform(similarities)
    return pos

# http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.distance.correlation.html
def correlation_MDS(data):
    seed = np.random.RandomState(seed=3)
    similarities = [[0 for x in range(len(data))] for x in range(len(data))]
    for i in range(len(data)):
        for j in range(len(data)):
            similarities[i][j] = correlation(data[i], data[j])
    mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                   dissimilarity="precomputed", n_jobs=1)
    pos = mds.fit_transform(similarities)
    return pos

def isomap(data):
    X = np.array(data)
    X_iso = manifold.Isomap(n_neighbors = 10, n_components=2).fit_transform(X)
    return X_iso

if __name__ == "__main__":
    # at first, I read data and preprocessed them and then write processed data in a new file
    # datasetDict, original_dataset, original_nameOfAttributes = readData('prosperLoanData.csv')
    # dataset, nameOfAttributes = preprocess_data(original_dataset, original_nameOfAttributes)
    # write_in_file("processed_data.csv", dataset, nameOfAttributes)

    datasetDict, original_dataset, original_nameOfAttributes = readData('processed_data.csv')

    # sampledData, sampledLabels = adaptive_sampling(dataset)
    # # pcaData = my_pca(sampledData, nameOfAttributes)
    # print "before"
    # correlation_MDS(sampledData)