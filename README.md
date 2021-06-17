# R2D2 Research
###### *For EN users, the readme is in Dutch for consistency with the paper, but the code should be self-explanatory enough.

###### This GitHub repository contains all the toolings and code required to facilitate our R2D2 research project (Hogeschool Utrecht, 2021).

Deze GitHub repository bevant alle tools en code die horen bij ons R2D2 research project (Hogeschool Utrech, 2021)

# Inhoud

We hebben onze verschillende tools en andere resources in folder structuur ondergebracht. Hieronder is een overzicht te zien, waar in de komende 'hoofdstukken' per onderdeel verder op in gegaan zal worden.


    ├── algorithm                   # Onze algoritmes in c++ en wat simpele testcode
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

# algorithm
    algorithm              
    ├── basicAlgorithm
    └── patchAlgorithm

We hebben twee algoritmes ontworpen, deze zijn in de subfolders te vinden in de vorm van c++ code, met daarbij een kleine test opzet. Dit maakt gebruik van de afbeeldingen, in de vorm van headers, uit de imageConverter.

Het basicAlgorithm is het algoritme wat we daadwerkelijk in onze experimenten hebben gebruikt.
Het patchAlgorithm is een, in theorie, snellere versie die we wegens tijdgebrek niet hebben kunnen gebruiken in onze experimenten.

# algorithmTestingTools
    algorithmTestingTools
    ├── serialFlusher           # Een klein c++ programmatje dat één regel cout, om de serial-logger.py te kunnen stoppen (zie #serial-logger)
    |
    ├── algorithm-tester.hpp    # Dit groepje bestanden is alle code voor 
    ├── crc32.hpp               # het ontvangen van de afbeeldingen via 
    ├── main.cpp                # ons protocol, het uitvoeren van het 
    ├── makefile                # algoritme op deze afbeeldingen en het 
    ├── protocol-tsy.hpp        # cout'en van de resultaten.
    |
    ├── protocol-pi.py          # De code voor het versturen van afbeeldingen vanaf de Raspberry Pi.
    |
    └── serial-logger.py        # Een simpel python programma dat de serial output. 
                                # van de Teensy opslaat naar een text bestand.

Dit zijn de tools die wij gebruikt hebben om onze resultaten te krijgen uit de datasets en het algoritme.
Om ze te gebruiken moet je de Raspberry Pi en Teensy aansluiten zoals in onderstaande tabel. 
Vervolgens kun je onderin protocol-pi.py de directory aanpassen zodat deze naar de correcte dataset wijst.
Daarna open je de serial-logger.py en pas je ook daar de dataset naam aan. 
Dan start je eerst protocol-pi.py, dan serial-logger.py en als laatste run je de makefile ('make run', in de juiste folder (vergeet niet op het knopje op de Teensy te drukken))
Als de protocol-pi.py klaar is, ga je naar serial-logger.py en stop je deze met ctrl+c, echter stop hij dan niet meteen, want hij moet nog één keer iets binnen krijgen op de serial port. Daarom run je de serialFlusher.

Nu kun je de resultaten, op de locatie die je in serial-logger.py hebt aangeven, gebruiken om de resultProcessingTools te runnen.


## Communication Protocol Pin-in/-out
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

# datasetGenerationTools
    datasetGenerationTools
    ├── DataCorrectionTool.py   # Een tool om een dataset te corrigeren.
    ├── DataSetGenerator.py     # Een tool om een dataset mee aan te maken
    └── NpyListReader.py        # Print je .npy bestanden

Om de DataCorrection tool te gebruiken pas je de "setName" variabele aan naar de folder van je dataset. Met je muis kan je de cirkel verplaatsen, met enter ga je naar de volgende afbeelding en met backspace verwijder je de afbeelding. Het resultaat wordt opgeslagen in een [naam van je dataset]_corrected folder.

Om de DataSetGenerator te gebruiken geef je opniew de folder waar je je dataset in wil hebben aan in de "setName" variabele. De grootte van de dataset pas je aan in de setSize variabele. De resolutie is aan te passen met de x- en yTargetRes. Om een foto op te slaan klik je op de window op de plek waar je de laser ziet.

met NpyListReader kan je .npy bestanden die de dataset generator creert uitprinten voor debug purposes. De naam van de dataset waarin het .npy bestand staat stop je opniew in de setName variabele

# datasets
    datasets
    ├── [nameOfDataset]             # Datasets gemaakt met de generator
    └── [nameOfDataset]_corrected   # Datasets gecorrigeerd door de correction tool
Een dataset zelf bestaat uit een lijst aan .jpg bestanden en een _coordList.npy die alle XY-coördinaten per afbeelding bevat.

# imageConverter
    imageConverter
    ├── input            # De input folder voor de converter.
    ├── sample_images    # Een map met voorbeeld afbeeldingen
    ├── converter.py     # Een tool die een afbeelding omzet naar een .hpp bestand.
    └── images.hpp       # Het resultaat van de converter.
De converter pakt alle afbeeldingen uit de input folder (alleen de .jpg en .png bestanden) en zet deze om tot images.hpp. In de .hpp file komen de afbeeldingen samen tot static const std::array<std::array<std::array<std::array<uint8_t, 3>, 126>, 126>, 2> genaamd images. Deze .hpp file kan je gebruiken om een snelle test uit te voeren op de Teensy (of andere microcontroller).
pas de resolutie van de afbeeldingen aan met de x- en yTargetRes variabelen.

# imageConverter
    imageConverter.
    ├── old                      # Een eerdere versie van de tools.
    ├── processResults.py        # Een tool om resultaten te berekenen.
    ├── processingFunctions.py   # De functies voor processingResults.py.
    └── scatterGraph.py          # De img en het resultaat in een grafiek.
De processResults tool kan alle datastes in "setnames" processen en 
Momenteel berekent de processResults de accuracy per dataset en de gemiddelde accuracy voor een gespecificeerde HSV scale value (in te vullen op line 43).

De tool kan ook een scattergraph, op de gemiddelde accuracy (gebaseerd de beste hsv cale value), de beste en slechtste scale combinaties per dataset genereren. Hiervoor dienen een aantal regels uitgecomment te worden.
Om de foutmarge te verkleinen kan je de maxDistance variabele aanpassen (dit is de range rond de correcte XY die toch goedgekeurd wordt.)

# results
    imageConverter.
    └── output[nameOfDataset].txt     # de resultaten
Dit bestand bevat een lijst van alle afbeeldingen. De grans tussen de afbeeldingen wordt aangegeven door middel van de crc code
