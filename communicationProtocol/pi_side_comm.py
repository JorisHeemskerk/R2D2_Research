from gpiozero import InputDevice
from gpiozero import OutputDevice
import time

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
dataBus = [bit7, bit6, bit5, bit4, bit3, bit2, bit1, bit0]

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
        print("Waiting for start.")
        pass
    for i in range(len(data)):
        for j in range(len(dataBus)):
            dataBus[j].value = data[i][j]
        print("Data set")
        piReady.on()
        #time.sleep(2)
        print("Pi ready")
        while(not teensyReady.is_active): #and not transactionStart.is_active):
            print("Teensy not ready")
            pass
        if(teensyReady.is_active):
            piReady.off()
            print("Pi not ready")
        #elif(transactionStart.is_active):
        #    turnOffOutPins()
        #    return False
    transactionStop.on()
    turnOffOutPins()
    return True

data = [[0,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,1],[1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,1],[1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,1],[1,1,1,1,1,1,1,1]]

print("sendData return: ", end='')
print(sendData(data))