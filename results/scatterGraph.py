import numpy as np
from matplotlib import pyplot as plt

setName = "../dataSetGenerationTools/blackDark"
index = 6

with open(f'{setName}/_coordList.npy', 'rb') as f:
    coordList = np.load(f)

data = np.array([
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 347],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 347],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 347],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 347],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 347],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 347],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 347],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[52, 77, 346],
[53, 73, 347],
[53, 73, 346],
[53, 73, 346],
[53, 73, 346],
[53, 73, 346],
[53, 73, 347],
[53, 73, 346],
[53, 73, 346],
[53, 73, 346],
[53, 73, 346],
])

x, y, z = data.T
split_X = np.array_split(x, 3)
split_Y = np.array_split(y, 3)

print(f"On average, it takes {round(sum(z)/60, 2)} microseconds (us) to run the algorithm")
print("The blue values alter in the H spectrum (with sScale=1 and vScale=1)")
print("The green values alter in the s spectrum (with hScale=1 and vScale=1)")
print("The yellow values alter in the v spectrum (with sScale=1 and hScale=1)")
plt.scatter(coordList[index][0], coordList[index][1], s=1000, marker='x', c="red")
plt.scatter(coordList[index][0], coordList[index][1], s=500, marker='o', c="red", alpha=0.1)
plt.scatter(split_X[0],split_Y[0], s=40 ,marker='^', c="blue", alpha=0.8)
plt.scatter(split_X[1],split_Y[1], s=30, marker='P', c="green", alpha=0.5)
plt.scatter(split_X[2],split_Y[2], s=10, marker='o', c="yellow", alpha=0.5)
plt.xlim([0, 126])
plt.ylim([0, 126])
plt.gca().invert_yaxis()
plt.show()




