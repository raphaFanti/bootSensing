import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial
import sys
import os
import pylab

# Load Adalogger data from serial
arduinoData = serial.Serial('/dev/cu.usbmodem14201',9600) # connection to arduino for Mari's Mac (via cable: '/dev/cu.usbmodem14201')

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
#ax2 = fig.add_subplot(3, 1, 2)
#ax3 = fig.add_subplot(3, 1, 3)

# Initialize variables
xs = []
ys1 = []
ys2 = []
ys3 = []
#ys2 = []
strain= [] # strain dataframe
strainData={} # strain dataframe for changing data from str to float
strainconvert={} # convert in voltage value
strainData1 = []

# Values for digital-analog-converting
V = 3.3 # Adalogger voltage V = 3.3V
adc = 2**24 # 24bit ADC
gain = 128 # pga set_gain = 128

# This function is called periodically from FuncAnimation
def animate(i, xs, ys1,ys2,ys3):

    # Read data from Arduino in serial
    arduinoString = arduinoData.readline() # read text line from serial
    arduinoString = arduinoString.decode(encoding = 'utf-8') # utf8 coding
    dataArray = arduinoString.split(',') # split text line from serial by ","

    for i in range(1,4):
        strainData[i]=float(dataArray[i]) # change from string to float for strain 1-6
        strainconvert[:,i] = (((strainData[:,i]/adc)*V)/gain)*1000
        #strain[i].append(strainconvert[i]) # append strain data 1-6 in strain array
    #strainData1=float(dataArray[1])
    #ys1=strain[1]
    ys1.append(strainData[1])
    ys2.append(strainData[2])
    ys3.append(strainData[3])

    # Read time from dataArray
    time = float(dataArray[5])
    xs.append(time)
    #xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    #ys1=strain[1]
    #ys2=strain[2]
    #ys3=strain[3]

    # Draw x/y
    ax.clear()

    ax.plot(xs, ys1,'r-',label='3A')
    ax.plot(xs, ys2,'b-',label='3B')
    ax.plot(xs, ys3,'g-',label='3C')


    # Format plot
    plt.subplots_adjust(bottom=0.30)
    plt.title('Live #Bootsensing')
    plt.ylabel('voltage [mV]')
    plt.xlabel('time [s]')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys1,ys2,ys3), interval=1) # interval = 1 for fast live plotting
plt.show() # show plot
