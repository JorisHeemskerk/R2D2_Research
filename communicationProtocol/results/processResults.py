import numpy as np
from matplotlib import pyplot as plt
import os
import binascii
from skimage import io

from scatterGraph import scatter_graph

def read_image(filename):
    #filename = os.path.join(filename)
    #print(filename)
    image = io.imread(filename)
    data = []
    for row in image:
        for pixel in row:
            for part in pixel:
                data.append(part)
    return bytearray(data)


def load_checksums_from_images(directory):
    """Returns list of checksums with indexes equal to the numeric part of their name. 
    I.E. the checksum of 23.jpg will end up on index 23 of the returned list"""
    filenames = os.listdir(directory)
    checksums = [None]*len(filenames)
    for filename in filenames:
        if filename.endswith('.jpg'):
            data = read_image(directory + filename)
            checksums[int(filename[:-4])] = binascii.crc32(data)
            #print(f'checksums[{int(filename[:-4])}] = {hex(checksums[int(filename[:-4])])} with filename = {filename}')
    return checksums

def load_results_dict(filename):
    bigArr = []

    resultsDict = {}

    prevChecksum = 0

    f = open(filename, "r")
    for line in f:
        if(line[0] != '['):
            line = line.strip('\n')
            resultsDict[prevChecksum] = bigArr
            prevChecksum = int(line,16)
            bigArr = []
        else:
            tempArr = []
            tempNum = ""
            line = line.strip('\n,, ')
            for char in line:
                
                if(char >= '0' and char <= '9'):
                    tempNum += char
                elif(char == ','):
                    tempArr.append(int(tempNum))
                    tempNum = ""
                elif(char == ']'):
                    tempArr.append(int(tempNum))
                    bigArr.append(tempArr)
                    tempNum = ""
                    tempArr = []
                
    #for key, value in resultsDict.items() :
    #    print(key)
    return resultsDict

for i in range(130):
    setName = 'blackDark_corrected'
    index = i

    print('Loading checksums')
    checksums = load_checksums_from_images(f'images/{setName}/')
    print('Finished loading checksums')

    print('Loading coordlist')
    with open(f'images/{setName}/_coordList.npy', 'rb') as f:
        coordList = np.load(f)
    print('Finished loading coordlist')

    print('Loading results')
    resultsDict = load_results_dict(f'output/output_{setName}.txt')
    print('Finished loading results')

    print('Processing results')
    data = np.array(resultsDict[checksums[index]])

    scatter_graph(data, coordList[index])