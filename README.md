# R2D2 Research

This GitHub repository contains all the toolings and code required to facilitate our R2D2 research project (Hogeschool Utrecht, 2021).

## Communication Protocol

The following section lists the pinouts that are used by the simple communication protocol that we've created in order to transfer data from a Raspberry Pi to a Teensy. Our initial approach was aimed at using existing libraries/protocol implementations to accomplish this. Unfortunately, due to some buffering issues with the Broadcom chip that some of the newer Raspberry Pi models are using, we ended up with writing our own implementation.

Name | Teensy | Raspberry Pi
-----|--------|-------------
bit0 | d14 | gpio6
bit1 | d15 | gpio13
bit2 | d16 | gpio19
bit3 | d17 | gpio26
bit4 | d18 | gpio12
bit5 | d19 | gpio16
bit6 | d20 | gpio20
bit7 | d21 | gpio21
||
teensy_ready | d10 | gpio9
pi_ready |  d11 | gpio25
||
start_signal | d8 | gpio11
stop_signal | d9 | gpio8
