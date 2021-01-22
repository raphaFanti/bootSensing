import serial
import numpy as np
import matplotlib.pyplot as plt
from drawnow import *
import sys
from datetime import datetime
import os

# runtime variables
plotLiveGraph = False	
serialPort = "com20" # to be redefined according to the actual port used
visibleDataPoints = 50

# Create arrays for both readings, to be used on the graph
if plotLiveGraph:
	graphChan1 = []
	graphChan2 = []
	graphChan3 = []
	graphChan4 = []
	graphChan5 = []
	graphChan6 = []
	graphChan7 = []
	graphChan8 = []
	graphChan9 = []
	graphChan10 = []

# experiment data and time variables
experimentData =  [["time", "chan1","chan2","chan3","chan4","chan5","chan6","chan7","chan8","chan9","chan10"]]
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
	plt.subplot(4, 3, 1)
	plt.plot(graphChan1, label='Chan1')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 2)
	plt.plot(graphChan2, label='Chan2')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 3)
	plt.plot(graphChan3, label='Chan3')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 4)
	plt.plot(graphChan4, label='Chan4')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 5)
	plt.plot(graphChan5, label='Chan5')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 6)
	plt.plot(graphChan6, label='Chan6')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 7)
	plt.plot(graphChan7, label='Chan7')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 8)
	plt.plot(graphChan8, label='Chan8')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 9)
	plt.plot(graphChan9, label='Chan9')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 10)
	plt.plot(graphChan10, label='Chan10')
	plt.legend(loc='upper left')


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
	#print(npExperimentData)

	plt.figure()
	plt.title("Experiment recording" + experimentTime.strftime("%y-%m-%d_%Hh%Mm%Ss"))
	plt.subplot(4, 3, 1)
	plt.plot(npExperimentData[:,1], label='Chan1')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 2)
	plt.plot(npExperimentData[:,2], label='Chan2')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 3)
	plt.plot(npExperimentData[:,3], label='Chan3')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 4)
	plt.plot(npExperimentData[:,4], label='Chan4')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 5)
	plt.plot(npExperimentData[:,5], label='Chan5')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 6)
	plt.plot(npExperimentData[:,6], label='Chan6')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 7)
	plt.plot(npExperimentData[:,7], label='Chan7')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 8)
	plt.plot(npExperimentData[:,8], label='Chan8')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 9)
	plt.plot(npExperimentData[:,9], label='Chan9')
	plt.legend(loc='upper left')
	plt.subplot(4, 3, 10)
	plt.plot(npExperimentData[:,10], label='Chan10')
	plt.legend(loc='upper left')

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
			experimentData = [["time", "chan1","chan2","chan3","chan4","chan5", "chan6","chan7","chan8","chan9","chan10"]] # numpy array for experiment data
			#experimentData = [["time", "chan1","chan2","chan3"]]
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
			data3 = float(serialMessage[2])
			data4 = float(serialMessage[3])
			data5 = float(serialMessage[4])
			data6 = float(serialMessage[5])
			data7 = float(serialMessage[6])
			data8 = float(serialMessage[7])
			data9 = float(serialMessage[8])
			data10 = float(serialMessage[9])
			dataTime = datetime.now()
		except:
			data1 = ""
			data2 = ""
			data3 = ""
			data4 = ""
			data5 = ""
			data6 = ""
			data7 = ""
			data8 = ""
			data9 = ""
			data10 = ""
			print("Problem decoding serial message. Value not stored")

		# stores data on respective graph arrays, limits size of array
		if plotLiveGraph:
			graphChan1.append(data1)
			graphChan2.append(data2)
			graphChan3.append(data3)
			graphChan4.append(data4)
			graphChan5.append(data5)
			graphChan6.append(data6)
			graphChan7.append(data7)
			graphChan8.append(data8)
			graphChan9.append(data9)
			graphChan10.append(data10)
			drawnow(updateGraph) # update live graph
		else:
			print([data1, data2, data3, data4, data5, data6, data7, data8, data9, data10])
			#print([data1, data2, data3])

		if recording:
			experimentData.append([dataTime, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10])
			#experimentData.append([dataTime, data1, data2, data3])

	# controls for the length of graph array
	if plotLiveGraph and len(graphChan1) > visibleDataPoints:
		graphChan1.pop(0)
		graphChan2.pop(0)
		graphChan3.pop(0)
		graphChan4.pop(0)
		graphChan5.pop(0)
		graphChan6.pop(0)
		graphChan7.pop(0)
		graphChan8.pop(0)
		graphChan9.pop(0)
		graphChan10.pop(0)

if plotLiveGraph:
	plt.pause(.1) #Pause Briefly. Important to keep drawnow from crashing
