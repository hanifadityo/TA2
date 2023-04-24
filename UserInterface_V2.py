import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import glob
import os.path
import serial
from serial import Serial
import scipy.signal as signal
    
window = tk.Tk()


#Start Button Function
def StartButton():
    parent_folder = "D:\TA2"
    save = parent_folder+"/Potensiostat"
    methodnumber  = "0"
    direct = ""

    if (inputmethod.get() == 'CV') :
        methodnumber = "1"
        direct = "CV"

    elif(inputmethod.get() == 'DPV') :
        methodnumber = "2"
        direct = "DPV"

    else :
        methodnumber = ""
    
    path_file = os.path.join(save, direct)

    os.makedirs(path_file, exist_ok = True)
    
    #Define Variable to Validate Value of Input Parameter
    CheckVmin = float(vmin_var.get())
    CheckVmax = float(vmax_var.get())
    CheckScanRate = int(scanrate_var.get())
    CheckCycle = int(cycle_var.get())
    CheckAmp = float(amp_var.get())
    CheckIncrement = float(vincrem_var.get())
    CheckSampling  = float(sampling_var.get())
    CheckPulse = float(pulse_var.get())

    #Validate Parameter Input From User
    if methodnumber == "" or vmin_var.get() == "" or vmax_var.get() == "" or scanrate_var.get() =="" or cycle_var.get() == "" or inputchannelnumber.get() =="" or amp_var.get() == "" or vincrem_var.get() == "" or pulse_var.get() == "" or sampling_var.get() == "" or inputfilename.get() =="":
        messagebox.showerror("ERROR", "Please Enter All Value of Input Parameter")
    elif methodnumber == '1':
        if CheckVmin < -1.5 or CheckVmin > 1.5 :
            messagebox.showerror("ERROR", "Please Enter Vmin Value Between -1.5V - 1.5V")
        elif CheckVmax < -1.5 or CheckVmax > 1.5 :
            messagebox.showerror("ERROR", "Please Enter Vmax Value Between -1.5V - 1.5V")
        elif CheckScanRate < 10 or CheckScanRate > 120: 
            messagebox.showerror("ERROR", "Please Enter Scan Rate Value Between 10 - 120 mV/s")
        else :
            parameter = inputmethod.get() + ";" + vmin_var.get() + ";" + vmax_var.get() + ";" + vincrem_var.get() + ";" + scanrate_var.get() + ";" + cycle_var.get() + ";" + sampling_var.get() + ";" + amp_var.get() + ";" + pulse_var.get() + ";" + inputchannelnumber.get() + ";"
            messagebox.showinfo("INFO", "Make sure the filename and parameters are correct.\nYour filename is "+inputfilename.get()+".csv.\nYour parameter is "+parameter+".\nPlease click 'OK' to continue the process.\n Wait until the plot is shown.\n The file will be saved in " + parent_folder) 
    elif methodnumber == '2':
        if CheckVmin < -1.5 or CheckVmin > 1.5 :
            messagebox.showerror("ERROR", "Please Enter Vmin Value Between -1.5V - 1.5V")
        elif CheckVmax < -1.5 or CheckVmax > 1.5 :
            messagebox.showerror("ERROR", "Please Enter Vmax Value Between -1.5V - 1.5V")
        elif CheckScanRate < 10 or CheckScanRate > 120: 
            messagebox.showerror("ERROR", "Please Enter Scan Rate Value Between 10 - 120 mV/s")
        elif CheckIncrement < 1 or CheckIncrement > 250 :
            messagebox.showerror("ERROR", "Please Enter Vinc Value Between 1mV - 250mV")
        elif inputmethod.get() == "DPV" and (CheckAmp < 1 or CheckAmp > 250) :
            messagebox.showerror("ERROR", "Please Enter Vamp Value Between 1mV - 250mV")
        elif inputmethod.get() == 'DPV' and (CheckPulse < 0.4 or CheckPulse > 1)  :
            messagebox.showerror("ERROR", "Please Enter TPulse Value Between 0.4ms - 1s")
        else :
            parameter = inputmethod.get() + ";" + vmin_var.get() + ";" + vmax_var.get() + ";" + vincrem_var.get() + ";" + scanrate_var.get() + ";" + cycle_var.get() + ";" + sampling_var.get() + ";" + amp_var.get() + ";" + pulse_var.get() + ";" + inputchannelnumber.get() + ";"
            messagebox.showinfo("INFO", "Make sure the filename and parameters are correct.\nYour filename is "+inputfilename.get()+".csv.\nYour parameter is "+parameter+".\nPlease click 'OK' to continue the process.\n Wait until the plot is shown.\n The file will be saved in " + parent_folder) 

    file_name = inputfilename.get()+".csv"

    input_parameter = methodnumber+"|"+vmin_var.get()+"|"+vmax_var.get()+"|"+vincrem_var.get()+"|"+scanrate_var.get()+"|"+cycle_var.get()+"|"+sampling_var.get()+"|"+amp_var.get()+"|"+pulse_var.get()+"|"+inputchannelnumber.get()+"|"
    string1 = input_parameter
    string1_encode = string1.encode()

    ser = serial.Serial(port = 'COM3', baudrate = 115200, timeout = 5)
    ser.flushInput()
    ser.write(string1_encode)

    print(string1_encode)

    folder = os.path.join(path_file, file_name)

    #plt.ion()

    #Initialize data Arrays
    x = []
    y1 = []
    y2 = []

    #Set up the plot
    #fig, ax = plt.subplots()
    #ax.set_xlabel("Voltage(V)")
   # ax.set_ylabel("Current(µA)")
    #ax.set_title("Voltammogram")

    #Reading data from serial port
    #Retrieving data from Serial Communication
    while True :
        #Read a line from serial
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        #data = line.split(';')
        if (len(line) > 1) :
            with open(folder, 'a') as f:
                writer = csv.writer(f)  
                writer.writerow(line)
        else :
            break
        #Split the line into columns
        #data = line.split(";")

        #if data == "":
         #   break
        
        #Check total amount of columns in data
        #if len(data) == 2 : #1 Channel
            #Append Data to Arrays
        #    x.append(data[0])
        #    y1.append(data[1])

            #Plot the Data
        #    ax.plot(x, y1, 'r', label = 'Channel 1')
        #    ax.legend()

            #Draw the plot
        #    plt.draw()
        #    plt.pause(0.001)
        
       # elif len(data) == 3 : #2 Channel 
            #Append data to arrays
        #    x.append(data[0])
         #   y1.append(data[1])
          #  y2.append(data[2])

            #Plot the data
        #    ax.plot(x, y1, 'r', label = 'Channel 1')
        #    ax.plot(x, y2, 'g', label = 'Channel 2')
        #    ax.legend()

            #Draw The plot
        #    plt.draw()
        #    plt.pause(0.001)

        #Write Serial Data to CSV File
        #with open (folder, 'a', newline = "") as f:
         #   writer = csv.writer(f)
          #  writer.writerow(data)
    
    #Close the Serial Communication
    ser.close()
       
    #Reading File
    df = pd.read_csv(folder)

    #Read total amount of column
    total_column = len(df.axes[1])

    if total_column == 2 : #Plotting data for 1 channel only
        x = df[df.columns[0]]
        y1 = df[df.columns[1]]
            
        plt.plot(x, y1, color='red', label = 'Channel 1')
        plt.xlabel("Voltage(V)")
        plt.ylabel("Current(µA)")
        plt.title("Voltammogram")
        plt.axis([-1.5, 1.5, -600, 600])
        plt.grid('on')
        plt.show()

    elif total_column == 3 : #2 Channel Plotting Data
        x = df[df.columns[0]]
        y1 = df[df.columns[1]]
        y2 = df[df.columns[2]]


        #Subplot for Channel 1
        plt.subplot(211)
        plt.plot(x, y1, color='red', label = "Channel 1")
        plt.xlabel("Voltage(V)")
        plt.ylabel("Current(µA)")
        plt.axis([-1.5, 1.5, -600, 600])
        plt.grid('on')

        #Subplot for channel 2
        plt.subplot(212)
        plt.plot(x, y2, color = 'green', label = "Channel 2")
        plt.xlabel("Voltage(V)")
        plt.ylabel("Current(µA)")
        plt.axis([-1.5, 1.5, -600, 600])
        plt.grid('on')
    
        #Naming the main graph
        plt.suptitle("Voltammogram")   
        plt.show()

    else :
         messagebox.showerror("ERROR","ERROR")

