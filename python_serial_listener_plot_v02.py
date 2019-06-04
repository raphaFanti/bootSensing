import serial # import Serial Library
import numpy  # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *

tempF= []
#pressure=[]
arduinoData = serial.Serial('com7', 9600) #Creating our serial object named arduinoData
plt.ion() #Tell matplotlib you want interactive mode to plot live data
cnt=0

def makeFig(): #Create a function that makes our desired plot
    #plt.ylim(80,90)                                 #Set y min and max values
    plt.title('Channel 1')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    plt.ylabel('measurement')                            #Set ylabels
    plt.plot(tempF, 'ro-', label='Degrees F')       #plot the temperature
    plt.legend(loc='upper left')                    #plot the legend

#plt.show()

while True: # While loop that loops forever
	while (arduinoData.inWaiting()==0): #Wait here until there is data
		#print("no data")
		pass
	arduinoString = arduinoData.readline()
	arduinoString = arduinoString.decode(encoding = 'utf-8')
	#read the line of text from the serial port
	#arduinoString = str("b'ini-15214.00end\r\n'") #read the line of text from the serial port
	#print(arduinoString)
	# dataArray = arduinoString.split('ni')
	# dataArray = dataArray[1]
	# dataArray = arduinoString.strip("b'ini")
	# dataArray = arduinoString.split('end')
	# dataArray = dataArray[0]
	
	temp = float(arduinoString)            #Convert first element to floating number and put in temp
	print(temp)
	tempF.append(temp)                     #Build our tempF array by appending temp readings
	drawnow(makeFig)                       #Call drawnow to update our live graph
	plt.pause(.1)                     #Pause Briefly. Important to keep drawnow from crashing
	cnt=cnt+1
	if(cnt>50):                            #If you have 50 or more points, delete the first one from the array
		tempF.pop(0)                       #This allows us to just see the last 50 data points