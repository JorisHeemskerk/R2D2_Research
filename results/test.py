import numpy as np
from matplotlib import pyplot as plt
import math

from numpy.lib import average

def averageHSV(bestHsvData):
    H, S, V = 0, 0, 0
    for data in bestHsvData:
        H += data[0]
        S += data[1]
        V += data[2]
    return H/len(bestHsvData), S/len(bestHsvData), V/len(bestHsvData)


setName = "../dataSetGenerationTools/blackDark"
txtFile = "test.txt"

with open (txtFile, "r") as myfile:
    lines = myfile.read().splitlines()

with open(f'{setName}/_coordList.npy', 'rb') as f:
    coordList = np.load(f)

image = 0
# allData = np.empty(shape=[0, 0, 3])
allData = []
data = np.empty(shape=[0, 3])
for i in range(len(lines)):
    if lines[i].find(".jpg") != -1:
        image += 1
        # allData = np.append(allData, data, axis=0)
        allData.append(data)
        data = np.empty(shape=[0, 3])
    else:
        lines[i] = lines[i][1:-2] 
        lines[i] = lines[i].split(", ")
        line = [int(numeric_string) for numeric_string in lines[i]]
        data = np.append(data, [line], axis=0)
# print(type(allData[0]))
allData.pop(0)
# print(len(allData))

totalRuntime_us = 0
bestHsvData = []
for i, data in enumerate(allData):
    laserLocation = coordList[i]
    x, y, z = data.T
    totalRuntime_us += sum(z)

    # find best individual H, S and V
    closestH = float('inf') 
    closestS = float('inf') 
    closestV = float('inf') 
    bestH = -1
    bestS = -1
    bestV = -1
    for j, guess in enumerate(data):
        distance = math.sqrt((laserLocation[0] - guess[0])**2 + (laserLocation[1] - guess[1])**2)
        if j < 20:
            # print(f"H value is: {j}")
            if distance < closestH:
                closestH = distance
                bestH = j
                continue
        elif j < 40:
            # print(f"S value is: {j-20}")
            if distance < closestS:
                closestS = distance
                bestS = j-20
                continue
        elif j < 60:
            # print(f"V value is: {j-40}")
            if distance < closestV:
                closestV = distance
                bestV = j-40
                continue
        else:
            print("help")
    bestHsvData.append([bestH, bestS, bestV])
    # print(f"for the {i+1}th image the best H, S and V values are ({bestH}, {bestS}, {bestV}) with these distances:({closestH}, {closestS}, {closestV}) ")

H, S, V = averageHSV(bestHsvData)
print(f"These are the best HSV averages: ({H}, {S}, {V})")
print(f"On average, it takes {round(totalRuntime_us/(len(allData)*len(allData[0])), 2)} microseconds (us) to run the algorithm")