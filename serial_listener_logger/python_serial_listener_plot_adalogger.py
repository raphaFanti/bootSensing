import serial
import numpy as np
import matplotlib.pyplot as plt
from drawnow import *
import sys
from datetime import datetime
import os

# runtime variables
#serialPort = "'/dev/cu.usbmodem14201'" # to be redefined according to the actual port used
visibleDataPoints = 50
plotLiveGraph=0

# Create arrays for both readings, to be used on the graph
graphChan1 = []
graphChan2 = []
graphChan3 = []
graphChan4 = []
graphChan5 = []
graphChan6 = []

# experiment data and time variables
experimentData =  [["time", "chan1","chan2","chan3","chan4","chan5","chan6"]]
#experimentData =  [["time", "chan1","chan2","chan3"]]

experimentTime = datetime.now()

# initialization of state variable for recording data
recording = False

# counter for experiment graphs. Figure 1 is the live graph
countFigures = 2

# function to update plot
def updateGraph():
	plt.figure(1)
	plt.title('Live strain gage data')
	plt.grid(True) #Turn the grid on
	plt.subplot(3, 2, 1)
	plt.plot(graphChan1, label='Chan1')
	plt.legend(loc='upper left')
	plt.subplot(3, 2, 2)
	plt.plot(graphChan2, label='Chan2')
	plt.legend(loc='upper left')
	plt.subplot(3, 2, 3)
	plt.plot(graphChan3, label='Chan3')
	plt.legend(loc='upper left')
	plt.subplot(3, 2, 4)
	plt.plot(graphChan4, label='Chan4')
	plt.legend(loc='upper left')
	plt.subplot(3, 2, 5)
	plt.plot(graphChan5, label='Chan5')
	plt.legend(loc='upper left')
	plt.subplot(3, 2, 6)
	plt.plot(graphChan6, label='Chan6')
	plt.legend(loc='upper left')


# enable live update
plt.ion()

# Opens serial port
try:
	arduinoData = serial.Serial('/dev/cu.usbmodem14201',9600) #Creating our serial object named arduinoData #'
except Exception as e:
	print("Error opening serial port. Close the Serial Monitor (if open) and retry")
	print(e)
	sys.exit()


arduinoData.flush() #clears buffers for serial port
while (arduinoData.inWaiting() == 0): #Wait here until there is data
	#print("no data")
	pass
firstString = arduinoData.readline() #first line is not used for issues of truncated messages

# forever loop
while True:

	while (arduinoData.inWaiting() == 0): #Wait here until there is data
		#print("no data")
		pass

	try:
		# read line from serial and decode it
		# [!!! ATTENTION MARI !!!] Might need different parsing of income string from adalogger
		arduinoString = arduinoData.readline()
		arduinoString = arduinoString.decode(encoding = 'utf-8') # decodes in utf-8
		serialMessage = arduinoString.split(',')
		serialMessage[-1] = serialMessage[-1].strip("\r\n") # removes undesired characters from end of message
		#print(serialMessage)
	except:
		print("Problem reading Serial message. In case of crash try again")

	# identifies if begining of message is an integer
	if isinstance(serialMessage[0], int): #python 3
	#if isinstance(serialMessage[0], (int, long)): # python 2

		try:
			data1 = int(serialMessage[1])
			data2 = int(serialMessage[2])
			data3 = int(serialMessage[3])
			data4 = int(serialMessage[4])
			data5 = int(serialMessage[5])
			data6 = int(serialMessage[6])
		except:
			data1 = ""
			data2 = ""
			data3 = ""
			data4 = ""
			data5 = ""
			data6 = ""
			print("Problem decoding serial message. Value not stored")

		graphChan1.append(data1)
		graphChan2.append(data2)
		graphChan3.append(data3)
		graphChan4.append(data4)
		graphChan5.append(data5)
		graphChan6.append(data6)

		drawnow(updateGraph) # update live graph

		# controls for the length of graph array
		if len(graphChan1) > visibleDataPoints:
			graphChan1.pop(0)
			graphChan2.pop(0)
			graphChan3.pop(0)
			graphChan4.pop(0)
			graphChan5.pop(0)
			graphChan6.pop(0)

		plt.pause(.1) #Pause Briefly. Important to keep drawnow from crashing
