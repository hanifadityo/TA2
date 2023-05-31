import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
import os.path
import serial
from serial import Serial
import scipy.signal as signal
import math
import serial.tools.list_ports
import screeninfo

    

#Progress bar 
class ProgressBar :
    def __init__(self, master, maximum) :
        self.master = master
        self.maximum = maximum
        self.progressbar = ctk.CTkProgressBar(master, mode = "determinate", width=400, height= 20, border_color = "dark_color")
        self.progressbar.grid(column = 8, row = 9, padx = 10, pady = 10)
        self.count = 0

    def update(self) :
        self.count += 1
        if self.count <= self.maximum:
            self.progressbar['value'] = self.count
        else :
            self.progressbar['value'] = self.maximum
        self.master.update_idletasks()

    def reset_progressbar(self) :
        self.count = 0
        self.progressbar['value'] = 0
        self.master.update_idletasks()

def plot_graph(x, y1, y2, axis_min, axis_max, min_current1, max_current1, min_current2, max_current2, use_subplots = False):
    fig = Figure(figsize = (6,4), dpi = 100)
    if use_subplots:
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        ax1.plot(x, y1, color = 'red')
        ax2.plot(x, y2, color = 'green')

        ax1.set_xlabel("Voltage (V)")
        ax1.set_ylabel("Current (µA)")
        ax1.set_title("Channel 1")
        ax1.axis([axis_min, axis_max, min_current1, max_current1])
        ax1.grid('on')

        ax2.set_xlabel("Voltage (V)")
        ax2.set_ylabel("Current (µA)")
        ax2.set_title("Channel 2")
        ax2.axis([axis_min, axis_max, min_current2, max_current2])
        ax2.grid('on')
    
    else : #1 channel 
        ax = fig.add_subplot(111)
        ax.plot(x, y1, color = 'red')
        ax.set_xlabel("Voltage (V)")
        ax.set_ylabel("Current (µA)")
        ax.set_title("Voltammogram")
        ax.axis([axis_min, axis_max, min_current1, max_current1])
        ax.grid('on')
    
    canvas = FigureCanvasTkAgg(fig, master = master)
    canvas.draw()
    canvas.get_tk_widget().grid(column = 8, row = 11, padx =10, pady = 10)

