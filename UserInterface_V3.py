import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os.path
import serial
from serial import Serial
import scipy.signal as signal
import math
import serial.tools.list_ports
    

#Progress bar 
class ProgressBar :
    def __init__(self, master, maximum) :
        self.master = master
        self.maximum = maximum
        self.progressbar = tk.ttk.Progressbar(master, maximum = maximum, length = 400)
        self.progressbar.grid(column = 8, row = 9)
        self.count = 0

    def update(self) :
        self.count += 1
        self.progressbar['value'] = self.count
        self.master.update_idletasks()

    def reset_progressbar(self) :
        self.count = 0
        self.progressbar['value'] = 0
        self.master.update_idletasks()

#Start Button Function
def StartButton():
    #parent_folder = "D:\TA2"
    parent_folder = "C:"
    save = parent_folder+"/PS Dual"
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

    progress_bar.update()

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
                elif CheckCycle < 2 or CheckCycle > 255 :
                    messagebox.showerror("ERROR", "Please Enter Cycle Value Between 2 - 255")
                else :
                    valid = True    #All user input is valid
            except ValueError : #Return error if not a number
                messagebox.showerror("ERROR", "Parameter must be a number")

            valid2 = False
            #Validate Ion Type in channel 2 if using only 1 channel
            if inputchannelnumber.get() == '1' and ion2.get() != "None":
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

                input_parameter = methodnumber+"|"+vmin_var.get()+"|"+vmax_var.get()+"|"+vincrem_var.get()+"|"+scanrate_var.get()+"|"+cycle_var.get()+"|"+sampling_var.get()+"|"+amp_var.get()+"|"+pulse_var.get()+"|"+inputchannelnumber.get()+ "|" + ion1.get() + "|" + ion2.get()
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
                                #  break

                    #Close the serial plot
                    ser.close()

                #except IndexError or UnicodeDecodeError or serial.serialutil.SerialException :
                    #messagebox.showerror("ERROR", "Something went wrong. Please, Try again")
            
                    #Reading the data from CSV File and Plot it
                    with open(folder, 'r') as f :
                        reader = csv.reader(f, delimiter = ";")
                        next(reader)    #Skip the header row
                        #reader2 = next(reader1)

                        #Define variable of array
                        x = []
                        y1 = []
                        y2 = []
                        axis_min = float(vmin_var.get())
                        axis_max = float(vmax_var.get())
                        
                
                        for row in reader:
                            if len(row) == 3 :
                                x.append(float(row[0]))
                                y1.append(float(row[1]))
                                y2.append(float(row[2]))
                            elif len(row) == 2 :
                                x.append(float(row[0]))
                                y1.append(float(row[1]))
                        
                        #Check number of channel that being used
                        if len(y1) > 0 and len(y2) == 0 :   #1 Channel only
                            UpperRange1 = len(y1) + 1

                            #slice the array for CV
                            
                            values_in_range_CV = y1[5413:UpperRange1]
                            CV_max_current1 = max(values_in_range_CV)
                            CV_min_current1 = min(values_in_range_CV)
                            FeCN_Concentration1 = 0.21372 * CV_max_current1 + 0.737816 
                            FeCN_Concentration1 = round(FeCN_Concentration1, 4)

                            messagebox.showinfo("SUCCESS", "Measurement Completed!")

                            #Show Concentration
                            if ion1.get() == 'FeCN' and ion2.get() == 'None':
                                result1.insert(0, FeCN_Concentration1)

                        
                            filtered_x = [value for index, value in enumerate(x) if index > 5413]
                            filtered_y1 = [value for index, value in enumerate(y1) if index > 5413]
                            #Plotting the Data from CSV
                            plt.plot(filtered_x, filtered_y1, color = 'red')
                            plt.xlabel("Voltage(V)")
                            plt.ylabel("Current(µA)")
                            plt.title("Voltammogram")
                            plt.axis([axis_min, axis_max, CV_min_current1, CV_max_current1])
                            plt.grid('on')
                            plt.show()
                            
                        elif len(y1) > 0 and len(y2) > 0 :    #Using 2 channel
                            #Find maximum value in desired range
                            UpperRange1 = len(y1) + 1                       #Upper range of index in channel 1 
                            UpperRange2 = len(y2) + 1                       #Upper range of index in channel 2

                            #Slicing array for CV
                            values_in_range_CV_1 = y1[5413:UpperRange1]
                            values_in_range_CV_2 = y2[5413:UpperRange2]
                            CV_max_current1 = max(values_in_range_CV_1)
                            CV_max_current2 = max(values_in_range_CV_2)
                            CV_min_current1 = min(values_in_range_CV_1)
                            CV_min_current2 = min(values_in_range_CV_2)
                            FeCN_Concentration1 = 0.21372 * CV_max_current1 + 0.737816
                            FeCN_Concentration2 = 0.21372 * CV_max_current2 + 0.737816

                            messagebox.showinfo("SUCCESS", "Measurement Completed!")

                            if ion1.get() == "FeCN" and ion2.get() == "FeCN":
                                result1.insert(0, FeCN_Concentration1)
                                result2.insert(0, FeCN_Concentration2)
                                
                        
                            filtered_x = [value for index, value in enumerate(x) if index > 5413]
                            filtered_y1 = [value for index, value in enumerate(y1) if index > 5413]
                            filtered_y2 = [value for index, value in enumerate(y2) if index > 5413]

                            #Subplot for Channel 1  
                            plt.subplot(211)
                            plt.plot(filtered_x, filtered_y1, color= 'red')
                            plt.subplot(211).set_title("Channel 1")
                            plt.xlabel("Voltage(V)")
                            plt.ylabel("Current(µA)")
                            plt.axis([axis_min, axis_max, CV_min_current1, CV_max_current1])
                            plt.grid('on')

                            #Subplot for channel 2
                            plt.subplot(212)
                            plt.plot(filtered_x, filtered_y2, color = 'green')
                            plt.xlabel("Voltage(V)")
                            plt.ylabel("Current(µA)")
                            plt.axis([axis_min, axis_max, CV_min_current2, CV_max_current2])
                            plt.grid('on')
        
                            #Naming the main graph
                            plt.suptitle("Voltammogram")   
                            plt.show()

                        else :
                            messagebox.showerror("ERROR", "ERROR")

    
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
            if inputchannelnumber.get() == '1' and ion2.get() != "None":
                messagebox.showerror("ERROR", "Please Set 'Ion Sample Type for Channel 2' to None")
            # Validate ion type in channel 2 if using all channels
            elif inputchannelnumber.get() == '2' and ion2.get() == 'None' :
                messagebox.showerror("ERROR", "Please Set 'Ion Sample Type for Channel 2' to K or Na")
            elif ion1.get() == "Calibration" or ion2.get() == "Calibration" :
                messagebox.showerror("ERROR", "Calibration can only be conducted by using the CV method")
            else :
                valid2 = True

            #All user parameter input is valid
            if valid == True and valid2 == True :
                parameter = inputmethod.get() + "|" + vmin_var.get() + "|" + vmax_var.get() +  "|" + scanrate_var.get() + "|" + cycle_var.get() + "|" + inputchannelnumber.get() + "|" + ion1.get() + "|" + ion2.get() + "|" + vincrem_var.get() + "|" + amp_var.get() + "|" + sampling_var.get() + "|" + pulse_var.get() 
                messagebox.showinfo("INFO", "Make sure the filename and parameters are correct.\nYour filename is "+inputfilename.get()+".csv.\nYour parameter is "+parameter+".\nPlease click 'OK' to continue the process.\n Wait until the plot is shown.\n The file will be saved in " + parent_folder) 
        
                file_name = inputfilename.get()+".csv"

                input_parameter = methodnumber+"|"+vmin_var.get()+"|"+vmax_var.get()+"|"+vincrem_var.get()+"|"+scanrate_var.get()+"|"+cycle_var.get()+"|"+sampling_var.get()+"|"+amp_var.get()+"|"+pulse_var.get()+"|"+inputchannelnumber.get()+ "|" + ion1.get() + "|" + ion2.get()
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

                
                    #Close the serial plot
                    ser.close()

                #except IndexError or UnicodeDecodeError or serial.serialutil.SerialException :
                    #messagebox.showerror("ERROR", "Something went wrong. Please, Try again")
            
                    #Reading the data from CSV File and Plot it
                    with open(folder, 'r') as f :
                        reader = csv.reader(f, delimiter = ";")
                        next(reader)    #Skip the header row
                        next(reader)    #skip the second row in DPV data

                        #Define variable of array
                        x = []
                        y1 = []
                        y2 = []
                        axis_min = float(vmin_var.get())
                        axis_max = float(vmax_var.get())
                
                        for row in reader:
                            if len(row) == 3 :
                                x.append(float(row[0]))
                                y1.append(float(row[1]))
                                y2.append(float(row[2]))
                            elif len(row) == 2 :
                                x.append(float(row[0]))
                                y1.append(float(row[1]))               

                        #Check number of channel that being used
                        if len(y1) > 0 and len(y2) == 0 :   #1 Channel only
                            UpperRange1 = len(y1) + 1
                            max_current1 = max(y1)  #Finding the maximum value of current in channel 1
                            min_current1 = min(y1)  #Findign the minimum value of current in channel 1
                            K_Concentration1 =  1.720193 * max_current1 - 55.3448    #Concentration Estimation of K
                            K_Concentration1 = round(K_Concentration1, 4)   #Round the number to 4 decimal places
                            Na_Concentration1 = 2.370854 * max_current1 - 138.698   #Concentration Estimation of Na
                            Na_Concentration1 = round(Na_Concentration1, 4) #Round the number to 4 decimal places

                            messagebox.showinfo("SUCCESS", "Measurement Completed!")
        
                            #Calulate Concentration
                            if ion1.get() == "K" and ion2.get() == "None" :      
                                result1.insert(0, K_Concentration1)
                            elif ion1.get() == "Na" and ion2.get() == "None":
                                result1.insert(0, Na_Concentration1)
                        
                            #Plotting the Data from CSV
                            plt.plot(x, y1, color = 'red')
                            plt.xlabel("Voltage(V)")
                            plt.ylabel("Current(µA)")
                            plt.title("Voltammogram")
                            plt.axis([axis_min, axis_max, min_current1, max_current1])
                            plt.grid('on')
                            plt.show()

                        elif len(y1) > 0 and len(y2) > 0 :    #Using 2 channel
                            #Find maximum value in desired range
                            UpperRange1 = len(y1) + 1                       #Upper range of index in channel 1 
                            UpperRange2 = len(y2) + 1                       #Upper range of index in channel 2

                            max_current1 = max(y1)  #Finding the maximum value of current in Channel 1
                            max_current2 = max(y2)  #Finding the maximum value of current in channel 2
                            min_current1 = min(y1)  #Finding the minimum value of current in channel 1
                            min_current2 = min(y2)  #Finding the minimum value of current in channel 2
                            
                            K_Concentration1 =  1.720193 * max_current1 - 55.3448    #Concentration Estimation of K
                            K_Concentration1 = round(K_Concentration1, 4)   #Round the number to 4 decimal places
                            Na_Concentration1 = 2.370854 * max_current1 - 138.698   #Concentration Estimation of Na
                            Na_Concentration1 = round(Na_Concentration1, 4) #Round the number to 4 decimal places

                            K_Concentration2 =  1.720193 * max_current2 - 55.3448    #Concentration Estimation of K
                            K_Concentration2 = round(K_Concentration2, 4)   #Round the number to 4 decimal places
                            Na_Concentration2 = 2.370854 * max_current2 - 138.698   #Concentration Estimation of Na
                            Na_Concentration2 = round(Na_Concentration2, 4) #Round the number to 4 decimal places
        
                            messagebox.showinfo("SUCCESS", "Measurement Completed!")

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
                            
                       
                            #Subplot for Channel 1  
                            plt.subplot(211)
                            plt.plot(x, y1, color= 'red')
                            plt.subplot(211).set_title("Channel 1")
                            plt.xlabel("Voltage(V)")
                            plt.ylabel("Current(µA)")
                            plt.axis([axis_min, axis_max, min_current1, max_current1])
                            plt.grid('on')

                            #Subplot for channel 2
                            plt.subplot(212)
                            plt.plot(x, y2, color = 'green')
                            plt.xlabel("Voltage(V)")
                            plt.ylabel("Current(µA)")
                            plt.axis([axis_min, axis_max, min_current2, max_current2])
                            plt.grid('on')
    
                            #Naming the main graph
                            plt.suptitle("Voltammogram")   
                            plt.show()

                        else :
                            messagebox.showerror("ERROR", "ERROR")

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
    ion1.set("")
    ion2.set("")
    result1_var.set("")
    result2_var.set("")
    progress_bar.reset_progressbar()

