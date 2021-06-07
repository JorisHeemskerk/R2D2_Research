from gpiozero import InputDevice
from gpiozero import OutputDevice
from skimage import io
# import numpy as np
# import math
import binascii
import time
import os

# run this file with -O to disable debugging
# for example: 'python3 -O b-prot.py'
if __debug__:
    class dbg:
        msg_id = 0

        @staticmethod
        def info(msg, interval=1, wait_ms=0):
            if (dbg.msg_id % interval) == 0:
                print(f'[dbg#{dbg.msg_id}]{msg}')
            time.sleep(wait_ms / 1000)
            dbg.msg_id += 1

# a more specific name for this could useful
class protocol:
    def __init__(self):
        self.setup_pins()
        self.clear_out_pins()

    def setup_pins(self):
        # signal pins
        self.start_signal = InputDevice(11, pull_up=False)
        self.stop_signal  = OutputDevice(8, active_high=True)

        # state pins
        self.tsy_ready = InputDevice(9, pull_up=False)
        self.pi_ready  = OutputDevice(25, active_high=True)

        # data pins
        self.bus = [
            OutputDevice( 6, active_high=True), # bit0
            OutputDevice(13, active_high=True), # bit1
            OutputDevice(19, active_high=True), # bit2
            OutputDevice(26, active_high=True), # bit3
            OutputDevice(12, active_high=True), # bit4
            OutputDevice(16, active_high=True), # bit5
            OutputDevice(20, active_high=True), # bit6
            OutputDevice(21, active_high=True)  # bit7
        ]

    def clear_out_pins(self):
        self.stop_signal.off()
        self.pi_ready.off()
        for bit in self.bus:
            bit.off()

    def send(self, data):
        data = self.insert_checksum(data)
        self.stop_signal.off()
        __debug__ and dbg.info('stop signal off')
        # wait for start signal from Teensy
        while not self.start_signal.is_active:
            __debug__ and dbg.info('start signal off', interval=20, wait_ms=100)
        for byte in data:
            # set data on the bus
            for index, bit in enumerate(self.bus):
                bit.value = (byte >> index) & 0b1
            __debug__ and dbg.info(f'data bus set: {byte:02X}')
            # signal Teensy that we are ready
            self.pi_ready.on()
            __debug__ and dbg.info('pi ready on', wait_ms=1000)
            # wait for Teensy to become ready
            while not self.tsy_ready.is_active:
                __debug__ and dbg.info('teensy ready off', interval=20, wait_ms=100)
            __debug__ and dbg.info('teensy ready on')
            # clear our own ready signal
            self.pi_ready.off()
            __debug__ and dbg.info('pi ready off', wait_ms=1000)
        self.stop_signal.on()
        __debug__ and dbg.info('stop signal on')
        # wait for the start signal to be cleared
        while self.start_signal.is_active:
            __debug__ and dbg.info('start signal on', interval=20, wait_ms=100)
        # return true if Teensy ready is off, else return false
        return not self.tsy_ready.value

    def insert_checksum(self, data):
        checksum = binascii.crc32(data)
        __debug__ and dbg.info(f'generated checksum: {checksum:02X}')
        return binascii.crc32(data).to_bytes(4, byteorder='big') + data


def read_image(filename):
    image = io.imread(filename)
    data = []
    for row in image:
        for pixel in row:
            for part in pixel:
                data.append(part)
    return bytearray(data)


def process_images(directory, comm):
    for filename in os.listdir(directory):
        if filename.endswith('.jpg'):
            data = read_image(directory + filename)
            print(f'processing file: {filename}')
            print(f'  checksum: {"".join(f"{x:02X}" for x in comm.insert_checksum(data)[:4])}')
            print(f'  data sent {"succesfully" if comm.send(data) else "failed"}')


if __name__ == '__main__':
    # data = bytearray([
    #     0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77,
    #     0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF
    # ])
    process_images(r'~/research/dataSetGenerationTools/blackDark_corrected/', protocol())