#Start Button Function
def StartButton():
    #parent_folder = "D:\TA2"
    parent_folder = "C:"
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

    #Validate if Input is empty
    if methodnumber == "" or vmin_var.get() == "" or vmax_var.get() == "" or scanrate_var.get() =="" or cycle_var.get() == "" or inputchannelnumber.get() == "" or ion1.get() == "" or ion2.get() == "" or amp_var.get() == "" or vincrem_var.get() == "" or pulse_var.get() == "" or sampling_var.get() == "" or inputfilename.get() =="":
        messagebox.showerror("ERROR", "Please Enter All Value of Input Parameter")
    else :
        #Validate user input (CV Parameter)
        if methodnumber == '1':
            #Variable to check user input
            #return True if all user input is valid
            valid = False
            try : 
                #Define Variable to Validate Value of Input Parameter
                CheckVmin = float(vmin_var.get())
                CheckVmax = float(vmax_var.get())
                CheckScanRate = int(scanrate_var.get())
                CheckCycle = int(cycle_var.get())

                #Validate the range of each parameter input
                if CheckVmin < -1.5 or CheckVmin > 1.5 :
                    messagebox.showerror("ERROR", "Please Enter Vmin Value Between -1.5V - 1.5V")
                elif CheckVmax < -1.5 or CheckVmax > 1.5 :
                    messagebox.showerror("ERROR", "Please Enter Vmax Value Between -1.5V - 1.5V")
                elif CheckVmax == CheckVmin :
                    messagebox.showerror("ERROR", "Vmax and Vmin Must Be a Different Value")
                elif CheckScanRate < 10 or CheckScanRate > 120:
                    messagebox.showerror("ERROR", "Please Enter Scan Rate Value Between 10 - 120 mV/s")
                elif CheckCycle <= 0 : 
                    messagebox.showerror("ERROR", "Please Enter Cycle Value Greater Than 0")
                elif CheckCycle > 255 :
                    messagebox.showerror("ERROR", "Cycle Value is Too Big")
                else :
                    valid = True    #All user input is valid
            except ValueError : #Return error if not a number
                messagebox.showerror("ERROR", "Parameter must be a number")
    
        #Validate user input (DPV Parameter)
        elif methodnumber == '2':
            #Variable to check user input
            #Return True if all user input is valid
            valid = False
            try :
                #Define Variable to Validate Value of Input Parameter
                CheckVmin = float(vmin_var.get())
                CheckVmax = float(vmax_var.get())
                CheckScanRate = int(scanrate_var.get())
                CheckIncrement = float(vincrem_var.get())
                CheckAmp = float(amp_var.get())
                CheckPulse = float(pulse_var.get())
                CheckSampling = float(sampling_var.get())
                
                #Validate the range of each parameter input
                if CheckVmin < -1.5 or CheckVmin > 1.5 :
                    messagebox.showerror("ERROR", "Please Enter Vmin Value Between -1.5V - 1.5V")
                elif CheckVmax < -1.5 or CheckVmax > 1.5 :
                    messagebox.showerror("ERROR", "Please Enter Vmax Value Between -1.5V - 1.5V")
                elif CheckVmax == CheckVmin :
                    messagebox.showerror("ERROR", "Vmax and Vmin Must Be a Different Value")
                elif CheckScanRate < 10 or CheckScanRate > 120: 
                    messagebox.showerror("ERROR", "Please Enter Scan Rate Value Between 10 - 120 mV/s")
                elif CheckIncrement < 0.001 or CheckIncrement > 0.25 :
                    messagebox.showerror("ERROR", "Please Enter Vinc Value Between 0.001 - 0.25 V")
                elif CheckAmp < 0.001 or CheckAmp > 0.25 :
                    messagebox.showerror("ERROR", "Please Enter Vamp Value Between 0.001 - 0.25 V")
                elif CheckPulse < 0.4 or CheckPulse > 1000 :
                    messagebox.showerror("ERROR", "Please Enter TPulse Value Between 0.4ms - 1000 ms")
                elif CheckPulse >= ((CheckIncrement/CheckScanRate) * 1000000) / 2  :
                    messagebox.showerror("ERROR", "TPulse Value is Too Big")
                elif CheckSampling <= 0 :
                    messagebox.showerror("ERROR", "Please Enter Tsampling Greater Than 0")
                else :
                    valid = True    #All user input is valid
            except ValueError :
                messagebox.showerror("ERROR", "Parameter must be a number")
        
        valid2 = False
        #Validate Ion Type in channel 2 if using only 1 channel
        if inputchannelnumber.get() == '1' and ion2.get() != "None" :
            messagebox.showerror("ERROR", "Please Set 'Ion Sample Type for Channel 2' to None")
        # Validate ion type in channel 2 if using all channels
        elif inputchannelnumber.get() == '2' and ion2.get() == 'None' :
            messagebox.showerror("ERROR", "Please Set 'Ion Sample Type for Channel 2' to K or Na")
        else :
            valid2 = True

        #All user parameter input is valid
        if valid == True and valid2 == True :
            parameter = inputmethod.get() + "|" + vmin_var.get() + "|" + vmax_var.get() +  "|" + scanrate_var.get() + "|" + cycle_var.get() + "|" + inputchannelnumber.get() + "|" + ion1.get() + "|" + ion2.get() + "|" + vincrem_var.get() + "|" + amp_var.get() + "|" + sampling_var.get() + "|" + pulse_var.get() 
            messagebox.showinfo("INFO", "Make sure the filename and parameters are correct.\nYour filename is "+inputfilename.get()+".csv.\nYour parameter is "+parameter+".\nPlease click 'OK' to continue the process.\n Wait until the plot is shown.\n The file will be saved in " + parent_folder) 
        
            file_name = inputfilename.get()+".csv"

            input_parameter = methodnumber+"|"+vmin_var.get()+"|"+vmax_var.get()+"|"+vincrem_var.get()+"|"+scanrate_var.get()+"|"+cycle_var.get()+"|"+sampling_var.get()+"|"+amp_var.get()+"|"+pulse_var.get()+"|"+inputchannelnumber.get()+"|"
            string1 = input_parameter
            string1_encode = string1.encode() 

            #Save data in folder
            folder = os.path.join(path_file, file_name)
        
            #Find an available serial port
            ser = None  #Define ser variable 

            #Get a list of all available ports
            ports = serial.tools.list_ports.comports()

            #try : 
            for port in ports :
                try :
                    ser = serial.Serial(port = port.device, baudrate = 115200)
                    ser.parity = serial.PARITY_NONE
                    ser.bytesize = serial.EIGHTBITS
                    ser.stopbits = serial.STOPBITS_ONE
                    break
                except :
                    pass
            else :
                messagebox.showerror("ERROR", "Could not connect to any ports")
    
            if ser is not None :
                #clear the input buffer / Flush the input buffer
                ser.flushInput()

                #Write data to ESP32
                ser.write(string1_encode)

                #Open the CSV file for writing
                with open(folder, 'a', newline="") as f :
                    writer = csv.writer(f, delimiter = ";")
                    writer.writerow(["Voltage", "Current_1", "Current_2"])  #Write header in csv file for the first row
            
                    #Reading data from serial port
                    #Retrieving data from Serial Communication
                    while True :
                        #Read a line from serial
                        line = ser.readline().decode('latin-1').strip()
                        print(line)
                        
                        #Break out of the loop if read serial data "999999999"
                        if line == "999999999" :
                            break
            
                        data = line.split(';')

                        if len(data) == 2 :
                            writer.writerow([data[0], data[1]])

                        elif len(data) == 3 :
                            writer.writerow([data[0], data[1], data[2]])
                    
                        progress_bar.update()

                        #if progress_bar.count >= max_rows :
                            #break

                #Close the serial plot
                ser.close()

            #except IndexError or UnicodeDecodeError or serial.serialutil.SerialException :
                #messagebox.showerror("ERROR", "Something went wrong. Please, Try again")
            
                #Reading the data from CSV File and Plot it
                with open(folder, 'r') as f :
                    reader = csv.reader(f, delimiter = ";")
                    next(reader)    #Skip the header row

                    #Define variable of array
                    x = []
                    y1 = []
                    y2 = []
                    n_cycle = int(cycle_var.get())
                    axis_min = float(vmin_var.get())
                    axis_max = float(vmax_var.get())

                    for row in reader :
                        if len(row) == 3 :
                            x.append(float(row[0]))
                            y1.append(float(row[1]))
                            y2.append(float(row[2]))

                        elif len(row) == 2 :
                            x.append(float(row[0]))
                            y1.append(float(row[1]))

                    #Check number of channel that being used
                    if len(y1) > 0 and len(y2) == 0 :   #1 Channel only
                        #Find maximum value in desired range
                        LowerRange1 = math.floor((n_cycle - 1)/n_cycle * len(y1))   #Lower Range of index
                        UpperRange1 = len(y1) + 1   #Upper range of index

                        #Slice the array
                        values_in_range1 = y1[LowerRange1:UpperRange1] 

                        #Find the maximum value in specified range
                        slope1 = max(values_in_range1)

                        max_current1 = max(y1)  #Finding the maximum value of current in channel 1
                        min_current1 = min(y1)  #Findign the minimum value of current in channel 1

                        K_Concentration1 =  81.3888 + 0.267 * slope1    #Concentration Estimation of K
                        K_Concentration1 = round(K_Concentration1, 4)   #Round the number to 4 decimal places

                        Na_Concentration1 = 277.3594 + 0.913 * slope1   #Concentration Estimation of Na
                        Na_Concentration1 = round(Na_Concentration1, 4) #Round the number to 4 decimal places
        
                        #Calulate Concentration
                        if ion1.get() == "K" and ion2.get() == "None" :      
                            result1.insert(0, K_Concentration1)
                        elif ion1.get() == "Na" and ion2.get() == "None":
                            result1.insert(0, Na_Concentration1)

                        #Plotting the Data from CSV
                        plot_graph(x, y1, y2, axis_min, axis_max, min_current1, max_current1)

                        messagebox.showinfo("SUCCESS", "Measurement Completed!")

                    elif len(y1) > 0 and len(y2) > 0 :    #Using 2 channel
                        #Find maximum value in desired range
                        LowerRange1 = math.floor((n_cycle - 1)/n_cycle * len(y1))   #Lower range of index in channel 1
                        LowerRange2 = math.floor((n_cycle - 1)/n_cycle * len(y2))   #Lower range of index in channel 2
                        UpperRange1 = len(y1) + 1                       #Upper range of index in channel 1 
                        UpperRange2 = len(y2) + 1                       #Upper range of index in channel 2

                        #Slicing the array
                        values_in_range1 = y1[LowerRange1:UpperRange1]
                        values_in_range2 = y2[LowerRange2:UpperRange2]

                        #Finding the maximum value in specified range
                        slope1 = max(values_in_range1)
                        slope2 = max(values_in_range2)

                        max_current1 = max(y1)  #Finding the maximum value of current in Channel 1
                        max_current2 = max(y2)  #Finding the maximum value of current in channel 2
                        min_current1 = min(y1)  #Finding the minimum value of current in channel 1
                        min_current2 = min(y2)  #Finding the minimum value of current in channel 2
                
                        #Calculate the concentration of ion
                        K_Concentration1 = 81.3888 + 0.267 * slope1   #Concentration Estimation of K in Channel 1
                        K_Concentration1 = round(K_Concentration1, 4)   #Round the number to 4 decimal places

                        K_Concentration2 = 81.3888 + 0.267 * slope2  #Concentration Estimation of K in Channel 2
                        K_Concentration2 = round(K_Concentration2, 4)   #Round the number to 4 decimal places

                        Na_Concentration1 = 277.3594 + 0.913 * slope1   #Concentration Estimation of Na in Channel 1
                        Na_Concentration1 = round(Na_Concentration1, 4)

                        Na_Concentration2 = 277.3594 + 0.913 * slope2   #Concentration Estimation of Na in Channel 2
                        Na_Concentration2 = round(Na_Concentration2, 4)

                        #Calculate Concentration
                        if ion1.get() == "K" and ion2.get() == "K":
                            result1.insert(0, K_Concentration1)
                            result2.insert(0, K_Concentration2)
                        elif ion1.get() == "Na" and ion2.get() == "Na" :
                            result1.insert(0, Na_Concentration1)
                            result2.insert(0, Na_Concentration2)
                        elif ion1.get() == "K" and ion2.get() == "Na" :
                            result1.insert(0, K_Concentration1)
                            result2.insert(0, Na_Concentration2)
                        elif ion1.get() == "Na" and ion2.get() == "K" :
                            result1.insert(0, Na_Concentration1)
                            result2.insert(0, K_Concentration2)
                        
                        plot_graph(x, y1, y2, axis_min, axis_max, min_current1, max_current1, min_current2, max_current2, use_subplots = True)

                        messagebox.showinfo("SUCCESS", "Measurement Completed!")

                    else :
                        messagebox.showerror("ERROR", "ERROR")

