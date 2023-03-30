import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import csv


#Array Variable for csv file 
x1 = []
y1 = []
x2 = []
y2 = []

#Function for start button
def StartButton():
    csv_filename1 = 'testplot.csv'
    csv_filename2 = 'testplot2.csv'

    #Read CSV File for Channel 1
    with open(csv_filename1) as f1:
        reader1 = np.loadtxt(csv_filename1, delimiter=";")
        for row in reader1 :
            x1.append(row[0])
            y1.append(int(row[1]))

    #Read CSV File for Channel 2
    with open(csv_filename2) as f2:
       reader2 = np.loadtxt(csv_filename2, delimiter = ";")
       for row in reader2:
           x2.append(row[0])
           y2.append(int(row[1]))
    
    #Plotting both plot simualtenously

    #Subplot for channel 1
    plt.subplot(211)
    plt.scatter(x1, y1, linewidth= 0.05, color='red', label = "Channel 1")
    plt.xlabel("Voltage(mV)")
    plt.ylabel("Current(µA)")
    plt.axis([-1.5, 1.5, -600, 600])
    plt.grid()

    #Subplot for channel 2
    plt.subplot(212)
    plt.scatter(x2, y2, linewidth = 0.05, color = 'green', label = "Channel 2")
    plt.xlabel("Voltage(mV)")
    plt.ylabel("Current(µA)")
    plt.axis([-1.5, 1.5, -600, 600])
    plt.grid()
    
    #Naming the main graph
    plt.suptitle("Voltammogram")   
    plt.show()

#Function for reset button
def ResetButton():





##APP WIDGET##

#App window 
window = tk.Tk()
window.geometry("800x450")
window.title(" Potensiostat ")


#Column 1
method = tk.Label(window, text = "Method")
method.grid(column = 0  , row = 1)

#Combobox for method dropdown button 
n = tk.StringVar()
method_choosen = ttk.Combobox(window, width = 22, textvariable = n)
method_choosen['values'] = ('DPV', 'CV')


filename = tk.Label(text = "File Name")
filename.grid(column = 0, row = 2)
Vmin = tk.Label(text = "Vmin/EBegin (V)")
Vmin.grid(column = 0, row = 3)
Vmax = tk.Label(text = "Vmax/EEnd (V)")
Vmax.grid(column = 0, row = 4)
Vincrem = tk.Label(text = "Vincrem/Estep (V)")
Vincrem.grid(column = 0, row = 5)
scanrate = tk.Label(text = "Scan Rate (mV/s)")
scanrate.grid(column = 0, row = 6)

#Column 2
#Num of channel
channel_number = tk.Label(window, text = "Num. of Channel")
channel_number.grid(column = 10 , row = 1)

#Combobox for num. of channel dropdown button
m = tk.StringVar()
channelnumber_choosen = ttk.Combobox(window, width = 22, textvariable = m)
channelnumber_choosen['values'] = ('1 Channel', '2 Channel')


cycle = tk.Label(text = "Cycle")
cycle.grid(column = 10, row = 2)
sampling = tk.Label(text = "Tsampling (ms)")
sampling.grid(column = 10, row = 3)

#Text
textArea = tk.Label(text = "Additional Parameter For DPV Method")
textArea.grid(column = 10, row = 4)

amp = tk.Label(text = "Vamp/EPulse (mV)")
amp.grid(column = 10, row = 5)
pulse = tk.Label(text = "TPulse/TRun (mS)")
pulse.grid(column = 10, row = 6)

#Input column
method_choosen.grid(column = 1, row = 1)
method_choosen.current()
filenameEntry = tk.Entry(width = 25)
filenameEntry.grid(column = 1, row = 2)
VminEntry = tk.Entry(width = 25)
VminEntry.grid(column = 1, row = 3)
VmaxEntry = tk.Entry(width = 25)
VmaxEntry.grid(column = 1, row = 4)
VincremEntry = tk.Entry(width = 25)
VincremEntry.grid(column = 1, row = 5)
scanrateEntry = tk.Entry(width = 25)
scanrateEntry.grid(column = 1, row = 6)

channelnumber_choosen.grid(column = 12, row = 1)
channelnumber_choosen.current()
cycleEntry = tk.Entry(width = 25)
cycleEntry.grid(column = 12, row = 2 )
samplingEntry = tk.Entry (width = 25)
samplingEntry.grid(column = 12, row = 3)
ampEntry = tk.Entry(width = 25)
ampEntry.grid(column = 12, row = 5)
pulseEntry = tk.Entry(width = 25)
pulseEntry.grid(column = 12, row = 6)

#Start and Reset Button
start = tk.Button(window, text = "Start", width = 15, command = StartButton)
start.grid(column = 1, row = 10)
reset  = tk.Button(window, text = "Reset", width = 15)
reset.grid(column = 12, row = 10 )

#Label Text 
ttk.Label(window, text = "Press Reset", font = ("Sherif", 10)).grid(column = 10, row = 30)
ttk.Label(window, text = "every time you change the measurement method and finish measuring", font = ("Sherif", 8)).grid(column = 10, row = 40)

window.mainloop()