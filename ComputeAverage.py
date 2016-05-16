__author__ = 'ghahr'
import os
import csv
import json

type_names = ["Average Packet Size","Average Payload Size","Average Header Size","Number of Packets","Throughput"]

def computeAverage():
    quic_results, HTTP2_results, HTTP1_results = readFiles()
    compAVG(quic_results)
    compAVG(HTTP1_results)
    compAVG(HTTP2_results)
    addToJSON(quic_results,HTTP2_results,HTTP1_results)

def readFiles():
    path = './Results/CSVs/'
    dirs = os.listdir( path )
    quic_results = {"Average Packet Size":0,"Average Payload Size":0,"Average Header Size":0,"Number of Packets":0,"Throughput":0}
    HTTP2_results = {"Average Packet Size":0,"Average Payload Size":0,"Average Header Size":0,"Number of Packets":0,"Throughput":0}
    HTTP1_results = {"Average Packet Size":0,"Average Payload Size":0,"Average Header Size":0,"Number of Packets":0,"Throughput":0}
    for file in dirs:
        with open(path + file) as csvfile:
            reader = csv.DictReader(csvfile)
            row = reader.next()
            for type_name in type_names:
                if "QUIC" in file:
                    quic_results[type_name] += (round(float(row[type_name]),2))
                elif "HTTP2.0" in file:
                    HTTP2_results[type_name] += (round(float(row[type_name]),2))
                elif "HTTP1.1" in file:
                    HTTP1_results[type_name] += (round(float(row[type_name]),2))
    return quic_results, HTTP2_results, HTTP1_results


def compAVG(data):
    for type_name in type_names:
        data[type_name] = data[type_name] / 4
    return data


def addToJSON(quic_results, HTTP2_results, HTTP1_results):
    print "salam"
    data = []
    f = open('./Results/JSONs/AVGResultsJSONFile.json', 'w')
    for type_name in type_names:
        obj = {"chart_title": type_name, "unit": "meter", "HTTP1.1": HTTP1_results[type_name], "HTTP2.0": HTTP2_results[type_name], "QUIC": quic_results[type_name]}
        data.append(obj)
    json.dump(data, f)
    f.close()
    return data

computeAverage()