#Reset Button Function
def ResetButton():
    vmin_var.set("0.0")
    VminEntry.configure(state = "disabled")
    vmax_var.set("0.0")
    VmaxEntry.configure(state = "disabled")
    vincrem_var.set("0.0")
    VincremEntry.configure(state = "disabled")
    scanrate_var.set("0")
    scanrateEntry.configure(state = "disabled")
    cycle_var.set("1")
    cycleEntry.configure(state = "disabled")
    sampling_var.set("10")
    samplingEntry.configure(state = "disabled")
    amp_var.set("0.0")
    ampEntry.configure(state = "disabled")
    pulse_var.set("0.0")
    pulseEntry.configure(state = "disabled")
    inputmethod.set("")
    inputfilename.set("")
    inputchannelnumber.set("")
    ion1.set("")
    ion2.set("")
    result1_var.set("")
    result2_var.set("")
    progress_bar.reset_progressbar()

#Function for disabling paramter input based on method being choosen by user
def metode() :
    if (inputmethod.get() == "CV"):
        VminEntry.configure(state = "normal")
        VmaxEntry.configure(state = "normal")
        scanrateEntry.configure(state = "normal")
        cycleEntry.configure(state = "normal")

    else : #method == DPV
        VminEntry.configure(state = "normal")
        VmaxEntry.configure(state = "normal")
        scanrateEntry.configure(state = "normal")
        VincremEntry.configure(state = "normal")
        samplingEntry.configure(state = "normal")
        ampEntry.configure(state = "normal")
        pulseEntry.configure(state = "normal")
        cycle_var.set("1")
        sampling_var.set("10")

