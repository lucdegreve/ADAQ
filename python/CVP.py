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

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

#============================

def RepresentsFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


#============================

def analogread_to_temp(ar):

  if int(ar) == 0 : 
    return -273.15
 
  r1 = 10000
  r2 = r1 * (1024.0/float(ar) - 1)
  a = 1.13e-3
  b = 2.34e-4
  c = 8.84e-8
  temp = 1/(a+b*math.log(r2)+c*pow(math.log(r2),3))-273.15
  return temp

#============================

def gettemps(comm):
  t = comm.split(",")
  
  if len(t) == 12:
    temperatures = [float(t[2]), float(t[4]), float(t[6]), float(t[8]), float(t[10])]
    
    return temperatures
  return [0,0,0,0,0]

#============================

def length_to_flow(length):

  if float(length) == 0.0 : return 0

  wavelength = float(length) / 1000000 / 60 # in mu second to minute
  freq = 1.0 / (float(length) / 1000000.0)
  rpm = 1 / (4*wavelength) # 4 pulse per round
  flow = 2850 / 1500 * rpm
  
  return freq


#============================

def getlengths(comm):
  p = comm.split(",")
  if len(p) == 12:
    lengths = [p[3], p[5], p[7], p[9], p[11]]

    if all(RepresentsFloat(item) for item in lengths):

      p3 = float(p[3])
     
      return length_to_flow(p[3]), length_to_flow(p[5]), length_to_flow(p[7]), length_to_flow(p[9]), length_to_flow(p[11])
  return [0,0,0,0,0]



#============================

debug = True
ser = serial.Serial('/dev/arduinoMegaCVP', 9600, timeout=None)


startMarker = 60
endMarker = 62

plt.style.use("seaborn-white")
colors = sns.color_palette("muted")

run = True


csv_t = "../csv/CVP/T" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".csv"
csv_p = "../csv/CVP/P" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".csv"
csv_tall = "../csv/CVP/T_all.csv"
csv_pall = "../csv/CVP/P_all.csv"




# Create the csv file
f_csv_t = open(csv_t, 'w')
wr_t = csv.writer(f_csv_t, quoting=csv.QUOTE_ALL)
wr_t.writerow(["Datetime", "Temp1", "Temp2", "Temp3", "Temp4", "TempExt"])
f_csv_t.close()

f_csv_p = open(csv_p, 'w')
wr_p = csv.writer(f_csv_p, quoting=csv.QUOTE_ALL)
wr_p.writerow(["Datetime", "PC1", "PC2", "PC3", "PC4", "PC5"])
f_csv_p.close()

if not os.path.isfile(csv_tall):
    f_csv_tall = open(csv_tall, 'w')
    wr_tall = csv.writer(f_csv_tall, quoting=csv.QUOTE_ALL)
    wr_tall.writerow(["Datetime", "Temp1", "Temp2", "Temp3", "Temp4", "TempExt"])
    f_csv_tall.close()

if not os.path.isfile(csv_pall):
    f_csv_pall = open(csv_pall, 'w')
    wr_pall = csv.writer(f_csv_pall, quoting=csv.QUOTE_ALL)
    wr_pall.writerow(["Datetime", "PC1", "PC2", "PC3", "PC4", "PC5"])
    f_csv_tall.close()

while run == True :
    tstart = time.time()
    buffer_string = recvFromArduino()
    print('read time:', (time.time()-tstart))
 
    tstart = time.time()
    date = datetime.now()

    temperatures = gettemps(buffer_string)
    lengths = getlengths(buffer_string)

    print(buffer_string)
    print(temperatures, lengths)

    f_csv_t = open(csv_t, 'a')
    wr_t = csv.writer(f_csv_t, quoting=csv.QUOTE_ALL)
    wr_t.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), temperatures[0], temperatures[1], temperatures[2], temperatures[3], temperatures[4]])
    f_csv_t.close()

    f_csv_p = open(csv_t, 'a')
    wr_p = csv.writer(f_csv_p, quoting=csv.QUOTE_ALL)
    wr_p.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), lengths[0], lengths[1], lengths[2], lengths[3], lengths[4]])
    f_csv_p.close()

    f_csv_tall = open(csv_tall, 'a')
    wr_tall = csv.writer(f_csv_tall, quoting=csv.QUOTE_ALL)
    wr_tall.writerow(
      [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), temperatures[0], temperatures[1], temperatures[2], temperatures[3],
       temperatures[4]])
    f_csv_tall.close()

    f_csv_pall = open(csv_pall, 'a')
    wr_pall = csv.writer(f_csv_pall, quoting=csv.QUOTE_ALL)
    wr_pall.writerow(
      [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), lengths[0], lengths[1], lengths[2], lengths[3], lengths[4]])
    f_csv_pall.close()