#Function for disabling paramter input based on method being choosen by user
def metode() :
    if (inputmethod.get() == "CV"):
        VminEntry['state'] = tk.NORMAL
        VmaxEntry['state'] = tk.NORMAL
        scanrateEntry['state'] = tk.NORMAL
        cycleEntry['state'] = tk.NORMAL
        vmin_var.set("-1")
        vmax_var.set('1')
        scanrate_var.set('50')
        cycle_var.set('3')
        
    else : #method == DPV
        VminEntry['state'] = tk.NORMAL
        VmaxEntry['state'] = tk.NORMAL
        scanrateEntry['state'] = tk.NORMAL
        VincremEntry['state'] = tk.NORMAL
        samplingEntry['state'] = tk.NORMAL
        ampEntry['state'] = tk.NORMAL
        pulseEntry['state'] = tk.NORMAL
        vmin_var.set('-0.25')
        vmax_var.set('0.5')
        vincrem_var.set('0.01')
        scanrate_var.set('50')
        amp_var.set('0.2')
        pulse_var.set('20')
        cycle_var.set("1")
        sampling_var.set("10")

###################### APP WIDGET ######################

#App window 
window = tk.Tk()
window.geometry("1000x450")
window.title("PS Dual")
window.resizable(False, False)

#add icon logo
icon = tk.PhotoImage(file = 'gear-icon.png')
window.iconphoto(False, icon)

