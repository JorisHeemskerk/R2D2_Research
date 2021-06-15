import numpy as np
from matplotlib import pyplot as plt
import os
import binascii
from skimage import io
import math

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
                distance = math.sqrt((laserLocation[1] - guesses[(h*100)+(s*10)+v][0])**2 + (laserLocation[1] - guesses[(h*100)+(s*10)+v][1])**2)
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

def get_accuracy(resultsDict, checksums, coordList, h, s, v, maxDistance):
    '''Returns the accuracy as fraction, vor H, S and V multipliers h,s,v. A guess is counted as "correct" when the distance from the correct answer is less than maxDistance'''
    nCorrectGuesses = 0
    for i in range(len(coordList)):
        data = np.array(resultsDict[checksums[i]])
        distance = math.sqrt((coordList[i][1] - data[(h*100)+(s*10)+v][0])**2 + (coordList[i][0] - data[(h*100)+(s*10)+v][1])**2)
        if distance < maxDistance:
            nCorrectGuesses += 1
    return nCorrectGuesses / len(coordList)

def accuracy_based_find_best_and_worst_hsv_scales(resultsDict, checksums, coordList, maxDistance, scaleStart=0, scaleEnd=10):
    best = (0,0,0,-1)
    worst = (0,0,0,float('inf'))
    for h in range(scaleStart, scaleEnd):
        for s in range(scaleStart, scaleEnd):
            for v in range(scaleStart, scaleEnd):
                acc = get_accuracy(resultsDict, checksums, coordList, h,s,v, maxDistance)
                if acc > best[3]:
                    best = (h,s,v,acc)
                elif acc < worst[3]: #Using elif here should make it impossible for the worst to have h,s,v == 0,0,0
                    worst = (h,s,v,acc)
    return best, worst

def get_all_accuracies(resultsDict, checksums, coordList, maxDistance, scaleStart=0, scaleEnd=10):
    accuracies = []
    for h in range(scaleStart, scaleEnd):
        for s in range(scaleStart, scaleEnd):
            for v in range(scaleStart, scaleEnd):
                accuracies.append(get_accuracy(resultsDict, checksums, coordList, h,s,v, maxDistance)) 
    return accuracies

def find_best_from_accuracies(accuracies, scaleStart=0, scaleEnd=10):
    best = (0,0,0,-1)
    for h in range(scaleStart, scaleEnd):
        for s in range(scaleStart, scaleEnd):
            for v in range(scaleStart, scaleEnd):
                totAcc = 0
                for dataSet in accuracies:
                    totAcc += dataSet[(h*100)+(s*10)+v]
                if (totAcc/len(accuracies)) > best[3]:
                    best = (h,s,v,totAcc/len(accuracies))
    return best