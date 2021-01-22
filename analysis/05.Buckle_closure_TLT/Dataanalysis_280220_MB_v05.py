#!/usr/bin/env python
# coding: utf-8

# # Experiments @Fischer in Montebelluna 28.02.20

# We had the oppurtunity to use the Flexometer for ski boots of Fischer with their help at Montebelluna. The idea is to validate our system acquiring simultaneously data by our sensor setup and the one from their machine. With the machine of Fischer it's possible to apply exact loads.
# We used booth our sensorized ski boots (Dynafit Hoji Pro Tour W and Dynafit TLT Speedfit). The Hoji we already used in the past for our experiments in the lab @Bz with our selfbuild experiment test bench. For the TLT Speedfit this was the first experiment.
# 
# Strain gauge setup:
#     - Dynafit Hoji Pro Tour: 4 pairs of strain gauges 1-4 (a=0°, b=90°)  
#     - Dynafit TLT Speedfit: 4 triples of strain gauges 1-4 (a=0°,b=45°,c=90°)   
# As we had only a restricted time, we tested all 4 strain gauges pairs of the Hoji and only strain gauge triple 3 for TLT Speedfit. For the first time the new prototype of datalogger was running in an experiment. In addition also the first time in battery mode and not at room temperature. Unfortunately the connection of the strains to the logging system was not the best as in battery mode we don't have any possibility to control the connection to the channels yet. We'll get a solution for this the next days. 
# 
# Experiments (ambient temperature: 4°C):
# - #1: Hoji Pro Tour, 4a&b
# - #2: Hoji Pro Tour, 3a&b
# - #3: Hoji Pro Tour, 2a&b
# - #4: Hoji Pro Tour, 1a&b
# - #5: TLT Speedfit, 3a&b&c
# 
# ATTENTION: The Hoji boot was not closed as much as the TLT. Take in consideration this when looking at force/angular displacement graph.

# In[50]:


# Importing libraries
import pandas as pd
import numpy as np
import datetime
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import csv
import matplotlib.patches as mpatches #needed for plot legend
from matplotlib.pyplot import *
get_ipython().run_line_magic('matplotlib', 'inline')
from IPython.display import set_matplotlib_formats
set_matplotlib_formats('png', 'pdf')


# # Machine Data: load and plot
# The boot was loaded cyclical by the machine with a maximum of F = 150N. In each single experiment 1-5 we exported the data of the last 5 cycles.
# 

# In[51]:


#Loading data in df[expnr]: exprnr-> experiment 1-5 with cycle 1-5 
expnr=5 #number of exp
cyclenr = 5 #number of cycle per experiment
colnr = 2*cyclenr #
dfm={}
for expnr in range(expnr):
    d = {}    
    for i in range(cyclenr): #load data from cycle 1-5
        d[expnr,i] = pd.DataFrame()
        d[expnr,i] = pd.read_csv('ESP'+ str(expnr+1) + 'ciclo'+ str(i+1) +'.csv', sep='\t',header=None)
            
    dfm[expnr]=pd.concat([d[expnr,0], d[expnr,1], d[expnr,2], d[expnr,3], d[expnr,4]], axis=1, join='inner')
    dfm[expnr] = np.array(dfm[expnr]) #transform in np.array
    
    for i in range(len(dfm[expnr])): #replace , with . and change format to float 
        for j in range(colnr):
            dfm[expnr][i,j]=float(dfm[expnr][i,j].replace(',', '.'))

#print(dfm[1][:,0])


# In[52]:


figm, axm = plt.subplots(5, 5, figsize=(13, 11), sharex='col') #define plot settings
col_title = ['Experiment {}'.format(col) for col in range(1, 5)]
for i in range(expnr+1):
    for j in range(cyclenr):
        axm[j,i].plot(dfm[i][:,2*j+1],dfm[i][:,2*j])
        axm[0,i].set_title('Experiment '+ str(i+1))
        axm[j,0].set(ylabel='F[N] Cycle'+ str(j+1))
        axm[4,i].set(xlabel='angle [°]')
       
plt.tight_layout()
figm.suptitle('Machine Data Plot (Hoji Pro Tour: 1-4, TLT Speedfit: 5)',fontsize=16)
figm.subplots_adjust(top=0.88)


# On the x-axis the force F is shown (max 150N) and on the y-axis the displacement angle alpha.
# In the plot above the columns are showing the experiment and the rows the single cycles. The cycles within the same experiment are quite similar (qualitative). It's cool how clear is the difference between the two different ski boot models we used. Experiment 1-4 is showing Dynafit Hoji Pro Tour and experiment 5 the Dynafit TLT Speedfit.

