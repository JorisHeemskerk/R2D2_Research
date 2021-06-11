import numpy as np
from matplotlib import pyplot as plt

def scatter_graph(data, correctCoords):

    x, y, t = data.T

    print(f"On average, it takes {round(sum(t)/60, 2)} microseconds (us) to run the algorithm")
 
    plt.scatter(correctCoords[0], correctCoords[1], s=1000, marker='x', c="red")
    plt.scatter(correctCoords[0], correctCoords[1], s=500, marker='o', c="red", alpha=0.1)
    plt.scatter(y,x, s=40 ,marker='^', c="blue", alpha=0.8)
    plt.xlim([0, 126])
    plt.ylim([0, 126])
    plt.gca().invert_yaxis()
    plt.show()
