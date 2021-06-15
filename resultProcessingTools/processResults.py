import numpy as np
from matplotlib import pyplot as plt
import os
import binascii
from skimage import io
import math

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
    resultsDict[prevChecksum] = bigArr
                
    #for key, value in resultsDict.items() :
    #    print(key)
    return resultsDict

def averageHSV(hsvData):
    H, S, V = 0, 0, 0
    for data in hsvData:
        H += data[0]
        S += data[1]
        V += data[2]
    return (H/len(hsvData), S/len(hsvData), V/len(hsvData))

def find_best_and_worst_hsv_scales(guesses, laserLocation, scaleStart=0, scaleEnd=10):
    #a tuple containing (Hscale, Sscale, Vscale, distance)
    best = (0,0,0,float('inf'))
    worst = (0,0,0,-1)

    #The testing code runs three for loops (one inside the other, etc.) Going through all combinations of H, S and V scales, so we do the same thing here.
    for h in range(scaleStart, scaleEnd):
        for s in range(scaleStart, scaleEnd):
            for v in range(scaleStart, scaleEnd):
                distance = math.sqrt((laserLocation[0] - guesses[(h*100)+(s*10)+v][0])**2 + (laserLocation[1] - guesses[(h*100)+(s*10)+v][1])**2)
                if distance < best[3]:
                    best = (h,s,v,distance)
                if distance > worst[3]:
                    worst = (h,s,v,distance)
    return best, worst

def find_avg_best_and_worst_hsv_scales(resultsDict, checksums, coordList):
    best_values = []
    worst_values = []
    for i in range(len(coordList)):
        data = np.array(resultsDict[checksums[i]])
        best, worst = find_best_and_worst_hsv_scales(data, coordList[i])
        best_values.append(best)
        worst_values.append(worst)
    avg_best = averageHSV(best_values)
    avg_worst = averageHSV(worst_values)
    return avg_best, avg_worst


# These setnames are assumed to reference the corrected variants, 
# make sure to run dataSetGenerationTools/DataCorrectionTool.py on any new datasets! 
# (in order to correct them, or just change the name ¯\_(ツ)_/¯)
setNames = ['blackDark', 'blackLight', 'greyDark', 'greyLight', 'whiteDark', 'whiteLight', 'mirror', 'r3d']
dbg = False
for setName in setNames:
    index = 0

    if dbg: print('Loading checksums')
    checksums = load_checksums_from_images(f'../datasets/{setName}_corrected/')
    if dbg: print('Finished loading checksums')

    if dbg: print('Loading coordlist')
    with open(f'../datasets/{setName}_corrected/_coordList.npy', 'rb') as f:
        coordList = np.load(f)
    if dbg: print('Finished loading coordlist')

    if dbg: print('Loading results')
    resultsDict = load_results_dict(f'../results/output_{setName}_corrected.txt')
    if dbg: print('Finished loading results')

    if dbg: print('Processing results')
    data = np.array(resultsDict[checksums[index]])

    #scatter_graph(data, coordList[index])

    bestHSV, worstHSV = find_avg_best_and_worst_hsv_scales(resultsDict, checksums, coordList)
    print(f'For {setName} the best HSV values are {bestHSV} and the worst HSV values are {worstHSV}')

