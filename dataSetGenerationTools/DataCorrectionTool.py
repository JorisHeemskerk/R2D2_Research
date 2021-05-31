import os, shutil
from os import path
import pygame, sys
import time
import numpy as np
from skimage import color as skcolor

##########################################################################################################################
##                                                                                                                      ##
## This tool can be used to correct a dataset.                                                                          ##
## When ran, the terminal will ask you to confirm you want to alter the dataset.                                        ##
## To change the cirlce around the place where the laser should be, use the left mouse button to correct the circle.    ##
## Use the return key to go to the next image when satisfied.                                                           ##
## If the image does not satisfy, use the backspace to remove said image.                                               ##
##                                                                                                                      ##
##########################################################################################################################

# set parameters
display_width = 126
display_height = 126
setName = "whiteLight"

# see if folder exists and ask user if they are sure they want to continue
if path.exists(setName):
    print("This is an existing dataset, are you sure you want to continue? \nEnter Y to continue or N to stop")
    userInput = input()
    if userInput == 'N' or userInput == 'n':
        exit(69)
else:
    print(f"Directory doesnt exist")


# open the corresponding coordList.npy as to read the coordinates
with open(f'{setName}/_coordList.npy', 'rb') as f:
    coordList = np.load(f)

images = np.empty([len(coordList)], dtype="S40")
for i in range(len(coordList)):
    images[i] = f'{setName}/{i}.jpg'

#initialise pygame   
pygame.init()
gameDisplay = pygame.display.set_mode((display_width*2,display_height))
pygame.display.set_caption('Dataset')

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False
i = 0
while not crashed:
    img = pygame.image.load(images[i])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(i)
                if(i < len(coordList)-1):
                    i += 1
                else:
                    crashed = True
            if event.key == pygame.K_BACKSPACE:
                print("You are about to delete a item from the dataset, are you sure? \nEnter Y to continue or N to stop")
                userInput = input()
                if userInput == 'y' or userInput == 'Y':
                    images = np.delete(images, i)
                    coordList = np.delete(coordList, i, axis=0)
                    img = pygame.image.load(images[i])
                    print("The image has been deleted")
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            coordList[i][0], coordList[i][1] = pos[0], pos[1]
        if event.type == pygame.QUIT:
            crashed = True
    gameDisplay.fill(white)
    npImage = pygame.surfarray.array3d(img)
    npImage = skcolor.hsv2rgb(npImage)
    rgbImg = pygame.surfarray.make_surface(255*npImage/npImage.max())
    gameDisplay.blit(rgbImg, (0,0))
    gameDisplay.blit(img, (display_width,0))
    pygame.draw.circle(gameDisplay, (255,255,255), (coordList[i][0],coordList[i][1]), (9), (1))
        
    pygame.display.update()

# if out of the while loop the pygame will terminate
pygame.quit()

print("All items have been corrected, time to save!")

try:
    os.mkdir(f'{setName}_corrected')
except OSError:
    print("Folder already exists, enter Y to continue or N to stop")
    userInput = input()
    if userInput == 'N' or userInput == 'n':
        exit(69)
else:
    folder = f'{setName}_corrected'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print(f"Created directory \'{setName}_corrected\'")

for i in range(len(images)):
    img = pygame.image.load(images[i])
    pygame.image.save(img, f'{setName}_corrected/{i}.jpg')
with open(f'{setName}_corrected/_coordList.npy', 'wb') as f:
    np.save(f, coordList)
