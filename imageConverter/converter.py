from skimage import io
from skimage import color
from skimage import transform
from skimage.viewer import ImageViewer
import numpy as np
import os
import math


# This converter enables you to make .hpp files from images,
# making it possible to compile them along with a program.
# we used this before we got the communication between the
# pi and teensy working.


### For usage,
### make an 'input' folder and put some pngs and/or jpgs in there
### then configure the desired resolution below and run the tool
### you'll get an hpp file called images.hpp containing the converted images
### this is a 4D array containing all input images.

def fractionToByte(fraction):
    fraction = max(0.0, min(1.0, fraction))
    return math.floor(255 if fraction == 1.0 else fraction * 256.0)

#change these to affect the resulting resolution
xTargetRes = 126
yTargetRes = 126

imageNames = os.listdir('input')
print(imageNames)
resultingImages = []
for imageName in imageNames:
    if imageName.endswith(".jpg") or imageName.endswith(".png"):
        image = np.empty(1)

        if imageName.endswith(".jpg"):
            filename = os.path.join('input/' + imageName)
            image = io.imread(filename)

            image = color.rgb2hsv(image)
        if imageName.endswith(".png"):
            filename = os.path.join('input/' + imageName)
            image = io.imread(filename)

            image = color.rgba2rgb(image)
            image = color.rgb2hsv(image)
        
        if len(image) < len(image[0]): #for images wider than they are high
            image = transform.resize(image, (yTargetRes, int( (yTargetRes / len(image)) * len(image[0])) ), anti_aliasing = True)

            image = image[0 : yTargetRes+1, (len(image[0])-xTargetRes)//2 : ((len(image[0])-xTargetRes)//2)+xTargetRes]

        if len(image) > len(image[0]): #for images higher than they are wide
            image = transform.resize(image, ( int( (xTargetRes / len(image[0])) * len(image)), xTargetRes ), anti_aliasing = True)

            image = image[(len(image)-yTargetRes)//2 : ((len(image)-yTargetRes)//2)+yTargetRes, 0 : xTargetRes]

        resultingImages.append(image)

        pog = image
        #pog = color.hsv2rgb(image)
        viewer = ImageViewer(pog)
        viewer.show()
        
f = open('images.hpp', 'w')

f.write(f'#ifndef IMAGES_HPP__\n#define IMAGES_HPP__\n\n#include <array>\n\nstatic const std::array<std::array<std::array<std::array<uint8_t, {len(resultingImages[0][0][0])}>, {xTargetRes}>, {yTargetRes}>, {len(resultingImages)}> images{{{{')

for image in resultingImages:
    f.write('\n{{')
    for row in image:
        f.write('\n{{')
        for pixel in row:
            f.write(f'{{{{{fractionToByte(pixel[0])}, {fractionToByte(pixel[1])}, {fractionToByte(pixel[2])}}}}},')
        f.write('}},')
    f.write('}},')

f.write('}};\n\n#endif //IMAGES_HPP__\n')
f.close()