###################### APP WIDGET ######################

#App window 
master = ctk.CTk()
master.title("PSDual")
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue") 

#Set the window size
#screen_width = master.winfo_screenwidth()
#screen_height = master.winfo_screenheight()
#master.geometry(f"{screen_width}x{screen_height}")
#master.geometry("700x450")
appWidth, appHeight = 1000, 450
#window.resizable(False, False)

#add icon logo
icon = tk.PhotoImage(file = 'logo.png')
master.iconphoto(False, icon)

#Column 1
method = ctk.CTkLabel(master, text = "Method") 
method.grid(column = 0  , row = 3)
#Input Parameter Button
method_button = ctk.CTkButton(master, text = "Input Parameter", command = metode, width = 100)
method_button.grid(column = 1, row = 4)

#Combobox for method dropdown button 
inputmethod = tk.StringVar()
method_choosen = ctk.CTkComboBox(master, width = 100, variable = inputmethod, values = ["CV", "DPV"])
inputmethod.set("")
method_choosen.grid(column = 1, row =3)

#Combobox for num. of channel dropdown button
Channel_number = ctk.CTkLabel(master, text = "Number of Channel").grid(column = 0 , row = 2)
inputchannelnumber = tk.StringVar()
Channelnumber_choosen = ctk.CTkComboBox(master, width = 100, variable = inputchannelnumber, values = ['1', '2'])
inputchannelnumber.set("")
Channelnumber_choosen.grid(column = 1, row = 2)