# # Calculate surface under curve
# To compare the energy release between Hoji and TLT we are going to calculate the surface in the closed curve.
# We can calculate an area under a curve (curve to x-axis) by integration (E = \int{M dphi}). Via interpolation of extracted points on the curve we generate a function which is integrated afterwards by trapezian rule to get the surface. By subtracting the surface of unloading from the one of loading the area between can be calculated, which corresponds the energy release.

# In[53]:


from scipy.interpolate import interp1d
from numpy import trapz

# Experiment data
x1=dfm[1][:,1] # Exp1 cycle 1 Hoji
y1=dfm[1][:,0] # Exp1 cycle 1 Hoji

x2=dfm[4][:,1] # Exp5 cycle 1 Hoji
y2=dfm[4][:,0] # Exp5 cycle 1 Hoji

ym1=np.array([-29,17,41.14,63,96,147.8]) # x points loading Hoji
xm1=np.array([-1.5,2.9,7.312,11,13.7,13.94]) # y points loading Hoji
ym2=np.array([-29,3.741,25,43.08,63,72,106,147.8]) # x points unloading Hoji
xm2=np.array([-1.5,-0.646,1.2,3.127,6.6,8.37,13.28,13.94]) # y points unloading Hoji
ym3=np.array([-28.5,-12.27,4.841,18.01,31.92,39.46,87.48,145.6]) # x points loading TLT
xm3=np.array([-2.752,-0.989,1.022,3.23,5.387,6.012,6.521,6.915]) # y point loading TLT
ym4=np.array([-28.5,2.042,26.35,41.36,51.86,56.33,93.87,145.6]) # x points unloading TLT
xm4=np.array([-2.752,-1.94,-0.43,1.524,3.76,5.625,6.24,6.915]) # y points unloading TLt

# Interpolation
f1 = interp1d(xm1, ym1)
f2 = interp1d(xm2, ym2)
f3 = interp1d(xm3, ym3)
f4 = interp1d(xm4, ym4)

# Plot of original data and interpolation
fig0, ax0 = plt.subplots(1, 2, figsize=(15, 8))
fig0.suptitle('Ski boot testing machine', fontsize=16)
#fig0.suptitle('Interpolation of experiment data 1&5 cycle 1 (left: Hoji, right: TLT)', fontsize=16)
ax0[0].plot(x1,y1) # loading Hoji
ax0[0].set_title('Hoji Pro Tour W')
#ax0[0].plot(xm2,ym2, 'o', xm2, f2(xm2), '-', xm2, f2(xm2), '--') # unloading Hoji
#ax0[0].plot(x1,y1,xm1,ym1, 'o', xm1, f1(xm1), '-') # loading Hoji
#ax0[0].plot(xm2,ym2, 'o', xm2, f2(xm2), '-', xm2, f2(xm2), '--') # unloading Hoji
ax0[0].set(xlabel='angle [°]')
ax0[0].set(ylabel='Force [N]')
ax0[1].plot(x2,y2) # loading Hoji
ax0[1].set_title('TLT Speedfit')
#ax0[1].plot(x2,y2,xm3,ym3, 'o', xm3, f3(xm3), '-') # loading Hoji
#ax0[1].plot(xm4,ym4, 'o', xm4, f4(xm4), '-', xm4, f4(xm4), '--') # unloading Hoji
ax0[1].set(xlabel='angle [°]')
ax0[1].set(ylabel='Force [N]')
plt.show()
# Calculation of area between loading and unloading curve -> Energy 
area1_hoji=np.trapz(f1(xm1), xm1)
area2_hoji=np.trapz(f2(xm2), xm2)
area1_TLT=np.trapz(f3(xm3), xm3)
area2_TLT=np.trapz(f4(xm4), xm4)
energy_hoji=abs(area1_hoji-area2_hoji)
energy_TLT=abs(area1_TLT-area2_TLT)
#print('Energy release Hoji = ', energy_hoji, '[J]')
#print('Energy release TLT = ', energy_TLT, '[J]')


# # Bootsensing: load and plot

# We created a datalogger which is saving the experiment data in a .txt file on a SD card. After the experiments we took them from the SD card to our PC.
# Raphael Fanti did an excellent work with his file reader (https://github.com/raphaFanti/multiSensor/blob/master/analysis/03.%20Experiments_200220/Analysis%20v02/datanalysis_200220-v02.ipynb) which I'm using here to load this data. I modified the col_names as we used adapted column names the last time and updated the experiment date. He implemented also a good way to store all in a big dataframe. I'll copy also this code from Raphael.  

# In[54]:


# transforms a time string into a datetime element
def toDate(timeString):
    hh, mm, ss = timeString.split(":")
    return datetime.datetime(2020, 2, 28, int(hh), int(mm), int(ss)) # date of experiment: 28.02.20

# returns a dataframe for each sub experient
col_names = ["ID","strain1","strain2","strain3","temp","millis"] # column names from file
cols_ordered = ["time","strain1","strain2","strain3"] # order wished
cols_int = ["strain1","strain2","strain3"] # to be transformed to int columns

