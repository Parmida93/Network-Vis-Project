import os
from flask import Flask
from flask import render_template
from flask import request
import json
# from bson import json_util
# from bson.json_util import dumps
# from PreProcessing import adaptive_sampling, random_sampling, my_pca, preprocess_data, readData, \
#     find_intrinsic_dimensionality, write_kmean_result_in_file, euclidean_MDS, cosine_MDS, correlation_MDS, isomap, \
#     read_k_mean_clustering, split_array
# from TextVisulization import compute_tfidf, readFiles
# import TextVisulization
import math
from flask import make_response
from Sampling import binning, random_sampling, reservoir_sampling

app = Flask(__name__)

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DBS_NAME = 'donorschoose'
COLLECTION_NAME = 'projects'
FIELDS = {'school_state': True, 'resource_type': True, 'poverty_level': True, 'date_posted': True, 'total_donations': True, '_id': False}

dataset = []
nameOfAttributes = []
labels = []
centroids = []
sampledLabels = []
sampledData = []

@app.route("/")
def index():
    # global dataset, nameOfAttributes, labels, centroids, sampledData, sampledLabels
    # datasetDict, dataset, nameOfAttributes = readData('processed_data.csv')
    # labels, centroids = read_k_mean_clustering()
    return render_template("index.html")

@app.route("/metrics", methods=['POST'])
def metrics_render():
    type_name = request.form['type_name']
    file_name = request.form['trace_file']
    sampling_type = request.form['sampling_type']
    samplingNo = request.form['samplingNo']
    result = []
    if type_name == "Packet Size" or type_name == "Payload Size":
        result1 = read_file_type1(type_name, file_name)
        result = sampleData(result1, sampling_type, samplingNo)
    elif type_name == "Packet Loss Rate":
        result = read_file_type2(type_name, file_name)
    elif type_name == "HTTPS/QUIC":
        result = read_file_type3(type_name, file_name)
    return json.dumps({'all_packets': result})


@app.route('/radio.gif')
def templated_svg():
    "Example using a template in the templates directory."
    # width = request.args.get('width', '800')
    # height = request.args.get('height', '600')
    gif = open(os.path.join(app.root_path, 'images', 'radio.gif')).read()
    return gif

def sampleData(data, sampling_type, samplingNum):
    result = []
    if sampling_type == "Binning":
        result = binning(data, int(samplingNum))
    elif sampling_type == "Random Sampling":
        result = random_sampling(data, int(samplingNum))
    elif sampling_type == "Reservoir Sampling":
        result = reservoir_sampling(data, int(samplingNum))
    return result


def read_file_type1(type_name, file_name):
    array_result = []
    file_path = './Results/' + type_name + '/' + file_name + '.txt'
    f = open(file_path, 'r')
    for line in f:
        array_result.append(float(line))
    f.close()
    return array_result


def read_file_type2(type_name, file_name):
    array_result = []
    file_path = './Results/' + type_name + '/' + file_name + '.txt'
    f = open(file_path, 'r')
    for line in f:
        array_result.append(line)
    percent = [0 for i in range(len(array_result))]
    packetNo = 0
    for el in array_result:
        packetNo += int(el)
    for i in range(0, len(array_result)):
        percent[i] = round((int(array_result[i]) * 100.0 / packetNo), 2)
    f.close()
    return percent


def read_file_type3(type_name, file_name):
    array_result = []
    file_path = './Results/Traces' + '/' + file_name + '.txt'
    f = open(file_path, 'r')
    for line in f:
        array_result.append(line)
    return array_result


@app.route("/compare", methods=['POST'])
def compare_render():
    type_name = request.form['type_name']
    quic_result, https_result = read_file_comp1(type_name)
    return json.dumps({'quic_packets': quic_result, 'https_packets': https_result})


def read_file_comp1(type_name):
    path = './Results/' + type_name
    dirs = os.listdir( path )
    quic_results = ['QUIC']
    https_results = ['HTTPS']
    for file in dirs:
        array_result = []
        f = open((path + "/" + file), 'r')
        print f
        for line in f:
            if "QUIC" in file:
                quic_results.append(round(float(line),2))
            elif "HTTPS" in file:
                https_results.append(round(float(line),2))
    return quic_results, https_results


# @app.route("/text_visualization",  methods=['GET'])
# def textshow(:
#     x_data1, y_data1, x_data2, y_data2, words = compute_tfidf(readFiles())
#     return json.dumps({'x_data1': x_data1.tolist(), 'y_data1': y_data1.tolist(), 'x_data2': x_data2.tolist(), 'y_data2': y_data2.tolist(), 'words': words})
#
# @app.route("/text")
# def textindex():
#     return render_template("textindex.html")
#
# @app.route("/sampling", methods=['POST'])
# def selectSampling():
#     global dataset, nameOfAttributes, labels, centroids, sampledLabels, sampledData
#     samp = request.form['sampling']
#     vis = request.form['visualization']
#     sampNo = request.form['samplingNo']
#     sampNo = int(sampNo)
#     if(samp == "Adaptive Sampling"):
#         sampledData, sampledLabels = adaptive_sampling(dataset, labels, centroids, sampNo)
#     else:
#         sampledData, sampledLabels = random_sampling(dataset, labels, centroids, sampNo)
#     sampledData_float = []
#     for s1 in sampledData:
#         sampledData_float.append([float(s2) for s2 in s1])
#     sampledData = sampledData_float
#     pcaData, dim1, dim2 = computation(vis)
#     return json.dumps({'pca_data': pcaData.tolist(), 'vis_results': [dim1, dim2], 'sampled_labels': sampledLabels})
#
#
# @app.route("/visualization", methods=['POST'])
# def selectVis():
#     global dataset, nameOfAttributes, labels, centroids, sampledData, sampledLabels
#     vis = request.form['visualization']
#     pcaData, dim1, dim2 = computation(vis)
#     return json.dumps({'pca_data': pcaData.tolist(), 'vis_results': [dim1, dim2], 'sampled_labels': sampledLabels})#, data2=json.dumps(dim1,dim2))
#
# def computation(vis):
#     pcaData = find_intrinsic_dimensionality(sampledData)
#     vis_results = []
#     if(vis == "PCA"):
#         vis_results = my_pca(sampledData)
#     elif(vis == "Euclidian"):
#         vis_results = euclidean_MDS(sampledData)
#     elif(vis == "Cosine"):
#         vis_results = cosine_MDS(sampledData)
#     elif(vis == "Correlation"):
#         vis_results = correlation_MDS(sampledData)
#     elif(vis == "Isomap"):
#         vis_results = isomap(sampledData)
#     dim1, dim2 = split_array(vis_results)
#     return pcaData, dim1, dim2

if __name__ == "__main__":
    app.run(host='localhost',port=5000,debug=True)