#Reset Button Function
def ResetButton():
    vmin_var.set("0")
    VminEntry['state'] = tk.DISABLED
    vmax_var.set("0")
    VmaxEntry['state'] = tk.DISABLED
    vincrem_var.set("0")
    VincremEntry['state'] = tk.DISABLED
    scanrate_var.set("0")
    scanrateEntry['state'] = tk.DISABLED
    cycle_var.set("1")
    cycleEntry['state'] = tk.DISABLED
    sampling_var.set("10")
    samplingEntry['state'] = tk.DISABLED
    amp_var.set("0")
    ampEntry['state'] = tk.DISABLED
    pulse_var.set("0")
    pulseEntry['state'] = tk.DISABLED
    inputmethod.set("")
    inputfilename.set("")
    inputchannelnumber.set("")

#Function For Estimation Concentration




#Function for start button
#def PlotGraph():
   # csv_filename1 = 'testplot.csv'
   # csv_filename2 = 'testplot2.csv'

    #Array Variable for csv file 
    #x1 = []
    #y1 = []
    #x2 = []
    #y2 = []

    #Read CSV File for Channel 1
  #  with open(csv_filename1) as f1:
   #     reader1 = np.loadtxt(csv_filename1, delimiter=";")
    #    for row in reader1 :
     #       x1.append(float(row[0]))
      #      y1.append(float(row[1]))

    #Read CSV File for Channel 2
    #with open(csv_filename2) as f2:
     ##  for row in reader2 :
       #     x2.append(float(row[0]))
        #    y2.append(float(row[1]))
    
    #Plotting both plot simualtenously

    #Subplot for channel 1
    #plt.subplot(211)
    #plt.scatter(x1, y1, linewidth= 0.05, color='red', label = "Channel 1")
    #plt.xlabel("Voltage(mV)")
    #plt.ylabel("Current(µA)")
    #plt.axis([-1.5, 1.5, -600, 600])
    #plt.grid()

    #Subplot for channel 2
    #plt.subplot(212)
    #plt.scatter(x2, y2, linewidth = 0.05, color = 'green', label = "Channel 2")
    #plt.xlabel("Voltage(mV)")
    #plt.ylabel("Current(µA)")
    #plt.axis([-1.5, 1.5, -600, 600])
    #plt.grid()
    
    #Naming the main graph
    #plt.suptitle("Voltammogram")   
    #plt.show()


