import serial
import numpy as np
import matplotlib.pyplot as plt
from drawnow import *
import sys
from datetime import datetime
import os

# runtime variables
plotLiveGraph = False
serialPort = "com12" # to be redefined according to the actual port used
visibleDataPoints = 50

# Create arrays for both readings, to be used on the graph
if plotLiveGraph:
	graphChan1 = []
	graphChan2 = []

# experiment data and time variables
experimentData =  [["time", "chan1","chan2"]]
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
	plt.subplot(2, 1, 1)
	plt.plot(graphChan1, label='Channel 1A')
	plt.legend(loc='upper left')
	plt.subplot(2, 1, 2)
	plt.plot(graphChan2, label='Channel 1B')
	#plt.legend(loc='upper left')

# function to store experiment data
def logExperiment():
	fileName = experimentTime.strftime("%y-%m-%d_%Hh%Mm%Ss") + "_BootSensorData.csv"
	currentDir = os.getcwd()
	dest = os.path.join(currentDir, "Data", fileName)
	npExperimentData = np.array(experimentData)
	np.savetxt(dest, experimentData, delimiter=",", fmt='%s')

# function to generate a static graph image with experiment data
def printExperimentGraph():
	#countFigures += 1
	npExperimentData = np.array(experimentData)
	npExperimentData = np.delete(npExperimentData, (0), axis=0)
	print(npExperimentData)
	plt.figure()
	plt.title("Experiment recording" + experimentTime.strftime("%y-%m-%d_%Hh%Mm%Ss"))
	plt.subplot(2, 1, 1)
	plt.plot(npExperimentData[:,1], label='Channel 1A')
	plt.subplot(2, 1, 2)
	plt.plot(npExperimentData[:,2], label='Channel 1B')
	fileName = experimentTime.strftime("%y-%m-%d_%Hh%Mm%Ss") + "_BootSensorGraph"
	currentDir = os.getcwd()
	dest = os.path.join(currentDir, "Data", fileName)
	plt.show()
	plt.savefig(dest)

# Tell matplotlib you want interactive mode to plot live data
if plotLiveGraph:
	plt.ion()

# Opens serial port
try:
	arduinoData = serial.Serial(serialPort, 9600) #Creating our serial object named arduinoData
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
		if recording:
			experimentData = [["time", "chan1","chan2"]] # numpy array for experiment data
			experimentTime = datetime.now()
			arduinoData.write(str.encode("b"))
			print("Recording experiment")
		else:
			logExperiment()
			printExperimentGraph()
			arduinoData.write(str.encode("e"))
			print("Experiment data saved")

	# extracts sensor data sent by arduino
	else:
		try:
			data1 = float(serialMessage[0])
			data2 = float(serialMessage[1])
			dataTime = datetime.now()
		except:
			data1 = ""
			data2 = ""
			print("Problem decoding serial message. Value not stored")

		# stores data on respective graph arrays, limits size of array
		if plotLiveGraph:
			graphChan1.append(data1)
			graphChan2.append(data2)
			drawnow(updateGraph) # update live graph
		else:
			print([data1, data2])

		if recording:
			experimentData.append([dataTime, data1, data2])

	# controls for the length of graph array
	if plotLiveGraph and len(graphChan1) > visibleDataPoints:
		graphChan1.pop(0)
		graphChan2.pop(0)

if plotLiveGraph:
	plt.pause(.1) #Pause Briefly. Important to keep drawnow from crashing
