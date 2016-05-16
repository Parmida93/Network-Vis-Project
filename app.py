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
import csv
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
    result, result2, result3, result4, x = [], [], [], [], []
    if type_name == "Packet Size" or type_name == "Payload Size" or type_name == "Header Size":
        result1 = read_file_type1(type_name, file_name)
        result = sample_data(result1, sampling_type, samplingNo)
    elif type_name == "Packet Loss Rate":
        result = read_file_type2(type_name, file_name)
    elif type_name == "Trace Table":
        result = read_file_type3(type_name, file_name)
    elif type_name == "Parallel Coordinates":
        result1 = read_file_type3(type_name, file_name)
        result = sample_data(result1, sampling_type,samplingNo)
    elif type_name == "Object Number Through Time":
        result2, result3, result4, x = read_file_type4(type_name, file_name)
    elif type_name == "Load Time CDF":
        result = load_time_cdf(file_name)
    return json.dumps({'all_packets': result, 'HTTP1.1_Packets': result2, 'QUIC_Packets': result3, 'HTTP2.0_Packets': result4, 'x': x})


def sample_data(data, sampling_type, samplingNum):
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
    # file_path = './Results/' + type_name + '/' + file_name + '.txt'
    # f = open(file_path, 'r')
    # for line in f:
    #     array_result.append(float(line))
    # f.close()
    file_path = './Results/CSVs/' + file_name + '.csv'
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            array_result.append(row[type_name])

    return array_result


def read_file_type2(type_name, file_name):
    array_result = []
    file_path = './Results/' + type_name + "/" + file_name + '.txt'
    f = open(file_path, 'r')
    for line in f:
        array_result.append(line)
    percent = [0 for i in range(len(array_result))]
    lossNo = int(array_result[1])
    packetNo = int(array_result[0])
    percent[0] = round(lossNo * 100.0 / packetNo, 2)
    percent[1] = round((packetNo - lossNo) * 100.0 / packetNo, 2)
    f.close()
    return percent


def read_file_type3(type_name, file_name):
    array_result = []
    file_path = './Results/Traces' + '/' + file_name + '.txt'
    print('in file type')
    f = open(file_path, 'r')
    for line in f:
        array_result.append(line)
    return array_result


def read_file_lines(file):
    line = file.readline().split(" ")
    x_array = line
    array_result = file.readline().split(" ")
    return array_result, x_array


def read_file_type4(type_name, file_name):
    print("here")
    file_path_HTTP1 = './Results/' + type_name + '/' + file_name + '_HTTP1.1.txt'
    file_path_HTTP2 = './Results/' + type_name + '/' + file_name + '_HTTP2.0.txt'
    file_path_QUIC = './Results/' + type_name + '/' + file_name + '_QUIC.txt'
    print file_path_HTTP1
    f_HTTP1 = open(file_path_HTTP1, 'r')
    f_HTTP2 = open(file_path_HTTP2, 'r')
    f_QUIC = open(file_path_QUIC, 'r')

    array_result_QUIC, x_array = read_file_lines(f_QUIC)
    array_result_HTTP2, x_array = read_file_lines(f_HTTP2)
    array_result_HTTP1, x_array = read_file_lines(f_HTTP1)

    min_len = min(len(x_array), len(array_result_HTTP2), len(array_result_HTTP1), len(array_result_QUIC))

    f_HTTP1.close()
    f_HTTP2.close()
    f_QUIC.close()

    # print len(x_array), x_array
    # print len(array_result_HTTP1), array_result_HTTP1
    # print len(array_result_HTTP2), array_result_HTTP2
    # print len(array_result_QUIC), array_result_QUIC
    return array_result_HTTP1[:min_len], array_result_QUIC[:min_len], array_result_HTTP2[:min_len], x_array[:min_len]


@app.route("/compare", methods=['POST'])
def compare_render():
    type_name = request.form['type_name']
    quic_result, HTTP1_result, HTTP2_result, totalData = [], [], [], []
    if(type_name == "Total Comparison"):
        totalData = read_file_comp2()
    else:
        quic_result, HTTP2_result, HTTP1_result = read_file_comp1(type_name)
    return json.dumps({'quic_packets': quic_result, 'HTTP2.0_packets': HTTP2_result, 'HTTP1.1_packets': HTTP1_result, 'TotalData': totalData})


def read_file_comp1(type_name):
    path = './Results/CSVs/'
    dirs = os.listdir( path )
    quic_results = ['QUIC']
    HTTP2_results = ['HTTP2.0']
    HTTP1_results = ['HTTP1.1']
    for file in dirs:
        with open(path + file) as csvfile:
            reader = csv.DictReader(csvfile)
            row = reader.next()
            if "QUIC" in file:
                quic_results.append(round(float(row[type_name]),2))
            elif "HTTP2.0" in file:
                HTTP2_results.append(round(float(row[type_name]),2))
            elif "HTTP1.1" in file:
                HTTP1_results.append(round(float(row[type_name]),2))
    return quic_results, HTTP2_results, HTTP1_results


def read_file_comp2():
    path = './Results/JSONs/AVGResultsJSONFile.json'
    with open(path) as data_file:
        data = json.load(data_file)
    print data
    return data

def load_time_cdf(file_name):
    file_path = './Results/Traces' + '/' + file_name + '.txt'
    f = open(file_path, 'r')
    dict = {}
    line = f.readline()
    splitted = line.split(" ")
    receiver = splitted[2]
    sender = splitted[3]
    dict[receiver] = 0
    dict[sender] = 0
    temp_array = [[0, 0]]
    for line in f:
        splitted = line.split(" ")
        if splitted[3] == receiver:
            temp_array.append([splitted[0] , (int(splitted[5]) + temp_array[len(temp_array)-1][1])])
            dict[splitted[3]] += int(splitted[5])
    for i in range(len(temp_array)):
        temp_array[i][1] = temp_array[i][1] * 1.0 / dict[receiver]
    return temp_array


if __name__ == "__main__":
    app.run(host='localhost',port=5001,debug=True)