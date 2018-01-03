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
import CellMonitoring
import os.path

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


#============================

def waitForArduino(state = "Ready"):

   # wait until the Arduino sends 'Ready' - allows time for Arduino reset
   # it also ensures that any bytes left over from a previous message are discarded
   
    global startMarker, endMarker
    
    msg = ""
    while msg.find(state) == -1:

        while ser.inWaiting() == 0:
            pass
        
        msg = recvFromArduino()

      # print(msg)
      # print

#============================

def RepresentsFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


#============================

def gettemps(comm):
    t = comm.split(",")

    if len(t) == 5:
        
        if all(RepresentsFloat(item) for item in t) and (float(t[3]) > -10 and float(t[3]) < 80 and float(t[4]) < 5) :
            return int(t[0]), int(t[1]), int(t[2]), float(t[3]), float(t[4])
        else :
            print("WARNING! time:", datetime.now(), " D", t[1], " S", t[2], " T:", t[3], "+-", t[4] )
    return [0, 0, 0, 0, 0]

#============================

debug = True
ser = serial.Serial('/dev/arduinoMegaT', 9600, timeout=None)

ncell = 8
startMarker = 60
endMarker = 62


run = True

# Create the csv file
for cell_id in range(1, 9):
    if not os.path.isfile("../csv/Temps/cell_" + str(cell_id) + ".csv"):
        f_csv = open("../csv/Temps/cell_"+str(cell_id)+".csv", 'w')
        wr = csv.writer(f_csv, quoting=csv.QUOTE_ALL)
        wr.writerow(["Datetime", "probe", "T", "Err"])
        f_csv.close()



while run == True :
    tstart = time.time()
    buffer_string = recvFromArduino()
    print('read time:', (time.time()-tstart))
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    millis, cell_id, probe_id, t, err = gettemps(buffer_string)
    if millis != 0:
      f_csv = open("../csv/Temps/cell_" + str(cell_id+1) + ".csv", 'a')
      wr = csv.writer(f_csv, quoting=csv.QUOTE_ALL)
      wr.writerow([date, probe_id+1, t, err])
      f_csv.close()

  