#Progressbar Function
#def update_progress_label():
    #return f"Current Progress : {pb['value']}%"

def progress():
    if pb['value'] < 100:
        pb['value'] += 20
        value_label['text'] = update_progress_label()
    else:
        showinfo(message = 'The Progress Completed')

def stop() :
    pb.stop()
    value_label['text'] = update_progress_label()


def metode() :
    if (inputmethod.get() == "CV"):
        VminEntry['state'] = tk.NORMAL
        VmaxEntry['state'] = tk.NORMAL
        scanrateEntry['state'] = tk.NORMAL
        cycleEntry['state'] = tk.NORMAL

    else : #method == DPV
        VminEntry['state'] = tk.NORMAL
        VmaxEntry['state'] = tk.NORMAL
        scanrateEntry['state'] = tk.NORMAL
        cycleEntry['state'] = tk.NORMAL
        VincremEntry['state'] = tk.NORMAL
        samplingEntry['state'] = tk.NORMAL
        ampEntry['state'] = tk.NORMAL
        pulseEntry['state'] = tk.NORMAL
        cycle_var.set("1")
        sampling_var.set("10")

###################### APP WIDGET ######################

#App window 
window.geometry("950x450")
window.title("Potensiostat")
window.resizable(False, False)

#Column 1
method = tk.Label(window, text = "Method") #Edit
method.grid(column = 0  , row = 2)

#Combobox for method dropdown button 
inputmethod = tk.StringVar()
method_choosen = ttk.Combobox(window, width = 22, textvariable = inputmethod)
method_choosen['values'] = ('CV', 'DPV')
inputmethod.set("")


Filename = tk.Label(text = "File Name").grid(column = 0, row = 1) #EditF
Vmin = tk.Label(text = "Vmin(V) [Value between -1.5V - 1.5V]").grid(column = 0, row = 4)
Vmax = tk.Label(text = "Vmax(V) [Value between -1.5V - 1.5V]").grid(column = 0, row = 5)
Cycle = tk.Label(text = "Cycle").grid(column = 0, row = 6)
Scanrate = tk.Label(text = "Scan Rate(mV/s) [Value between 10-120]").grid(column = 0, row = 7)

ttk.Label(window, text = "Click Input Parameter Button Before Enter Value").grid(column = 0 , row  = 3)

method_button = tk.Button(window, text = "Input Parameter", command = metode)
method_button.grid(column = 1, row = 3)
#Method Button

#Column 2
#Num of channel
Channel_number = tk.Label(window, text = "Num. of Channel").grid(column = 8 , row = 1)