Filename = ctk.CTkLabel(master, text = "File Name").grid(column = 0, row = 1) #EditF
Vmin = ctk.CTkLabel(master, text = "Vmin(V) [Value between -1.5V - 1.5V]").grid(column = 0, row = 5)
Vmax = ctk.CTkLabel(master, text = "Vmax(V) [Value between -1.5V - 1.5V]").grid(column = 0, row = 6)
Cycle = ctk.CTkLabel(master, text = "Cycle [Value between 0 - 255]").grid(column = 0, row = 7)
Scanrate = ctk.CTkLabel(master, text = "Scan Rate(mV/s) [Value between 10-120]").grid(column = 0, row = 8)

#Text for Input Parameter Button
ctk.CTkLabel(master, text = "Click Input Parameter Button Before Enter Value").grid(column = 0 , row  = 4)


#Column 2
#Combobox for Ion Sample Type in Channel 1
Ion_sample1 = ctk.CTkLabel(master, text = "Ion Sample Type for Channel 1").grid(column = 8, row = 1)
ion1 = tk.StringVar()
ion_choosen1 = ctk.CTkComboBox(master, width = 100, variable = ion1, values = ['Na', 'K'])
ion_choosen1.grid(column = 10, row = 1)
ion1.set("")

#Combobox for Ion Sample Type in Channel 2
Ion_sample2 = ctk.CTkLabel(master, text = "Ion Sample Type for Channel 2").grid(column = 8, row = 2)
ion2 = tk.StringVar()
ion_choosen2 = ctk.CTkComboBox(master, width = 100, variable = ion2, values = ['Na','K','None'])
ion_choosen2.grid(column = 10, row = 2)
ion2.set("")

#Text
TextArea = ctk.CTkLabel(master, text = "Additional Parameter For DPV Method: ").grid(column = 8, row = 3)

