# R2D2 Research

###### *For EN users, the readme is in Dutch for consistency with the paper, but the code should be self-explanatory enough.

###### This GitHub repository contains all the toolings and code required to facilitate our R2D2 research project (Hogeschool Utrecht, 2021).

Deze GitHub repository bevant alle tools en code die horen bij ons R2D2 research project (Hogeschool Utrech, 2021)

# Inhoud

We hebben onze verschillende tools en andere resources in folder structuur ondergebracht. Hieronder is een overzicht te zien, waar in de komende 'hoofdstukken' per onderdeel verder op in gegaan zal worden.

    .
    ├── algorithm                   # Onze algoritmen in c++ en wat simpele testcode
    |                               
    ├── algorithmTestingTools       # Alle tools die nodig zijn om afbeeldingen van 
    |                               # de Pi naar de Teensy te sturen, deze door het algoritme te 
    |                               # halen en de resultaten naar een text bestand op te slaan.
    |                               
    ├── datasetGenerationTools      # De tools om nieuwe datasets te maken en deze te corrigeren.
    |                               
    ├── datasets                    # De datasets die wij gemaakt hebben.
    |                                
    ├── imageConverter              # Een converter die afbeelding naar het HSV spectrum en de
    |                               # juiste afmetingen vertaald en deze vervolgens in een
    |                               # compileerbare header file zet.
    |                                
    ├── resultProcessingTools       # De tools om de resultaten van algorithmTestingTools te
    |                               # verwerken tot bruikbare dingen, zoals een accuracy 
    |                               # percentage of scatter graph.
    |                                
    ├── results                     # De resultaten van het uitvoeren van de tools in
    |                               # algorithmTestingTools.
    |                                
    ├── .gitignore                   
    ├── makefile.link               # Een bestand voor c++ compilatie met de hwlib/bmptk suite (github.com/wovo)
    └── README.md                   # Dit bestand.



## Communication Protocol

The following section lists the pinouts that are used by the simple communication protocol that we've created in order to transfer data from a Raspberry Pi to a Teensy. Our initial approach was aimed at using existing libraries/protocol implementations to accomplish this. Unfortunately, due to some buffering issues with the Broadcom chip that some of the newer Raspberry Pi models use, we had to resort to writing our own communication protocol.

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
