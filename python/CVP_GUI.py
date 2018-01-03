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

run = False

# Create the csv file
f_csv_t = open("../csv/CVP/T" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".csv", 'w')
wr_t = csv.writer(f_csv_t, quoting=csv.QUOTE_ALL)
f_csv_p = open("../csv/CVP/P" + datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".csv", 'w')
wr_p = csv.writer(f_csv_p, quoting=csv.QUOTE_ALL)

# Create the matplotlib window
plt.ion() # set plot to animated
fig = plt.figure()
ax_t = fig.add_subplot(121)
ax_t.grid(True)
xfmt = dates.DateFormatter('%Y-%m-%d\n%H:%M:%S')
ax_t.xaxis_date()
datemin = datetime.now()
datemax = datetime.now()+timedelta(seconds=60)
ax_t.set_xlim(datemin, datemax)
ax_t.xaxis.set_major_formatter(xfmt)
plt.xticks(rotation=90)
ax_t.set_ylim(-10,35)

ax_p = fig.add_subplot(122)
ax_p.grid(True)
ax_p.xaxis_date()
ax_p.set_xlim(datemin, datemax)
ax_p.xaxis.set_major_formatter(xfmt)
plt.xticks(rotation=90)
ax_p.set_ylim(0,150)


fig.subplots_adjust(bottom=0.35)

# Add status and warning text area

t0 = fig.text(0.6, 0.1 , "Waiting...")
t1 = fig.text(0.8, 0.1 , "Looks fine!")

# Add button for running
run_button_ax = fig.add_axes([0.6, 0.025, 0.1, 0.04])
run_button = widgets.Button(run_button_ax, 'Run', hovercolor='0.975')

time_array = []
temp_array = [[] for x in range(5)]
length_array = [[] for x in range(5)]

# bool, to plot only once
plotted = False

if not plotted :

  lines_t = []
  lines_p = []

  for i in range(5):
    line_t, = ax_t.plot(time_array, temp_array[i], c=colors[i], linestyle = '', marker = '.', label='Poste '+str(i+1))
    lines_t.append(line_t)

    line_p, = ax_p.plot(time_array, temp_array[i], c=colors[i], linestyle = '', marker = '.')
    lines_p.append(line_p)

  ax_t.legend(bbox_to_anchor=(0., -0.25), loc=2, ncol=2)
  plotted = True



def running():
  print("entering running loop")
  global run
  global wr_t
  global wr_p

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

    wr_t.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), temperatures[0], temperatures[1], temperatures[2], temperatures[3], temperatures[4]])
    wr_p.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), lengths[0], lengths[1], lengths[2], lengths[3], lengths[4]])


    time_array.append(date)

    for i in range(5):
      

      temp_array[i].append(temperatures[i])
      lines_t[i].set_xdata(time_array)
      lines_t[i].set_ydata(temp_array[i]) 
      ax_t.draw_artist(lines_t[i])

      length_array[i].append(lengths[i])
      lines_p[i].set_xdata(time_array)
      lines_p[i].set_ydata(length_array[i])
      ax_p.draw_artist(lines_p[i])

      if temperatures[i] > 120 or temperatures[i] < -30:
        global t1
        warning_text = "T sensor "+str(i+1)+" returns "+str(temperatures[i])
        t1.set_text(warning_text)
        t1.set_color('r')

    global datemax
    global datemin
    if datetime.now() > datemax:
      delta = datetime.now() - datemin
      datemax = datetime.now() + delta
      ax_t.set_xlim(datemin, datemax)
      ax_p.set_xlim(datemin, datemax)

    plt.pause(0.01)

    print('time:' , (time.time()-tstart))
  
def run_button_on_clicked(mouse_event):
  # Send "Run" command 

  global f_csv_t
  global wr_t
  global f_csv_p
  global wr_p

  f_csv_t = open("../csv/CVP/T"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".csv", 'w')
  wr_t = csv.writer(f_csv_t, quoting=csv.QUOTE_ALL, delimiter = '\t')
  wr_t.writerow(["Datetime", "Temp1", "Temp2","Temp3", "Temp4", "TempExt"])
  f_csv_p = open("../csv/CVP/P"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".csv", 'w')
  wr_p = csv.writer(f_csv_p, quoting=csv.QUOTE_ALL, delimiter = '\t')
  wr_p.writerow(["Datetime", "PC1", "PC2","PC3", "PC4", "PC5"])

  print("sending RunCommand")
  RunCommand = "<1>"
  ser.write((RunCommand).encode())
  waitForArduino("Running")
  global t0
  t0.set_text("Running")
  t0.set_color('g')

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
  global t0

  run = False
  # Send "Stop" command
  print("Sending StopCommand")
  StopCommand = "<0>"
  ser.write((StopCommand).encode())
  waitForArduino()
  t0.set_text("Ready")
  t0.set_color('b')

stop_button.on_clicked(stop_button_on_clicked)

plt.show(block=True)
