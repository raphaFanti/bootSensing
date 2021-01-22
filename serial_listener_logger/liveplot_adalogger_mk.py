import serial
import numpy as np
import matplotlib.pyplot as plt
from drawnow import *
from datetime import datetime
import sys
import os

# initialize array variables
strain={}
strainData={}
cnt={}

for i in range(1,7): #create array with data of strain 1-6, datapoint counter for strain 1-6
    strain[i]=[]
    cnt[i]=[]


def makeFig(): # create a function for plot strain data 1-6
    plt.figure(1)
    plt.title('Live strain gage data')
	#plt.grid(True)
    plt.subplot(6,1,1)
    plt.plot(strain[1],'r-', label = 'Channel 1A') # plot strain1 in red
    plt.legend(loc='upper left') # legend with position
    plt.subplot(6,1,2)
    plt.plot(strain[2],'b-', label = 'Channel 1B') # plot strain2 in blue
    plt.legend(loc='upper left') # legend with position
    plt.subplot(6,1,3)
    plt.plot(strain[3],'g-', label = 'Channel 2A') # plot strain3 in green
    plt.legend(loc='upper left') # legend with position
    plt.subplot(6,1,4)
    plt.plot(strain[4], 'y-', label = 'Channel 2B') # plot strain4 in yellow
    plt.legend(loc='upper left') # legend with position
    plt.subplot(6,1,5)
    plt.plot(strain[5], 'y-', label = 'Channel 2B') # plot strain5 in yellow
    plt.legend(loc='upper left') # legend with position
    plt.subplot(6,1,6)
    plt.plot(strain[6], 'y-', label = 'Channel 2B') # plot strain6 in yellow
    plt.legend(loc='upper left') # legend with position


if makeFig:
    plt.ion() # interactive mode in plotting
try:
    arduinoData = serial.Serial('/dev/cu.HC-06-DevB',9600) # connection to arduino for Mari's Mac (via cable: '/dev/cu.usbmodem14201')
except:
	print("Error opening serial port. Close the Serial Monitor (if open) and retry") # warning if problems with serial
	sys.exit()

while True: # forever loop
    while    (arduinoData.inWaiting()==0): # Wait here until there is data
        pass # do nothing
    arduinoString = arduinoData.readline() # read text line from serial
    arduinoString = arduinoString.decode(encoding = 'utf-8') # utf8 coding
    dataArray = arduinoString.split(',') # split text line from serial by ","

    for i in range(1,7):
        strainData[i]=float(dataArray[i]) # change from string to float for strain 1-6
        strain[i].append(strainData[i]) # append strain data 1-6 in strain array

    drawnow(makeFig) # draw plot function
    plt.pause(.1) # pause to avoid drawnow from crashing

    #for i in range(1,7): # show only 50 datapoints in graph window for strain 1-6
    #    cnt[i]=cnt[i]+1
    #    if(cnt[i]>50):
    #        strain[i].pop(0)
