from gpiozero import InputDevice
from gpiozero import OutputDevice
import time
from skimage import io
import numpy as np
import os
import math

def fractionToByte(fraction):
    fraction = max(0.0, min(1.0, fraction))
    return math.floor(255 if fraction == 1.0 else fraction * 256.0)

transactionStart = InputDevice(11, pull_up=False)#Invert for active high or active low (for all below too)
transactionStop = OutputDevice(8, active_high=True)

teensyReady = InputDevice(9, pull_up=False)
piReady = OutputDevice(25, active_high=True)

bit0 = OutputDevice(6, active_high=True)
bit1 = OutputDevice(13, active_high=True)
bit2 = OutputDevice(19, active_high=True)
bit3 = OutputDevice(26, active_high=True)
bit4 = OutputDevice(12, active_high=True)
bit5 = OutputDevice(16, active_high=True)
bit6 = OutputDevice(20, active_high=True)
bit7 = OutputDevice(21, active_high=True)
dataBus = [bit0, bit1, bit2, bit3, bit4, bit5, bit6, bit7]

def turnOffOutPins():
    transactionStop.off()
    piReady.off()
    bit0.off()
    bit1.off()
    bit2.off()
    bit3.off()
    bit4.off()
    bit5.off()
    bit6.off()
    bit7.off()

def sendData(data): #Data should be a 2D array of shape (dataAmount, len(dataBus)), containing only Bools
    turnOffOutPins()
    while(not transactionStart.is_active):
        #print("Waiting for start.")
        pass
    for i in range(len(data)):
        #print(data[i])
        for j in range(len(dataBus)):
            shifted = data[i] >> j
            dataBus[j].value = 0b1 & shifted
        #print("Data set")
        piReady.on()
        #time.sleep(2)
        #print("Pi ready")
        while(not teensyReady.is_active): #and not transactionStart.is_active):
            #print("Teensy not ready")
            pass
        if(teensyReady.is_active):
            piReady.off()
            #print("Pi not ready")
        #elif(transactionStart.is_active):
        #    turnOffOutPins()
        #    return False
    transactionStop.on()
    turnOffOutPins()
    return True

data = []

filename = os.path.join("images/blackDark_corrected/" + "0" + ".jpg")
image = io.imread(filename)

for row in image:
    for pixel in row:
        for part in pixel:
            data.append(part)

#data = [0x00,0x11,0x22,0x33,0x44,0x55,0x66,0x77,0x88,0x99,0xAA,0xBB,0xCC,0xDD,0xEE,0xFF]

print("sendData return: ", end='')
print(sendData(data))