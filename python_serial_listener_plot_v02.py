import serial # import Serial Library
import numpy as np # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *

# Create arrays for both readings, to be used on the graph
chan1 = []
chan2 = []

# Create numpy arrays for storing the data experiment data
experimentData = np.array(["TimeStamp", "Channel1","channel2"])

# Opens serial port
serialPort = "com12" # to be redefined according to the actual port used
arduinoData = serial.Serial(serialPort, 9600) #Creating our serial object named arduinoData

# Tell matplotlib you want interactive mode to plot live data
plt.ion() 

# counter for data points on the graph
visibleDataPoints = 50
cnt=0

def makeFig(): #Create a function that makes our desired plot
	#plt.ylim(80,90)                                 #Set y min and max values
	plt.title('Live strain gage data')      #Plot the title
	plt.grid(True)                                  #Turn the grid on
	#plt.ylabel('getUnits')                            #Set ylabels
	plt.plot(chan1, 'ro-', label='Channel 1')       #plot the temperature
	plt.legend(loc='upper left')                    #plot the legend
	plt2=plt.twinx()                                #Create a second y axis
	#plt.ylim(93450,93525)                           #Set limits of second y axis- adjust to readings you are getting
	plt2.plot(chan2, 'b^-', label='Channel 2') #plot pressure data
	#plt2.set_ylabel('getUnits')                    #label second y axis
	#plt2.ticklabel_format(useOffset=False)           #Force matplotlib to NOT autoscale y axis
	plt2.legend(loc='upper right')                  #plot the legend

while True: # While loop that loops forever
	
	while (arduinoData.inWaiting()==0): #Wait here until there is data
		#print("no data")
		pass
	
	# read line from serial and decode it
	arduinoString = arduinoData.readline()
	arduinoString = arduinoString.decode(encoding = 'utf-8')
	dataArray = arduinoString.split(',')
	print(dataArray)
	
	if dataArray[0] == "button_input": # identifies if message is from experiment
		timeStamp = int(dataArray[1])
		dt1 = float(dataArray[2])            
		dt2 = float(dataArray[3].strip("\r\n")) # for some reason, carriage return and end of line need to me removed
		experimentData = np.append(experimentData,[timeStamp, dt1, dt2], axis=0)
		print("Experiment data logged")
		#print(experimentData[-1])
		
	else: # in case the message is not from experiment, data is retrieved for plotting
	
		#Convert data elements to float
		
		dt1 = float(dataArray[0])            
		dt2 = float(dataArray[1].strip("\r\n"))
		
		
		chan1.append(dt1)                     #Build our chan1 array by appending temp readings
		chan2.append(dt2)
		#drawnow(makeFig)                       #Call drawnow to update our live graph
		
		plt.pause(.1)                     #Pause Briefly. Important to keep drawnow from crashing
		
		# remove points on data array to limit axe
		cnt = cnt+1
		if(cnt > visibleDataPoints):
			chan1.pop(0)
			chan2.pop(0)