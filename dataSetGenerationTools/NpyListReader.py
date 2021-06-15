import numpy as np

setName = "../datasets/r3d_corrected"

with open(f'{setName}/_coordList.npy', 'rb') as f:
    coordList = np.load(f)

for i in range(len(coordList)):
    print(f"{i}: {coordList[i]}")