import os
from os import path
import pygame, sys
import time
import numpy as np

def reorderImages(directory):
    i = 0
    for filename in os.listdir(directory):
        print(filename)
        if filename.endswith(".jpg"):
            os.rename(filename, f'{i}.jpg')
            i += 1


# set parameters
display_width = 126
display_height = 126
setName = "whiteDark"

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

#initialise pygame   
pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A bit Racey')

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
crashed = False
i = 1
while not crashed:
    img = pygame.image.load(f'{setName}/{i}.jpg')
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
                    os.remove(f'{setName}/{i}.jpg')
                    img = pygame.image.load(f'{setName}/5.jpg')
                    reorderImages(setName)
                    print()
                    
            
        if event.type == pygame.QUIT:
            crashed = True
    gameDisplay.fill(white)
    gameDisplay.blit(img, (0,0))
    pygame.draw.circle(gameDisplay, (255,255,255), (coordList[i][0],coordList[i][1]), (9), (1))
        
    pygame.display.update()




pygame.quit()
quit()