#Combobox for num. of channel dropdown button
inputchannelnumber = tk.StringVar()
Channelnumber_choosen = ttk.Combobox(window, width = 22, textvariable = inputchannelnumber)
Channelnumber_choosen['values'] = ('1', '2')
inputchannelnumber.set("")

#Text
TextArea = tk.Label(text = "Additional Parameter For DPV Method: ").grid(column = 8, row = 2)

#Additional Parameter For DPV Method
Vincrem = tk.Label(text = "Vinc(mV) [Value between 1mV - 250mV]").grid(column = 8, row = 3) #Edit
Amp = tk.Label(text = "Vamp(mV) [Value between 1mV - 250mV]").grid(column = 8, row = 4)
Sampling = tk.Label(text = "Tsampling(ms)").grid(column = 8, row = 5)
Pulse = tk.Label(text = "TPulse(ms) [Value between 0.4ms to 1s]").grid(column = 8, row = 6)

#Input column

#Declaration of Tkinter variables
inputfilename  = tk.StringVar()
vmin_var = tk.StringVar()
vmax_var = tk.StringVar()
vincrem_var = tk.StringVar()
scanrate_var = tk.StringVar()
cycle_var = tk.StringVar()
sampling_var = tk.StringVar()
amp_var = tk.StringVar()
pulse_var = tk.StringVar()

method_choosen.grid(column = 1, row = 2)
method_choosen.current()

filenameEntry = tk.Entry(window, textvariable = inputfilename, width = 25)
filenameEntry.grid(column = 1, row = 1) 

VminEntry = tk.Entry(window, textvariable = vmin_var, width = 25)
VminEntry.grid(column = 1, row = 4)
vmin_var.set("0")
VminEntry['state'] = tk.DISABLED

VmaxEntry = tk.Entry(textvariable = vmax_var, width = 25)
VmaxEntry.grid(column = 1, row = 5)
vmax_var.set("0")
VmaxEntry['state'] = tk.DISABLED

cycleEntry = tk.Entry(textvariable = cycle_var, width = 25)
cycleEntry.grid(column = 1, row = 6 )
cycle_var.set("1")
cycleEntry['state'] = tk.DISABLED

scanrateEntry = tk.Entry(textvariable = scanrate_var, width = 25)
scanrateEntry.grid(column = 1, row = 7)
scanrate_var.set("0")
scanrateEntry['state'] = tk.DISABLED

Channelnumber_choosen.grid(column = 10, row = 1)
Channelnumber_choosen.current()

VincremEntry = tk.Entry(textvariable = vincrem_var, width = 25)
VincremEntry.grid(column = 10, row = 3)
vincrem_var.set("0")
VincremEntry['state'] = tk.DISABLED

ampEntry = tk.Entry(textvariable = amp_var, width = 25)
ampEntry.grid(column = 10, row = 4)
amp_var.set("0")
ampEntry['state'] = tk.DISABLED

samplingEntry = tk.Entry (textvariable = sampling_var, width = 25)
samplingEntry.grid(column = 10, row = 5)
sampling_var.set("10")
samplingEntry['state'] = tk.DISABLED

pulseEntry = tk.Entry(textvariable = pulse_var, width = 25)
pulseEntry.grid(column = 10, row = 6)
pulse_var.set("0")
pulseEntry['state'] = tk.DISABLED

#Draw a Line in GUI

#Estimation Concentration Label
result1_var = tk.DoubleVar()
result2_var = tk.DoubleVar()

#Result1 = tk.Label(text = "The Concentration in Channel 1 : ").grid(column = 0 , row = 10 )
#result1 = tk.Entry(textvariable = result1_var, width = 35)
#result1.grid(row = 2, column = )
#Result2 = tk.Label(text = "The Concentration in Channel 2 : ").grid(column = 0, row = 12)
#result2 = tk.Entry(textvariable = result2_var, width  = 35)
#esult2.grid(row = 2, column = 12)

#Start and Reset Button
start = tk.Button(window, text = "Start", width = 15, command = StartButton)
start.grid(column = 1, row = 20)
reset  = tk.Button(window, text = "Reset", width = 15, command = ResetButton)
reset.grid(column = 10, row = 20 )

#Label Text 
ttk.Label(window, text = "Press Reset", font = ("Sherif", 10)).grid(column = 8, row = 30)
ttk.Label(window, text = "every time you change the measurement method and finish measuring", font = ("Sherif", 8)).grid(column = 8, row = 40)

#Progressbar
#pb = ttk.Progressbar(window, orien = 'horizontal', mode = 'determinate', length = 400)
#pb.grid(column = 10, row = 10, columnspan = 2, padx = 10, pady = 20)


window.mainloop()