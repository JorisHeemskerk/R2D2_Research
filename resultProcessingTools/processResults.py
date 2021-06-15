import numpy as np
from matplotlib import pyplot as plt
import os
import binascii
from skimage import io
import math

from scatterGraph import scatter_graph
from processingFunctions import load_checksums_from_images, load_results_dict, find_avg_best_and_worst_hsv_scales, get_accuracy, accuracy_based_find_best_and_worst_hsv_scales

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

    #scatter_graph(data, coordList[index], setName, index)

    #bestHSV, worstHSV = find_avg_best_and_worst_hsv_scales(resultsDict, checksums, coordList)
    #print(f'For {setName} the best HSV values are {bestHSV} and the worst HSV values are {worstHSV}')

    #h,s,v = 1, 1, 1
    maxDistance = 20
    #print(f'Accuracy on the {setName} dataset with HSV multipliers ({h}, {s}, {v}) and maxDistance {maxDistance} is {round(get_accuracy(resultsDict, checksums, coordList, h, s, v, maxDistance) * 100, 1)}%.')

    best, worst = accuracy_based_find_best_and_worst_hsv_scales(resultsDict, checksums, coordList, maxDistance)
    print(f'For {setName} the best HSV values are {best[:3]} with an accuracy of {round(best[3] * 100, 1)}% and the worst HSV values are {worst[:3]} with an accuracy of {round(worst[3] * 100, 1)}%.')