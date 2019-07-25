import serial
import numpy as np
import matplotlib.pyplot as plt
from drawnow import *
import sys
from datetime import datetime

# runtime variables
plotGraph = True
serialPort = "com12" # to be redefined according to the actual port used
visibleDataPoints = 50

# Create arrays for both readings, to be used on the graph
graphChan1 = []
graphChan2 = []
experimentData = np.array(["time", "chan1","chan2"]) # numpy array for experiment data

# initialization of state variable for recording data
recording = False

# function to update plot
def updateGraph():
	if recording:
		plt.title('Live strain gage data - Recording...')
	else:
		plt.title('Live strain gage data')
	plt.grid(True) #Turn the grid on
	plt.plot(graphChan1, 'ro-', label='Channel 1')
	plt.legend(loc='upper left')
	plt2=plt.twinx()
	plt2.plot(graphChan2, 'b^-', label='Channel 2')
	plt2.legend(loc='upper right')

# function to store experiment data
def logExperiment():
	#fileName = datetime.now().strftime("%y-%m-%d_%Hh%Mm%Ss") + "_BootSensorExperimentData"
	fileName = "BootSensorExperimentData"
	np.savetxt(fileName, experimentData, delimiter=",")
	print("Experiment data saved as file: " + fileName)

# Tell matplotlib you want interactive mode to plot live data
plt.ion()

# Opens serial port
try:
	arduinoData = serial.Serial(serialPort, 9600) #Creating our serial object named arduinoData
except:
	print("Error opening serial port. Close the Serial Monitor (if open) and retry")
	sys.exit()
arduinoData.flush() #clears buffers for serial port
arduinoString = arduinoData.readline() #first line is not used for issues of truncated messages

# forever loop
while True:

	while (arduinoData.inWaiting() == 0): #Wait here until there is data
		#print("no data")
		pass


	try:
		# read line from serial and decode it
		arduinoString = arduinoData.readline()
		arduinoString = arduinoString.decode(encoding = 'utf-8')
		serialMessage = arduinoString.split(',')
		serialMessage[-1] = serialMessage[-1].strip("\r\n")
		#print(serialMessage)
	except:
		print("Problem reading Serial message. In case of crash try again")

	# identifies if message is "button_pressed"
	if serialMessage[0] == "button_pressed":
		recording = not recording
		print("Recording experiment")
		if recording:
			experimentData = np.array(["time", "chan1","chan2"]) # numpy array for experiment data
		else:
			logExperiment()
			print("Saving experiment")

	# extracts sensor data sent by arduino
	else:
		data1 = float(serialMessage[0])
		data2 = float(serialMessage[1])

		# stores data on respective graph arrays, limits size of array
		graphChan1.append(data1)
		graphChan2.append(data2)
		drawnow(updateGraph) # update live graph

		if recording:
			experimentData = np.append(experimentData,[datetime.now(), data1, data2], axis=0)

	# controls for the length of graph array
	if len(graphChan1) > visibleDataPoints:
		graphChan1.pop(0)
		graphChan2.pop(0)

plt.pause(.1)                     #Pause Briefly. Important to keep drawnow from crashing
