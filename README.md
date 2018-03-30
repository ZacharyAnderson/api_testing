# api_testing
Used for the testing of 3par/XtremIO/Vplex/Brocade API integration


## config.ini
You will need to create a config.ini file that includes:
```
[HPE_3PAR]
HPE_USERNAME = USERNAME
HPE_PASSWORD = PASSWORD

[EMC_VPLEX]
VPLEX_USERNAME = USERNAME
VPLEX_PASSWORD = PASSWORD
```

## API_menu.py
When executing API_menu.py you will be greeted with a screen that allows you to log in to any 3Par array:
```
Welcome Storage Administrator, 

Please select the Storage Array you would like to work on: 

1. ESGMID3PAR7400C1

2. ESGLYN3PAR7400C1

3. ESGLYN3PAR-25K8

4. ESGMID3PAR-22WT

5. ESGNET3PAR7400C

6. ESGPL3PAR20K1

7. ESGPM3PAR20K1

0. Quit
```

Once you enter an array you will have the ability to choose a few actions:
```
You made it into: ESGPL3PAR20K1!

We have the ability to complete basic storage administration tasks through the HPE 3PAR WSAPI.

You have now successfully logged into the 3PAR.

Select the task you would like to complete:

1. Create Virtual Volume Set

2. Create Virtual Volumes

3. Query VV/Vlun information

4. Query VVset names

5. Query CPG names

9. Exit
```

An example of the Quer VV/Vlun information action:
```
Please enter the base volume you want to query:
 >> PIWDI
PIWDI1_1                         60002AC0000000000000081000019287
PIWDI1_2                         60002AC0000000000000081100019287
PIWDI1_3                         60002AC0000000000000081200019287
PIWDI1_4                         60002AC0000000000000081300019287
PIWDI1_5                         60002AC0000000000000081400019287
PIWDI1_6                         60002AC0000000000000081500019287
PIWDI1_7                         60002AC0000000000000081600019287
PIWDI1_8                         60002AC0000000000000081700019287
PIWDI1_9                         60002AC0000000000000081800019287
PIWDI1_10                        60002AC0000000000000081900019287
PIWDI1_11                        60002AC0000000000000081A00019287
PIWDI1_12                        60002AC0000000000000081B00019287
PIWDI1_13                        60002AC0000000000000081C00019287
PIWDI1_14                        60002AC0000000000000081D00019287
PIWDI1_15                        60002AC0000000000000081E00019287
PIWDI1_16                        60002AC0000000000000081F00019287
Select the task you would like to complete:
```


## HPE3Par_device_removal.py
Start with device WWN's in a file called "3ParWWNlist.txt" i.e.:
```
60002ac000000000010016380001246b
60002ac000000000010016390001246b
60002ac0000000000100163a0001246b
60002ac0000000000100163b0001246b
60002ac0000000000100163c0001246b
60002ac0000000000100163d0001246b
60002ac0000000000100163e0001246b
60002ac0000000000100163f0001246b
60002ac000000000010016400001246b
60002ac000000000010016410001246b
60002ac000000000010016420001246b
60002ac000000000010016430001246b
60002ac000000000010016440001246b
60002ac000000000010016450001246b
```
This application will automatically unexport the lun, remove from a volume set, and delete the volume.