def getDf(fl, startTime):
            
    # ! note that we remove the first data line for each measurement since the timestamp remains zero for two first lines
    fl.readline() # line removed
    
    line = fl.readline()
    lines = []
    while "Time" not in line:
        cleanLine = line.rstrip()
        # trick for int since parsing entire column was not working
        intsLine = cleanLine.replace(".00", "")
        splitedLine = intsLine.split(",")
        lines.append(splitedLine)          
        line = fl.readline()

    # create dataframe
    df = pd.DataFrame(lines, columns = col_names)

    # create time colum
    df["time"] = df["millis"].apply(lambda x: startTime + datetime.timedelta(milliseconds = int(x)))      

    # drop ID, millis and temperature, and order columns
    df = df.drop(["ID", "temp", "millis"], axis = 1)
    df = df[cols_ordered]

    # adjust types
    df[cols_int] = df[cols_int].astype(int)

    return df


# Load data to dataframe. As we were not working with our usually experiment protocol, I had to skip phase = bs2.

# In[55]:


filenames = ["2022823_exp1","2022848_exp2","2022857_exp3", "202285_exp4", "2022829_exp5"]
nExp = len(filenames) # we simply calculate the number of experiments

# big data frame
df = pd.DataFrame()

for i, this_file in enumerate(filenames):
    # experiment counter
    exp = i + 1
    
    # open file
    with open(this_file + ".TXT", 'r') as fl:
        
        # throw away first 3 lines and get baseline 1 start time
        for i in range(3):
            fl.readline()
            
        # get start time for first baseline
        bl1_time = fl.readline().replace("BASELINE Time: ", "")
        startTime = toDate(bl1_time)
        
        # get data for first baseline
        df_bl1 = getDf(fl, startTime)
        df_bl1["phase"] = "bl1"
        
        # get start time for experiment
        exp_time = fl.readline().replace("RECORDING Time: ", "")
        startTime = toDate(exp_time)
        
        # get data for experiment
        df_exp = getDf(fl, startTime)
        df_exp["phase"] = "exp" 
        
        # get start time for second baseline
        #bl2_time = fl.readline().replace("BASELINE Time: ", "")
        #startTime = toDate(bl2_time)
        
        # get data for second baseline
        #df_bl2 = getDf(fl, startTime)
        #df_bl2["phase"] = "bl2"
        
        # create full panda
        df_exp_full = pd.concat([df_bl1, df_exp])
        
        # create experiment column
        df_exp_full["exp"] = exp
        
    df = pd.concat([df, df_exp_full])

# shift columns exp and phase to begining
cols = list(df.columns)
cols = [cols[0]] + [cols[-1]] + [cols[-2]] + cols[1:-2]
df = df[cols]
#print(df)    


# In[56]:


def plotExpLines(df, exp):
    fig, ax = plt.subplots(3, 1, figsize=(15, 8), sharex='col')

    fig.suptitle('Experiment ' + str(exp), fontsize=16)
    # fig.subplots_adjust(top=0.88)

    ax[0].plot(dfExp["time"], dfExp["strain3"], 'tab:green')
    ax[0].set(ylabel='strain3')

    ax[1].plot(dfExp["time"], dfExp["strain1"], 'tab:red')
    ax[1].set(ylabel='strain1')

    ax[2].plot(dfExp["time"], dfExp["strain2"], 'tab:blue')
    ax[2].set(ylabel='strain2')
    ax[2].set(xlabel='time [ms]')

    plt.show()


# ### Experiment 1

# In[57]:


