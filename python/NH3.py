#!/usr/bin/python3

import serial
import time
from datetime import datetime
from datetime import timedelta
import struct
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import matplotlib.dates as dates
import numpy as np
import seaborn as sns
import csv
import math

#======================================

def recvFromArduino():
  global startMarker, endMarker
  
  ck = ""
  x = "z" # any value that is not an end- or startMarker
  byteCount = -1 # to allow for the fact that the last increment will be one too many
  
  # wait for the start character
  while  ord(x) != startMarker: 
    x = ser.read()

  # save data until the end marker is found
  while ord(x) != endMarker:
    if ord(x) != startMarker:
      ck = ck + x.decode('utf-8') 
      byteCount += 1
    x = ser.read()
  
  return(ck)


debug = True
ser = serial.Serial('/dev/arduinoMegaNH3S', 9600, timeout=None)


startMarker = 60
endMarker = 62

run = True

# Create the csv file
f_csv = open("../csv/NH3Trap/S" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".csv", 'w')
wr = csv.writer(f_csv, quoting=csv.QUOTE_ALL)
wr.writerow(["Datetime", "DP_T", "DP1", "DP2", "DP3", "DP4", "P_A", "T_T", "T1", "T2", "T3", "T4", "T_A"])

f_csv_daq = open("../monitoring/NH3Trap.csv", 'a')
wr_daq = csv.writer(f_csv_daq, quoting=csv.QUOTE_ALL)

while run == True :
    tstart = time.time()
    buffer_string = recvFromArduino()
    print('read time:', (time.time()-tstart))
    data = buffer_string.split(";")

    print(data)

    wr.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data[11], 
                 data[13], data[15], data[17], data[19], data[21],
                 data[23], data[25], data[27], data[29], data[31], data[33]])


    f_csv_daq = open("../monitoring/NH3Trap.csv", 'a')
    wr_daq = csv.writer(f_csv_daq, quoting=csv.QUOTE_ALL)
    wr_daq.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data[11], 
                 data[13], data[15], data[17], data[19], data[21],
                 data[23], data[25], data[27], data[29], data[31], data[33]])
    f_csv_daq.close()