#Column 1
method = tk.Label(window, text = "Method")
method.grid(column = 0  , row = 3)

#Combobox for method dropdown button 
inputmethod = tk.StringVar()
method_choosen = ttk.Combobox(window, width = 22, textvariable = inputmethod)
method_choosen['values'] = ('CV', 'DPV')
inputmethod.set("")

#Combobox for num. of channel dropdown button
Channel_number = tk.Label(window, text = "Number of Channel").grid(column = 0 , row = 2)
inputchannelnumber = tk.StringVar()
Channelnumber_choosen = ttk.Combobox(window, width = 22, textvariable = inputchannelnumber)
Channelnumber_choosen['values'] = ('1', '2')
inputchannelnumber.set("")

Filename = tk.Label(text = "File Name").grid(column = 0, row = 1) #EditF
Vmin = tk.Label(text = "Vmin(V) [Value between -1.5V - 1.5V]").grid(column = 0, row = 5)
Vmax = tk.Label(text = "Vmax(V) [Value between -1.5V - 1.5V]").grid(column = 0, row = 6)
Cycle = tk.Label(text = "Cycle [Value between 2 - 255]").grid(column = 0, row = 7)
Scanrate = tk.Label(text = "Scan Rate(mV/s) [Value between 10-120]").grid(column = 0, row = 8)