figure(num=None, figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')
plt.plot(df[df["exp"] == 1]['time'],df[df["exp"] == 1]['strain3'])
plt.xlabel('daytime')
plt.ylabel('4A')
plt.title('Experiment 1: 4A ')
plt.show()


# We applied 34 cycles.

# ### Experiment 2

# In[58]:


figure(num=None, figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')
plt.plot(df[df["exp"] == 2]['time'],df[df["exp"] == 2]['strain3'])
plt.xlabel('daytime')
plt.ylabel('3A')
plt.title('Experiment 2: 3A ')
plt.show()


# # Experiment 3

# In[59]:


figure(num=None, figsize=(10, 8), dpi=80, facecolor='w', edgecolor='k')
plt.plot(df[df["exp"] == 3]['time'],df[df["exp"] == 3]['strain3'])
plt.xlabel('daytime')
plt.ylabel('2B')
plt.title('Experiment 3: 2B ')
plt.show()


# ### Experiment 4

# In[60]:


figure(num=None, figsize=(12, 8), dpi=80, facecolor='w', edgecolor='k')
plt.plot(df[df["exp"] == 4]['time'],df[df["exp"] == 4]['strain3'])
plt.xlabel('daytime')
plt.ylabel('1A')
plt.title('Experiment 4: 1A ')
plt.show()


# ### Experiment 5

# In[61]:


fig, ax = plt.subplots(2, 1, figsize=(15, 8), sharex='col')

fig.suptitle('Experiment 5: 3B & 3C ', fontsize=16)
    # fig.subplots_adjust(top=0.88)
ax[0].plot(df[df["exp"] == 5]['time'], df[df["exp"] == 5]['strain3'], 'tab:green')
ax[0].set(ylabel='3C')
ax[1].plot(df[df["exp"] == 5]['time'], df[df["exp"] == 5]['strain2'], 'tab:red')
ax[1].set(ylabel='3B')
ax[1].set(xlabel='daytime')
plt.show()


# In[62]:


#dfExp = df[df["exp"] == 3]

#plotExpLines(dfExp, 3)


# # Analysis
# Now we try to compare the data from the Flexometer of Fischer and from our Bootsensing. 
#     - Fischer: force F over displacement angle alpha 
#     - Bootsensing: deformation measured by strain gauge (resistance change) in at the moment unknown unit over time (daytime in plot shown)
# The idea now is to identify the last 5 cycles in Bootsensing data automatically and to exstract time information (t0,t). Afterwards this delta t can be applied on Fischers data to plot force F over the extracted time.  

# ### Bootsensing: Cycle identification
# For Experiment 1-5 we will identfy the last 5 cycles of strain3. As the data of Fischer starts at a peak (maximum load), we will identify them also in our bootsensing data and extract the last 6 peak indexes. Applying these indices on strain3/time data we get the last 5 cycles.
# 
# Find peaks: find_peaks function https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
# Find valley: with Inverse of find peaks
# 
# 

# In[63]:


from scipy.signal import find_peaks
import numpy as np
# Load data of Experiments 1-5 
ds={} # dict for strain data -> dataformat will be changed
dt={} # time data
peaks={} # peaks
valleys={} # valleys
inv_ds={} # inverse for valleys calculation
ds_peaks={} # index of peak (used for 5-2)
ds_peaks_end={} # index of last peaks
ds_valleys_end = {} # index of last valley
ds_valleys={} # index of valley (used for 5-2)
len_valley={} # valley lenght
for i in range(1,6): # i = Experiment number
    ds[i]=df[df["exp"] == i]['strain3'] #data for strain3
    dt[i]=df[df["exp"] == i]['time'] # time data
    ds[i]=ds[i].dropna() # drop NaN
    dt[i]=dt[i].dropna()
    ds[i]=ds[i].reset_index(drop=True) #reset index
    dt[i]=dt[i].reset_index(drop=True)
    peaks[i],_=find_peaks(ds[i],prominence=100000) # find peaks
    inv_ds[i]=ds[i]*(-1) # inverse of ds
    valleys[i],_=find_peaks(inv_ds[i],prominence=10000) # find valleys
    
    for j in range(1,6): # j = cycle number
        ds_valleys[j,i]=valleys[i][-1-j:-j] # selecting last 5 valleys
        ds_valleys_end[j,i]=valleys[i][-1:] # select last valley
        ds_valleys[j,i]=ds_valleys[j,i][0] # assign index
        ds_valleys_end[j,i]=ds_valleys_end[j,i][0]
        ds_peaks[j,i]=peaks[i][-1-j:-j] # selecting last 5 peaks
        ds_peaks_end[j,i]=peaks[i][-1:] # select last peak
        ds_peaks[j,i]=ds_peaks[j,i][0] # assign index
        ds_peaks_end[j,i]=ds_peaks_end[j,i][0]
#print(ds1[1][ds_valleys[1,1]])    
    
#Calculate cycle lengths
#for i in range(1,6):
    #len_valley[e] = dt1[e][ds_valleys[1,1]] - dt1[e][ds_valleys[2,1]] #1th
    #len_valley1_2[i] = dt1[ds_valley_3[i]] - dt1[ds_valley_4[i]] #2th
    #len_valley2_3[i] = dt1[ds_valley_2[i]] - dt1[ds_valley_3[i]] #3th
    #len_valley3_4[i] = dt1[ds_valley_1[i]] - dt1[ds_valley_2[i]] #4th
    #len_valley4_5[i] = dt1[ds_valley_last_end[i]] - dt1[ds_valley_1[i]] #5th

# EXPERIMENT 1: pay attention for peaks/valley after cycles    


# Now we will plot the data for strain3 for each experiment with their peaks and valleys.

# In[64]:


# Plot peaks and valleys for Exp 1-5 for strain3
fig1, ax1 = plt.subplots(5, 1, figsize=(15, 8))
fig1.subplots_adjust(top=2)
fig1.suptitle('Experiments 1-5: peaks and valleys ', fontsize=16)
for i in range(5): # i for Experiment number
    ax1[i].plot(df[df["exp"] == (i+1)]['time'], df[df["exp"] == (i+1)]['strain3'], 'tab:green')
    ax1[i].plot(dt[(i+1)][peaks[(i+1)]],ds[(i+1)][peaks[(i+1)]],"x") #Plot peaks with x
    ax1[i].plot(dt[(i+1)][valleys[(i+1)]],ds[(i+1)][valleys[(i+1)]],"o") #Plot valleys with o
    ax1[i].set(ylabel='raw signal')
    ax1[i].set(xlabel='daytime')
    ax1[i].set_title('Experiment'+str(i+1))
    plt.tight_layout()
    fig1.subplots_adjust(top=0.88) # spacer between title and plot
plt.show()

# Plot last 5 cycles for Exp 1-5 for strain3
fig2, ax2 = plt.subplots(5, 1, figsize=(10, 8))
fig2.suptitle('Experiments 1-5: last 5 cycles ', fontsize=16)
for i in range(5): # i for Experiment number
    ax2[i].plot(dt[(i+1)][ds_valleys[5,(i+1)]:ds_valleys_end[1,(i+1)]],ds[(i+1)][ds_valleys[5,(i+1)]:ds_valleys_end[1,(i+1)]]) # select data between 5th last and last valley
    #ax2[i].plot(dt[(i+1)][ds_peaks[5,(i+1)]:ds_peaks_end[1,(i+1)]],ds[(i+1)][ds_peaks[5,(i+1)]:ds_peaks_end[1,(i+1)]])# select data between 5th last and last peak
    ax2[i].set(ylabel='raw signal')
    ax2[i].set(xlabel='daytime')
    ax2[i].set_title('Experiment'+str(i+1))
    plt.tight_layout()
    fig2.subplots_adjust(top=0.88) # spacer between title and plot
plt.show()    

#plt.axvline(x=dt[ds_valley_2_index],color="grey") #time borders 3th cycle
#plt.axvline(x=dt[ds_valley_3_index],color="grey")
#plt.axhline(y=ds[ds_valley_3_index],color="red") # h line


# For Experiment 2-5 the last 5 cycles are clear. The signal of experiment 1 is raising again after the cyclic loading as it's not possible to select the last 5 cycles with this "peaks" method, but happily we can extract still the last cycle.
# As we can see in the plot of the last 5 cycles above, the last cycle for Exp1, Exp3 and Exp5 is ending with a peak where Exp2 and Exp4 is ending with a valley. We can say this from the plots as we know from our exported machine data that a cycle ends always with the maximum force of 150N. This means a valley or peak for our bootsensing system. 

# ### Match Fischer Data with Bootsensing cycle time 
# Now we are going to match the Bootsensing cycle time with the force data of Fischer for each experiment 1-5. As the machine of Fischer applied the load with a frequency of 0.33 Hz, the cycle length of each cycle should be approximately t=3s. We verified this calculating the length between 2 neighbour valley of our bootsensing data (see code above).

# In[65]:


#Identify frequency of Fischer Dataacquisition
f={} # Fischer force matrix
freq={} # matrix with vector lenght to identify frequency
for i in range(5): #
    f[i] = dfm[i][:,2*i] # load force data for Exp5, strain3   0,2,4,6,8
    freq[i] = len(dfm[i][:,2*i]) # force vector len

#Create time linspace for Fischer data
#Timestamp can not be selected by item, done without manually
time_start1=dt[1][ds_peaks[5,1]] # Exp1: select manually last cycle
time_end1=dt[1][ds_peaks[4,1]] 
time_start2=dt[2][ds_valleys[5,2]] # Exp2
time_end2=dt[2][ds_valleys[4,2]]
time_start3=dt[3][ds_peaks[5,3]] # Exp3
time_end3=dt[3][ds_peaks[4,3]]
time_start4=dt[4][ds_valleys[5,4]] # Exp4
time_end4=dt[4][ds_valleys[4,4]]
time_start5=dt[5][ds_peaks[5,5]] # Exp5
time_end5=dt[5][ds_peaks[4,5]]
#print(time_start1,time_end1)

x1=pd.date_range(time_start1, time_end1, periods=freq[0]).to_pydatetime()
x2=pd.date_range(time_start2, time_end2, periods=freq[1]).to_pydatetime()
x3=pd.date_range(time_start3, time_end3, periods=freq[2]).to_pydatetime()
x4=pd.date_range(time_start4, time_end4, periods=freq[3]).to_pydatetime()
x5=pd.date_range(time_start5, time_end5, periods=freq[4]).to_pydatetime()

#Plot Fischer Data in timerange x
fig3, ax3 = plt.subplots(5, 2, figsize=(12, 10))
fig3.suptitle('Experiments 1-5: Fischer F over Bootsensing daytime (left), Bootsensing cycle (right) ', fontsize=16)
ax3[0,0].plot(x1,f[0])
ax3[0,0].set(xlabel='daytime')
ax3[0,0].set(ylabel='F[N]')
ax3[0,0].set_title('Experiment 1')
ax3[1,0].plot(x2,f[1])
ax3[1,0].set(xlabel='daytime')
ax3[1,0].set(ylabel='F[N]')            
ax3[1,0].set_title('Experiment 2')
ax3[2,0].plot(x3,f[2])
ax3[2,0].set(xlabel='daytime')
ax3[2,0].set(ylabel='F[N]')            
ax3[2,0].set_title('Experiment 3')
ax3[3,0].plot(x4,f[3])
ax3[3,0].set(xlabel='daytime')
ax3[3,0].set(ylabel='F[N]')            
ax3[3,0].set_title('Experiment 4')
ax3[4,0].plot(x5,f[4])
ax3[4,0].set(xlabel='daytime')
ax3[4,0].set(ylabel='F[N]')            
ax3[4,0].set_title('Experiment 5')             

#for i in range(1,5): # Exp2-5
    #ax3[i,1].plot(dt[i+1][ds_peaks[2,i+1]:ds_peaks[1,i+1]],ds[i+1][ds_peaks[2,i+1]:ds_peaks[1,i+1]])
    #ax3[i,1].set(ylabel='strain3')
    #ax3[i,1].set(xlabel='daytime')
ax3[0,1].plot(dt[1][ds_peaks[5,1]:ds_peaks[4,1]],ds[1][ds_peaks[5,1]:ds_peaks[4,1]]) # special for Exp1 with peaks 
ax3[0,1].set(xlabel='daytime')
ax3[0,1].set(ylabel='4A') 
ax3[1,1].plot(dt[2][ds_valleys[5,2]:ds_valleys[4,2]],ds[2][ds_valleys[5,2]:ds_valleys[4,2]]) #Exp2 with valleys
ax3[1,1].set(xlabel='daytime')
ax3[1,1].set(ylabel='3A')
ax3[2,1].plot(dt[3][ds_peaks[5,3]:ds_peaks[4,3]],ds[3][ds_peaks[5,3]:ds_peaks[4,3]]) #Exp3 with peaks
ax3[2,1].set(xlabel='daytime')
ax3[2,1].set(ylabel='2B')
ax3[3,1].plot(dt[4][ds_valleys[5,4]:ds_valleys[4,4]],ds[4][ds_valleys[5,4]:ds_valleys[4,4]]) # Exp4 with valley
ax3[3,1].set(xlabel='daytime')
ax3[3,1].set(ylabel='1A')
ax3[4,1].plot(dt[5][ds_peaks[5,5]:ds_peaks[4,5]],ds[5][ds_peaks[5,5]:ds_peaks[4,5]]) #Exp5 with peaks
ax3[4,1].set(xlabel='daytime')
ax3[4,1].set(ylabel='3B')

plt.tight_layout()
fig3.subplots_adjust(top=0.88) # spacer between title and plot
plt.show() 


# In the graphs of Fischer data (left side) you can note a little kink in unloading as well as in loading. In experiment 5 (TLT) the kink is much more prominent.
# ATTENTION: As we verified the length between neighbour valleys as well as neighbour peaks in our bootsensing data, we can confirm the freqeuncy of f=0.33 Hz applied by the machine (see plots below). 

# ### Time delta Fischer&bootsensing

# Now we're going to find identify the extrema for Fischer force data and out bootsensing strain data for each single Experiment 1-5. As we applied the same timespan on the x-axis for both plot we can compare the x-coordinate of the left plot with the corresponding right one to check the response time (time delay) of our bootsensing system (like reaction time of strain gauges).

# In[66]:


# Find extrema in Fischer F for Exp 1-5 in last cycle
inv_f={} # inverse of F
valleys_f={} # valleys in Fischer F
fmin={} # f for extrema
for i in range(5): # find extrema (in this case valley)
    inv_f[i]=f[i]*(-1) # inverse of f
    valleys_f[i],_=find_peaks(inv_f[i],prominence=10) # find valleys
    fmin[i]=f[i][valleys_f[i]] # y-coordinate for minima
# x-coordinate for minima    
x1min=x1[valleys_f[0]] #Exp1
x2min=x2[valleys_f[1]] #Exp2
x3min=x3[valleys_f[2]] #Exp3
x4min=x4[valleys_f[3]] #Exp4
x5min=x5[valleys_f[4]] #Exp5

# Find extrema in bootsensing data for Exp 1-5 in last cycle
# extract time and strain for last cycle Exp1-5 (manually)
t1=dt[1][ds_peaks[5,1]:ds_peaks[4,1]] # Exp1 -> valley
t1=t1.reset_index(drop=True) # reset index
ds1=ds[1][ds_peaks[5,1]:ds_peaks[4,1]] 
ds1=ds1.reset_index(drop=True)
t2=dt[2][ds_valleys[5,2]:ds_valleys[4,2]] # Exp2 -> peak
t2=t2.reset_index(drop=True)
ds2=ds[2][ds_valleys[5,2]:ds_valleys[4,2]] 
ds2=ds2.reset_index(drop=True)
t3=dt[3][ds_peaks[5,3]:ds_peaks[4,3]] # Exp3 -> valley
t3=t3.reset_index(drop=True)
ds3=ds[3][ds_peaks[5,3]:ds_peaks[4,3]]
ds3=ds3.reset_index(drop=True)
t4=dt[4][ds_valleys[5,4]:ds_valleys[4,4]] # Exp4 -> peak
t4=t4.reset_index(drop=True)
ds4=ds[4][ds_valleys[5,4]:ds_valleys[4,4]]
ds4=ds4.reset_index(drop=True)
t5=dt[5][ds_peaks[5,5]:ds_peaks[4,5]] # Exp5 -> valley
t5=t5.reset_index(drop=True)
ds5=ds[5][ds_peaks[5,5]:ds_peaks[4,5]]
ds5=ds5.reset_index(drop=True)

# Find valley for Exp1,3,5
valley_ds1,_=find_peaks(ds1*(-1)) # Exp1
valley_ds3,_=find_peaks(ds3*(-1)) # Exp3
valley_ds5,_=find_peaks(ds5*(-1)) # Exp5

# Find peak for Exp2,4
peak_ds2,_=find_peaks(ds2) # Exp2
peak_ds4,_=find_peaks(ds4) # Exp4

# Apply extrema index on x-coordinate of bootsensing for Exp1-5
t1ext=t1[valley_ds1].dt.to_pydatetime() # converting in same format as xmin
t2ext=t2[peak_ds2].dt.to_pydatetime()
t3ext=t3[valley_ds3].dt.to_pydatetime()
t4ext=t4[peak_ds4].dt.to_pydatetime()
t5ext=t5[valley_ds5].dt.to_pydatetime()

#Calculating timedelta in format to_pydatetime()
deltat1=t1ext-x1min
deltat2=t2ext-x2min
deltat3=t3ext-x3min
deltat4=t4ext-x4min
deltat5=t5ext-x5min
print(deltat1,deltat2,deltat3,deltat4,deltat5)


# If we look at the timedelta for Exp1-5 we see that we are in range of deltat=0,007678s-0,1669s. For the setup at the moment if is enough. Maybe by increasing the data acquisition frequency we could improve this time delta.

# As we know that the machine applied the load with a frequency of f=0.33 Hz with f=1/T we can calculate the timespan of loading. Identifying the vector length of Fischer force data we can plot the force over time for each single cycle.

# In[67]:


fm=0.33 # frequency in Hz (preset)
T=1/fm #calculate time period T
fd={}
for i in range(5):
    fd[i]= len(f[i])
freq=fd[0] #as all fd[i] have the same length we choose f[0]
x = np.linspace(0, T, freq, endpoint=False) 

#Plot 
fig4, ax4 = plt.subplots(5, 1, figsize=(6, 8))
fig4.suptitle('Experiments 1-5: Fischer F over time t ', fontsize=16)
for i in range(5):
    ax4[i].plot(x,f[i])
    ax4[i].set(xlabel='daytime')
    ax4[i].set(ylabel='F[N]')
    ax4[i].set_title('Experiment '+str(i+1))
 
plt.tight_layout()
fig4.subplots_adjust(top=0.88) # spacer between title and plot
plt.show()


# In[68]:


# Plot an example experiment with peaks and valleys for thesis
fig5, ax5 = plt.subplots(1, figsize=(15, 8))
#fig5.subplots_adjust(top=2)
#fig5.suptitle('Experiments 1-5: peaks and valleys ', fontsize=16)
ax5.plot(df[df["exp"] == (3)]['time'], df[df["exp"] == (3)]['strain3'], 'tab:blue',label='strain gauge 2b')
ax5.plot(dt[(3)][peaks[(3)]],ds[(3)][peaks[(3)]],"rx",label='peak') #Plot peaks with x
ax5.plot(dt[(3)][valleys[(3)]],ds[(3)][valleys[(3)]],"ro",label='valley') #Plot valleys with o
ax5.set(ylabel='raw signal')
ax5.set(xlabel='daytime')
ax5.set_title('Cyclic loading of TLT Speedfit')
ax5.legend()
plt.tight_layout()
fig5.subplots_adjust(top=0.88) # spacer between title and plot
plt.show()


# # Machine force and strain data matching

# In[69]:


from datetime import timedelta

# Select strain 4A (stored in strain3) and machine data for Experiment 1
data_s1=pd.concat([dt[1][ds_peaks[5,1]:ds_peaks[4,1]], ds[1][ds_peaks[5,1]:ds_peaks[4,1]]],axis=1).reset_index(drop=True) # one dataframe with strain and time

# Select strain 3C (stored in strain3) and machine data for Experiment 5
data_s5C=pd.concat([dt[5][ds_peaks[5,5]:ds_peaks[4,5]],ds[5][ds_peaks[5,5]:ds_peaks[4,5]]],axis=1).reset_index(drop=True) # one dataframe with strain and time

# Convert machine time to DataFrame in ms precision
x1=pd.DataFrame(x1,columns=['time']).astype('datetime64[ms]') # Experiment 1
x5=pd.DataFrame(x5,columns=['time']).astype('datetime64[ms]') # Experiment 5

# Convert machine force data to DataFrame
f1=pd.DataFrame(f[0],columns=['force [N]']) # Experiment 1
f5=pd.DataFrame(f[4],columns=['force [N]']) # Experiment 5

# Make one dataframe with machine time and force
data_m1=pd.concat([x1,f1],axis=1) 
data_m5C=pd.concat([x5,f5],axis=1) 

# Create new time for data_s storing in data_splus1
d = timedelta(microseconds=1000)
data_snew1=[]
data_snew5=[]
for i in range(0,len(data_s1)): # Experiment 1
    data_new1=data_s1.iloc[i,0]+d
    data_snew1.append(data_new1)
    
for i in range(0,len(data_s5C)): # Experiment 5
    data_new5=data_s5C.iloc[i,0]+d
    data_snew5.append(data_new5)
    
data_splus11=pd.DataFrame(data_snew1,columns=['time']) # convert data_snew in DataFrame
data_splus12=pd.concat([data_splus11,data_s1['strain3']],axis=1) # concat data_s with data_splus1

data_splus51C=pd.DataFrame(data_snew5,columns=['time']) # convert data_snew in DataFrame
data_splus52C=pd.concat([data_splus51C,data_s5C['strain3']],axis=1) # concat data_s with data_splus1

# Data matching of strain 4A with corresponding force Experiment 1
data_match11=pd.merge(data_s1, data_m1, on=['time'])
data_match12=pd.merge(data_splus12, data_m1, on=['time'])
data_4A=pd.concat([data_match11, data_match12]).sort_values('time').reset_index(drop=True)
data_4A=data_4A.rename(columns={'strain3':'strain 4A'})

# Data matching of strain 3B with corresponding force Experiment 5
data_match51C=pd.merge(data_s5C, data_m5C, on=['time'])
data_match52C=pd.merge(data_splus52C, data_m5C, on=['time'])
data_3C=pd.concat([data_match51C, data_match52C]).sort_values('time').reset_index(drop=True)
data_3C=data_3C.rename(columns={'strain3':'strain 3C'})


# In[70]:


fig6, ax6 = plt.subplots(1, 2, figsize=(15, 6))
fig6.suptitle('Experiment 1: HOJI PRO TOUR W', fontsize=16)
ax6[0].plot(data_4A.iloc[0:15,2],data_4A.iloc[0:15,1])
ax6[0].set(ylabel="Strain 4A")
ax6[0].set(xlabel="Force [N]")
ax6[0].set_title('Loading')
ax6[1].plot(data_4A.iloc[15:-1,2],data_4A.iloc[15:-1,1])
ax6[1].set(ylabel="Strain 4A")
ax6[1].set(xlabel="Force [N]")
ax6[1].set_title('Unloading')
plt.show()

plt.plot(data_4A.iloc[:,2],data_4A.iloc[:,1])
plt.xlabel('Force [N]')
plt.ylabel('Strain 4A')
plt.title('Loading & Unloading')
plt.show()


# In[71]:


fig7, ax7 = plt.subplots(1, 2, figsize=(15, 6))
fig7.suptitle('Experiment 5: TLT SPEEDFIT', fontsize=16)
ax7[0].plot(data_3C.iloc[0:15,2],data_3C.iloc[0:15,1])
ax7[0].set(ylabel="Strain 3C")
ax7[0].set(xlabel="Force [N]")
ax7[0].set_title('Loading')
ax7[1].plot(data_3C.iloc[15:-1,2],data_3C.iloc[15:-1,1])
ax7[1].set(ylabel="Strain 3C")
ax7[1].set(xlabel="Force [N]")
ax7[1].set_title('Unloading')
plt.show()

plt.plot(data_3C.iloc[:,2],data_3C.iloc[:,1])
plt.xlabel('Force [N]')
plt.ylabel('Strain 3C')
plt.title('Loading & Unloading')
plt.show()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