#Additional Parameter For DPV Method
Vincrem = ctk.CTkLabel(master, text = "Vinc(V) [Value between 0.001V - 0.25V]").grid(column = 8, row = 4) #Edit
Amp = ctk.CTkLabel(master, text = "Vamp(V) [Value between 0.001V - 0.25V]").grid(column = 8, row = 5)
Sampling = ctk.CTkLabel(master, text = "Tsampling(ms)").grid(column = 8, row = 6)
Pulse = ctk.CTkLabel(master, text = "TPulse(ms) [Value between 0.4ms to 1000ms]").grid(column = 8, row = 7)

#Input column

#Declaration of Tkinter variables
inputfilename  = ctk.StringVar()
vmin_var = ctk.StringVar()
vmax_var = ctk.StringVar()
vincrem_var = ctk.StringVar()
scanrate_var = ctk.StringVar()
cycle_var = ctk.StringVar()
sampling_var = ctk.StringVar()
amp_var = ctk.StringVar()
pulse_var = ctk.StringVar()



filenameEntry = ctk.CTkEntry(master, textvariable = inputfilename, width = 100)
filenameEntry.grid(column = 1, row = 1) 

VminEntry = ctk.CTkEntry(master, textvariable = vmin_var, width = 100)
VminEntry.grid(column = 1, row = 5)
vmin_var.set("0.0")
VminEntry.configure(state = "disabled")

VmaxEntry = ctk.CTkEntry(master, textvariable = vmax_var, width = 100)
VmaxEntry.grid(column = 1, row = 6)
vmax_var.set("0.0")
VmaxEntry.configure(state = "disabled")

cycleEntry = ctk.CTkEntry(master, textvariable = cycle_var, width = 100)
cycleEntry.grid(column = 1, row = 7)
cycle_var.set("1")
cycleEntry.configure(state = "disabled")

scanrateEntry = ctk.CTkEntry(master, textvariable = scanrate_var, width = 100)
scanrateEntry.grid(column = 1, row = 8)
scanrate_var.set("0")
scanrateEntry.configure(state = "disabled")

VincremEntry = ctk.CTkEntry(master, textvariable = vincrem_var, width = 100)
VincremEntry.grid(column = 10, row = 4)
vincrem_var.set("0.0")
VincremEntry.configure(state = "disabled")

ampEntry = ctk.CTkEntry(master, textvariable = amp_var, width = 100)
ampEntry.grid(column = 10, row = 5)
amp_var.set("0.0")
ampEntry.configure(state = "disabled")

samplingEntry = ctk.CTkEntry (master, textvariable = sampling_var, width = 100)
samplingEntry.grid(column = 10, row = 6)
sampling_var.set("10")
samplingEntry.configure(state = "disabled")

pulseEntry = ctk.CTkEntry(master, textvariable = pulse_var, width = 100)
pulseEntry.grid(column = 10, row = 7)
pulse_var.set("0.0")
pulseEntry.configure(state = "disabled")

#Estimation Concentration Label
result1_var = tk.StringVar()
result2_var = tk.StringVar()

ctk.CTkLabel(master, text = "Concentration Of Samples", font = ("Sherif", 24), fg_color = "transparent").grid(column = 8, row = 10)
Result1 = ctk.CTkLabel(master, text = "Concentration in Channel 1 (mM): ").grid(column = 0 , row = 20)
result1 = ctk.CTkEntry(master, textvariable = result1_var, width = 100)
result1.grid(row = 20, column = 1)

Result2 = ctk.CTkLabel(master, text = "Concentration in Channel 2 (mM): ").grid(column = 8, row = 20)
result2 = ctk.CTkEntry(master, textvariable = result2_var, width  = 100)
result2.grid(row = 20, column = 10)

#Start and Reset Button
start = ctk.CTkButton(master, text = "Start", width = 100, command = StartButton)
start.grid(column = 1, row = 35)
reset  = ctk.CTkButton(master, text = "Reset", width = 100, command = ResetButton)
reset.grid(column = 10, row = 35)

#Label Text 
ctk.CTkLabel(master, text = "Press Reset", font = ("Sherif", 18)).grid(column = 8, row = 40)
ctk.CTkLabel(master, text = "every time you change the measurement method and finish measuring", font = ("Sherif", 16)).grid(column = 8, row = 50)

#Progressbar
max_rows = 10000
progress_bar = ProgressBar(master, max_rows)

master.mainloop()