#Text for Input Parameter Button
ttk.Label(window, text = "Click Input Parameter Button Before Enter Value").grid(column = 0 , row  = 4)

#Input Parameter Button
method_button = tk.Button(window, text = "Input Parameter", command = metode)
method_button.grid(column = 1, row = 4)

#Column 2
#Combobox for Ion Sample Type in Channel 1
Ion_sample1 = tk.Label(window, text = "Ion Sample Type for Channel 1").grid(column = 8, row = 1)
ion1 = tk.StringVar()
ion_choosen1 = ttk.Combobox(window, width = 22, textvariable = ion1)
ion_choosen1['values'] = ('Na', 'K', 'Calibration')
ion_choosen1.grid(column = 10, row = 1)
ion_choosen1.current()
ion1.set("")

#Combobox for Ion Sample Type in Channel 2
Ion_sample2 = tk.Label(window, text = "Ion Sample Type for Channel 2").grid(column = 8, row = 2)
ion2 = tk.StringVar()
ion_choosen2 = ttk.Combobox(window, width = 22, textvariable = ion2)
ion_choosen2['values'] = ('Na', 'K', 'Calibration','None')
ion_choosen2.grid(column = 10, row = 2)
ion_choosen2.current()
ion2.set("")

#Text
TextArea = tk.Label(text = "Additional Parameter For DPV Method: ").grid(column = 8, row = 3)

