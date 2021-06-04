from gpiozero import InputDevice
from gpiozero import OutputDevice

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

def sendData(data): #Data should be a 2D array of shape (dataAmount, len(dataBus)), containing only Bools
    transactionStop.off()#Just to be sure
    while(not transactionStart.is_active):
        pass
    for i in range(len(data)):
        for j in range(len(dataBus)):
            dataBus[j].value = data[i][j]
        piReady.on()
        while(not teensyReady.is_active and not transactionStart.is_active):
            pass
        if(teensyReady.is_active):
            piReady.off()
        elif(transactionStart.is_active):
            return False
    transactionStop.on()
    return True

data = [[0,0,0,0,0,0,0,0],[0,0,0,0,1,1,1,1],[1,1,1,1,1,1,1,1,]]

print(sendData(data))