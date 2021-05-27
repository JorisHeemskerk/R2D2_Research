import os
import pygame, sys
import time
import numpy as np
from skimage import color as skcolor
from skimage import transform
#import math

from pygame.locals import *
import pygame.camera

#change these to affect the resulting resolution
xTargetRes = 126
yTargetRes = 126

setName = "r3d"
setSize = 30

try:
    os.mkdir(setName)
except OSError:
    print("Folder already exists, enter Y to continue or N to stop")
    userInput = input()
    if userInput == 'N' or userInput == 'n':
        exit(69)
else:
    print(f"Created directory '{setName}'")

#def fractionToByte(fraction):
#    fraction = max(0.0, min(1.0, fraction))
#    return math.floor(255 if fraction == 1.0 else fraction * 256.0)

#initialise pygame   
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(xTargetRes,yTargetRes))
cam.start()
 
#setup window
windowSurfaceObj = pygame.display.set_mode((xTargetRes,yTargetRes),1,16)
pygame.display.set_caption('Camera')

coords = np.empty((setSize, 2))
counter = 0
loopCount = 0
image = cam.get_image()
while counter < setSize:
    if loopCount >= 25:
        #take a image
        image = cam.get_image()
        loopCount = 0
    loopCount += 1

    #convert image
    npImage = pygame.surfarray.array3d(image)
    
    if len(npImage) < len(npImage[0]): #for images wider than they are high
        npImage = transform.resize(npImage, (yTargetRes, int( (yTargetRes / len(npImage)) * len(npImage[0])) ), anti_aliasing = True)

        npImage = npImage[0 : yTargetRes+1, (len(npImage[0])-xTargetRes)//2 : ((len(npImage[0])-xTargetRes)//2)+xTargetRes]

    elif len(npImage) > len(npImage[0]): #for images higher than they are wide
        npImage = transform.resize(npImage, ( int( (xTargetRes / len(npImage[0])) * len(npImage)), xTargetRes ), anti_aliasing = True)

        npImage = npImage[(len(npImage)-yTargetRes)//2 : ((len(npImage)-yTargetRes)//2)+yTargetRes, 0 : xTargetRes]
    
    #display the image
        
    catSurfaceObj = pygame.surfarray.make_surface(255*npImage/npImage.max())
    windowSurfaceObj.blit(catSurfaceObj,(0,0))
    pygame.display.update()
    
    pygame.event.get()
    pygame.display.update()
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        #save image
        npImage = skcolor.rgb2hsv(npImage)
        catSurfaceObj = pygame.surfarray.make_surface(255*npImage/npImage.max())
        windowSurfaceObj.blit(catSurfaceObj,(0,0))
        pygame.image.save(windowSurfaceObj, f'{setName}/{counter}.jpg')
        coords[counter][0], coords[counter][1] = pos[0], pos[1]
        print(counter)
        counter += 1
        time.sleep(1)
with open(f'{setName}/_coordList.npy', 'wb') as f:
    np.save(f, coords)
exit(0)