#Additional Parameter For DPV Method
Vincrem = tk.Label(text = "Vinc(V) [Value between 0.001V - 0.25V]").grid(column = 8, row = 4) #Edit
Amp = tk.Label(text = "Vamp(V) [Value between 0.001V - 0.25V]").grid(column = 8, row = 5)
Sampling = tk.Label(text = "Tsampling(ms)").grid(column = 8, row = 6)
Pulse = tk.Label(text = "TPulse(ms) [Value between 0.4ms to 1000ms]").grid(column = 8, row = 7)

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

method_choosen.grid(column = 1, row = 3)
method_choosen.current()

filenameEntry = tk.Entry(window, textvariable = inputfilename, width = 25)
filenameEntry.grid(column = 1, row = 1) 

VminEntry = tk.Entry(window, textvariable = vmin_var, width = 25)
VminEntry.grid(column = 1, row = 5)
vmin_var.set("0.0")
VminEntry['state'] = tk.DISABLED

VmaxEntry = tk.Entry(textvariable = vmax_var, width = 25)
VmaxEntry.grid(column = 1, row = 6)
vmax_var.set("0.0")
VmaxEntry['state'] = tk.DISABLED

cycleEntry = tk.Entry(textvariable = cycle_var, width = 25)
cycleEntry.grid(column = 1, row = 7)
cycle_var.set("1")
cycleEntry['state'] = tk.DISABLED

scanrateEntry = tk.Entry(textvariable = scanrate_var, width = 25)
scanrateEntry.grid(column = 1, row = 8)
scanrate_var.set("0")
scanrateEntry['state'] = tk.DISABLED

Channelnumber_choosen.grid(column = 1, row = 2)
Channelnumber_choosen.current()

VincremEntry = tk.Entry(textvariable = vincrem_var, width = 25)
VincremEntry.grid(column = 10, row = 4)
vincrem_var.set("0.0")
VincremEntry['state'] = tk.DISABLED

ampEntry = tk.Entry(textvariable = amp_var, width = 25)
ampEntry.grid(column = 10, row = 5)
amp_var.set("0.0")
ampEntry['state'] = tk.DISABLED

samplingEntry = tk.Entry (textvariable = sampling_var, width = 25)
samplingEntry.grid(column = 10, row = 6)
sampling_var.set("10")
samplingEntry['state'] = tk.DISABLED

pulseEntry = tk.Entry(textvariable = pulse_var, width = 25)
pulseEntry.grid(column = 10, row = 7)
pulse_var.set("0.0")
pulseEntry['state'] = tk.DISABLED

#Estimation Concentration Label
result1_var = tk.StringVar()
result2_var = tk.StringVar()

tk.Label(window, text = "Concentration Of Samples", font = ("Sherif", 12), fg = "red").grid(column = 8, row = 10)
Result1 = tk.Label(text = "Concentration in Channel 1 (mM): ").grid(column = 0 , row = 20 )
result1 = tk.Entry(textvariable = result1_var, width = 25)
result1.grid(row = 20, column = 1)

Result2 = tk.Label(text = "Concentration in Channel 2 (mM): ").grid(column = 8, row = 20)
result2 = tk.Entry(textvariable = result2_var, width  = 25)
result2.grid(row = 20, column = 10)

#Start and Reset Button
start = tk.Button(window, text = "Start", width = 15, command = StartButton)
start.grid(column = 1, row = 35)
reset  = tk.Button(window, text = "Reset", width = 15, command = ResetButton)
reset.grid(column = 10, row = 35 )

#Label Text 
ttk.Label(window, text = "Press Reset", font = ("Sherif", 12)).grid(column = 8, row = 40)
ttk.Label(window, text = "after changing the measurement method or finish measuring", font = ("Sherif", 10)).grid(column = 8, row = 50)

#Progressbar
max_rows = 10000
progress_bar = ProgressBar(window, max_rows)

window.mainloop()