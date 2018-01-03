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

plt.style.use('seaborn-white')
colors = sns.color_palette("muted")

run = False

# Create the csv file
f_csv = open(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".csv", 'w')
wr = csv.writer(f_csv, quoting=csv.QUOTE_ALL)

# Create the matplotlib window
plt.ion() # set plot to animated
fig = plt.figure()

cellarray = []
for i in range(ncell):
  if i == 7 : newcell = CellMonitoring.CellMonitoring(fig,i+1,5, legend=True)
  else : newcell = CellMonitoring.CellMonitoring(fig,i+1,5)

  if i != 0 : newcell.ax.get_shared_x_axes().join(cellarray[0].ax, newcell.ax) 
  if i < 6 : newcell.ax.set_xticklabels([])

  cellarray.append(newcell)
  


fig.subplots_adjust(bottom=0.2)

# Add status and warning text area


# Add button for running
run_button_ax = fig.add_axes([0.6, 0.025, 0.1, 0.04])
run_button = widgets.Button(run_button_ax, 'Run', hovercolor='0.975')


def running():
  print("entering running loop")
  global run

  while run == True :
    tstart = time.time()
    buffer_string = recvFromArduino()
    print('read time:', (time.time()-tstart))
 
    tstart = time.time()
    date = datetime.now()

    millis, cell_id, probe_id, t, err = gettemps(buffer_string)
    if millis != 0:
      wr.writerow([date, cell_id, probe_id, t, err])
      cellarray[cell_id].appendtemp(probe_id, t)
      print(t)
      plt.pause(0.01)
  
def run_button_on_clicked(mouse_event):
  # Send "Run" command 

  #global f_csv
  #global wr

  #f_csv = open(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".csv", 'w')
  #wr = csv.writer(f_csv, quoting=csv.QUOTE_ALL)

  print("sending RunCommand")
  RunCommand = "<1>"
  ser.write((RunCommand).encode())
  #waitForArduino("Running")

  global run 
  run = True
  running()


run_button.on_clicked(run_button_on_clicked)


# Add button for stopping
stop_button_ax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
stop_button = widgets.Button(stop_button_ax, 'Stop', hovercolor='0.975')
def stop_button_on_clicked(mouse_event):
  global run 
  global f_csv

  f_csv.close()

  run = False
  # Send "Stop" command
  print("Sending StopCommand")
  StopCommand = "<0>"
  ser.write((StopCommand).encode())
  waitForArduino()

stop_button.on_clicked(stop_button_on_clicked)

plt.show(block=True)

