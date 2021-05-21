import os
import pygame, sys
import time
import numpy as np
 
from pygame.locals import *
import pygame.camera
 
setName = "prototype"
setSize = 10
windowWidth = 640
windowHeight = 480
 
try:
    os.mkdir(setName)
except OSError:
    print("Folder already exists, enter Y to continue or N to stop")
    userInput = input()
    if userInput == 'N' or userInput == 'n':
        exit(69)
else:
    print(f"Created directory '{setName}'")
 
#initialise pygame   
pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(windowWidth,windowHeight))
cam.start()
 
#setup window
windowSurfaceObj = pygame.display.set_mode((windowWidth,windowHeight),1,16)
pygame.display.set_caption('Camera')
 
coords = np.empty((setSize, 2))
counter = 0
while counter < setSize:
    #take a image
    image = cam.get_image()

    #convert image
    #soon TM

    #display the image
    catSurfaceObj = image
    windowSurfaceObj.blit(catSurfaceObj,(0,0))
    pygame.display.update()
    
    pygame.event.get()
    pygame.display.update()
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        #save image
        pygame.image.save(windowSurfaceObj, f'{setName}/{counter}.jpg')
        coords[counter][0], coords[counter][1] = pos[0], pos[1]
        counter += 1
        time.sleep(1)
with open(f'{setName}/_coordList.npy', 'wb') as f:
    np.save(f, coords)
exit(0)