import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

def scatter_graph(data, correctCoords, setname, index):

    plt.title(f'../images/{setname}_corrected/{index}.jpg')

    img = mpimg.imread(f'../images/{setname}_corrected/{index}.jpg')
    plt.imshow(img)

    x, y, t = data.T
    print(t)

    print(f"On average, it takes {round(sum(t)/60, 2)} microseconds (us) to run the algorithm")
 
    plt.scatter(correctCoords[0], correctCoords[1], s=1000, marker='x', c="red")
    plt.scatter(correctCoords[0], correctCoords[1], s=500, marker='o', c="red", alpha=0.1)
    plt.scatter(y,x, s=40 ,marker='^', c="blue", alpha=0.8)
    plt.xlim([0, 126])
    plt.ylim([0, 126])
    plt.gca().invert_yaxis()
    plt.show()
    # create data
    # lis = []
    # for i in range(0, 1000):
    #     lis.append(i)

    # x = lis
    # y = t

    # # plot
    # plt.plot(x,y)
    # plt.gcf().autofmt_xdate()
    # plt.show()