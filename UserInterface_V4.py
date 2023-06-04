import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import screeninfo
from PIL import Image, ImageTk

import threading
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import csv
import os.path
import serial
from serial import Serial
import scipy.signal as signal
import math
import serial.tools.list_ports


#Start Button Function
def perform_measurement():
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


    #Validate if Input is empty
    if methodnumber == "" or vmin_var.get() == "" or vmax_var.get() == "" or scanrate_var.get() =="" or cycle_var.get() == "" or inputchannelnumber.get() == "" or ion1.get() == "" or ion2.get() == "" or amp_var.get() == "" or vincrem_var.get() == "" or pulse_var.get() == "" or sampling_var.get() == "" or inputfilename.get() =="" or check_var.get() == "off":
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
                messagebox.showinfo("INFO", "Make sure the filename and parameters are correct.\nYour filename is "+inputfilename.get()+".csv.\nYour parameter is "+parameter+".\nPlease click 'OK' to continue the process.\n Wait until the plot is shown.\n The file will be saved in " + save) 
        
                file_name = inputfilename.get()+".csv"

                input_parameter = methodnumber+"|"+vmin_var.get()+"|"+vmax_var.get()+"|"+vincrem_var.get()+"|"+scanrate_var.get()+"|"+cycle_var.get()+"|"+sampling_var.get()+"|"+amp_var.get()+"|"+pulse_var.get()+"|"+inputchannelnumber.get()+ "|" + ion1.get() + "|" + ion2.get()
                string1 = input_parameter
                string1_encode = string1.encode()

                #disable start button
                start.configure(state = "disabled")

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
                    progress_bar.start()

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
                        
                            #Break out of the loop if read serial data "999999999"
                            if line == "999999999" :
                                break
            
                            data = line.split(';')

                            if len(data) == 2 :
                                writer.writerow([data[0], data[1]])

                            elif len(data) == 3 :
                                writer.writerow([data[0], data[1], data[2]])

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
                            max_current1 = max(values_in_range_CV)
                            min_current1 = min(values_in_range_CV)
                            FeCN_Concentration1 = 0.21372 * max_current1 + 0.737816 
                            FeCN_Concentration1 = round(FeCN_Concentration1, 4)

                            #Show Concentration
                            if ion1.get() == 'Calibration' and ion2.get() == 'None':
                                result1.insert("0.0", FeCN_Concentration1)

                            x = [value for index, value in enumerate(x) if index > 5413]
                            y1 = [value for index, value in enumerate(y1) if index > 5413]
                            min_current2 = None
                            max_current2 = None
                            
                            #Plotting the graph
                            #Show the graph by calling plot_graph function
                            #plotting the graph by using a thread
                            window.after(1, plot_graph, x, y1, y2, axis_min, axis_max, min_current1, min_current2, max_current1, max_current2)
                    
                            progress_bar.stop()

                            messagebox.showinfo("SUCCESS", "Measurement Completed!")

                        elif len(y1) > 0 and len(y2) > 0 :    #Using 2 channel
                            #Find maximum value in desired range
                            UpperRange1 = len(y1) + 1                       #Upper range of index in channel 1 
                            UpperRange2 = len(y2) + 1                       #Upper range of index in channel 2

                            #Slicing array for CV
                            values_in_range_CV_1 = y1[5413:UpperRange1]
                            values_in_range_CV_2 = y2[5413:UpperRange2]
                            max_current1 = max(values_in_range_CV_1)
                            max_current2 = max(values_in_range_CV_2)
                            min_current1 = min(values_in_range_CV_1)
                            min_current2 = min(values_in_range_CV_2)
                            FeCN_Concentration1 = 0.21372 * max_current1 + 0.737816
                            FeCN_Concentration2 = 0.21372 * max_current2 + 0.737816

                            if ion1.get() == "FeCN" and ion2.get() == "FeCN":
                                result1.insert("0.0", FeCN_Concentration1)
                                result2.insert("0.0", FeCN_Concentration2)
                                
                        
                            x = [value for index, value in enumerate(x) if index > 5413]
                            y1 = [value for index, value in enumerate(y1) if index > 5413]
                            y2 = [value for index, value in enumerate(y2) if index > 5413]

                            #Plotting the graph
                            #Show the graph by calling plot_graph function
                            #plotting the graph by using a thread
                            window.after(1, plot_graph, x, y1, y2, axis_min, axis_max, min_current1, min_current2, max_current1, max_current2)
                            
                            progress_bar.stop()

                            messagebox.showinfo("SUCCESS", "Measurement Completed!")

                        else :
                            progress_bar.stop()
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
                messagebox.showinfo("INFO", "Make sure the filename and parameters are correct.\nYour filename is "+inputfilename.get()+".csv.\nYour parameter is "+parameter+".\nPlease click 'OK' to continue the process.\n Wait until the plot is shown.\n The file will be saved in " + save) 
        
                file_name = inputfilename.get()+".csv"

                input_parameter = methodnumber+"|"+vmin_var.get()+"|"+vmax_var.get()+"|"+vincrem_var.get()+"|"+scanrate_var.get()+"|"+cycle_var.get()+"|"+sampling_var.get()+"|"+amp_var.get()+"|"+pulse_var.get()+"|"+inputchannelnumber.get()+ "|" + ion1.get() + "|" + ion2.get()
                string1 = input_parameter
                string1_encode = string1.encode()

                #disable start button
                start.configure(state = "disabled")

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
                    progress_bar.start()

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

                            #Break out of the loop if read serial data "999999999"
                            if line == "999999999" :
                                break
            
                            data = line.split(';')

                            if len(data) == 2 :
                                writer.writerow([data[0], data[1]])

                            elif len(data) == 3 :
                                writer.writerow([data[0], data[1], data[2]])
                
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
                            y2 = None
                            min_current2 = None
                            max_current2 = None
                        
                            #Calulate Concentration
                            if ion1.get() == "K" and ion2.get() == "None" :      
                                result1.insert("0.0", K_Concentration1)
                            elif ion1.get() == "Na" and ion2.get() == "None":
                                result1.insert("0.0", Na_Concentration1)

                            #Plot graph by calling plot_graph function
                            #plotting the graph by using a thread
                            window.after(1, plot_graph, x, y1, y2, axis_min, axis_max, min_current1, min_current2, max_current1, max_current2)
                           
                            progress_bar.stop()

                            messagebox.showinfo("SUCCESS", "Measurement Completed!")

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
        
                            #Calculate Concentration
                            if ion1.get() == "K" and ion2.get() == "K":
                                result1.insert("0.0", K_Concentration1)
                                result2.insert("0.0", K_Concentration2)
                            elif ion1.get() == "Na" and ion2.get() == "Na" :
                                result1.insert("0.0", Na_Concentration1)
                                result2.insert("0.0", Na_Concentration2)
                            elif ion1.get() == "K" and ion2.get() == "Na" :
                                result1.insert("0.0", K_Concentration1)
                                result2.insert("0.0", Na_Concentration2)
                            elif ion1.get() == "Na" and ion2.get() == "K" :
                                result1.insert("0.0", Na_Concentration1)
                                result2.insert("0.0", K_Concentration2)

                            #Show the graph by calling plot_graph function
                            window.after(1, plot_graph, x, y1, y2, axis_min, axis_max, min_current1, min_current2, max_current1, max_current2)
                         
                            progress_bar.stop()

                            #Message box measurement completed
                            messagebox.showinfo("SUCCESS", "Measurement Completed!")

                        else :
                            progress_bar.stop()
                            messagebox.showerror("ERROR", "ERROR")

#Function to simulate a long running measurement process
#this function use thread so can do multitasking (progress bar and showing plot)
def StartButton():
    #Create a separate threads for measurement process
    measurement_thread = threading.Thread(target = perform_measurement)
    measurement_thread.start()

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
    result1.delete("0.0", "end")  # delete all text
    result2.delete("0.0", "end")  # delete all text
    progress_bar.stop()
    check_var.set("off")
    clear_plot()
    start.configure(state = "normal")

#Function for clearing the plot from canvas
def clear_plot():
    global fig, canvas, tk_canvas
    
    #Clear figure
    if fig is not None :
        fig.clear()

    #delete the canvas
    if canvas is not None :
        canvas.get_tk_widget().grid_forget()

    tk_canvas.delete("all")

#Function for disabling paramter input based on method being choosen by user
def metode() :
    if (inputmethod.get() == "CV") and (check_var.get() == "on"):
        VminEntry.configure(state = "normal")
        VmaxEntry.configure(state = "normal")
        scanrateEntry.configure(state = "normal")
        cycleEntry.configure(state = "normal")
        vmin_var.set("-1")
        vmax_var.set("1")
        scanrate_var.set('50')
        cycle_var.set("3")
        

    elif (inputmethod.get() == "DPV") and (check_var.get() == "on"): #method == DPV
        VminEntry.configure(state = "normal")
        VmaxEntry.configure(state = "normal")
        scanrateEntry.configure(state = "normal")
        VincremEntry.configure(state = "normal")
        samplingEntry.configure(state = "normal")
        ampEntry.configure(state = "normal")
        pulseEntry.configure(state = "normal")
        vmin_var.set('-0.25')
        vmax_var.set('0.5')
        vincrem_var.set('0.01')
        scanrate_var.set('50')
        amp_var.set('0.2')
        pulse_var.set('20')
        cycle_var.set("1")
        sampling_var.set("10")

#Plot graph
def plot_graph(x, y1, y2 = None , axis_min = None, axis_max = None, min_current1 = None, min_current2 = None, max_current1 = None, max_current2 = None):
    global ax1, ax2, ax, fig, canvas, tk_canvas

    #Check fig is none or not
    if fig is None :
        fig = plt.figure(figsize=(12,8), dpi = 100)
    else :
        fig.clear()
    
    if y2 is not None and isinstance(y2, (list, tuple)) and len(y2) > 0:
        #create subplots
        ax1 = fig.add_subplot(211)
        ax2 = fig.add_subplot(212)

        #Plot the data in subplots
        ax1.plot(x, y1, color = 'red')
        ax2.plot(x, y2, color = 'green')

        #configure the subplots
        ax1.set_xlabel("Voltage (V)")
        ax1.set_ylabel("Current (µA)")
        ax1.set_title("Plot in Channel 1")
        ax1.grid('on')
        ax1.axis([axis_min, axis_max, min_current1, max_current1])

        ax2.set_xlabel("Voltage (V)")
        ax2.set_ylabel("Current (µA)")
        ax2.set_title("Plot in Channel 2")
        ax2.axis([axis_min, axis_max, min_current2, max_current2])
        ax2.grid('on')

        #Adjust the spacing between subplots and labels
        plt.subplots_adjust(hspace = 0.3)
        
    else:
        ax = fig.add_subplot(111)

        #Plot the data
        ax.plot(x, y1, color = 'red')

        #Configure the plot
        ax.set_xlabel("Voltage (V)")
        ax.set_ylabel("Current (µA)")
        ax.set_title("Voltammogram")
        ax.axis([axis_min, axis_max, min_current1, max_current1])
        ax.grid('on')
    
    #update tkinter canvas
    if canvas is not None :
        canvas.get_tk_widget().grid_forget()

    #Make a canvas and place the plot in this canvas
    canvas = FigureCanvasTkAgg(fig, master = frame)
    window_bg_color = window.cget("background")
    canvas.get_tk_widget().configure(bg = window_bg_color)
    canvas.get_tk_widget().grid(row = 1, column= 2, padx= 10, pady=10, sticky= 'nse')
    canvas.draw()

    #pack toolbar
    toolbar = NavigationToolbar2Tk(canvas, frame, pack_toolbar = False)
    toolbar.update()
    toolbar.grid(row = 2, column = 2)

#Main Loop

#Make App Window
window = ctk.CTk()
window.title("PS Dual")
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")
window.resizable(True, True)

#Set the window size
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")

window.protocol("WM_DELETE_WINDOW", window.quit)

#File name
Filename = ctk.CTkLabel(window, text = "File Name:", font = ('Roboto', 14))
Filename.grid(row = 1, column = 0, sticky = "w", pady = (20,5), padx = 10)
inputfilename = ctk.StringVar()
filenameEntry = ctk.CTkEntry(window, textvariable = inputfilename, width= 200, font = ('Roboto', 14))
filenameEntry.grid(row  = 1, column = 1, pady = (20,5), padx = 10)

#Number of Channel
Channel_number = ctk.CTkLabel(window, text = "Number of Channel:", font= ('Roboto', 14))
Channel_number.grid(row = 2, column = 0, sticky = 'w', pady = 5, padx = 10)
inputchannelnumber = ctk.StringVar()
Channelnumber_choosen = ctk.CTkComboBox(window, variable = inputchannelnumber, values = ['1', '2'], width = 200, font = ("Roboto", 14))
Channelnumber_choosen.grid(row = 2, column = 1, pady = 5, padx =10)
inputchannelnumber.set("")

#Method
method = ctk.CTkLabel(window, text = "Method:", font = ("Roboto", 14))
method.grid(row = 3, column = 0, sticky = 'w', pady = 5, padx = 10)
inputmethod = ctk.StringVar()
method_choosen = ctk.CTkComboBox(window, variable= inputmethod, values=['CV', 'DPV'], width= 200, font = ("Roboto",14) )
method_choosen.grid(row = 3, column = 1, pady = 5, padx = 10)
inputmethod.set("")

#Input Parameter
check_var = ctk.StringVar()
method_button = ctk.CTkCheckBox(window, text = "Are you sure with the method?", command = metode, onvalue= "on", offvalue = 'off', variable = check_var)
method_button.grid(row = 4, column = 1, pady = 5, padx = 10 )

#Ion sample type for channel 1
Ion_sample1 = ctk.CTkLabel(window, text= "Ion Sample Type For Channel 1", font = ("Roboto", 14))
Ion_sample1.grid(row = 5, column = 0, padx = 10, pady = 5, sticky = 'w')
ion1 = ctk.StringVar()
ion_choosen1 = ctk.CTkComboBox(window, width =200, variable=ion1, values=['Na', 'K', 'Calibration'], font = ('Roboto', 14))
ion_choosen1.grid(row = 5, column = 1 , padx = 10, pady =5)
ion1.set("")

#Ion sample type for channel 2
Ion_sample2 = ctk.CTkLabel(window , text = "Ion Sample Type For Channel 2", font = ("Roboto", 14))
Ion_sample2.grid(row = 6, column = 0, padx =10, pady =5, sticky = 'w')
ion2 = ctk.StringVar()
ion_choosen2 = ctk.CTkComboBox(window, width= 200, variable=ion2, values = ['Na', 'K', 'Calibration', 'None'], font = ("Roboto", 14))
ion_choosen2.grid(row = 6, column = 1, padx = 10, pady =5)
ion2.set("")

#Voltage sweep minimum
Vmin = ctk.CTkLabel(window, text= "Vmin (V):", font= ("Roboto", 14))
Vmin.grid(row = 7, column =0, padx = 10, pady = 5, sticky = 'w' )
vmin_var = ctk.StringVar()
VminEntry = ctk.CTkEntry(window, textvariable = vmin_var, width= 200, font = ("Roboto", 14) )
VminEntry.grid(row = 7, column = 1, padx = 10, pady = 5)
vmin_var.set("0.0")
VminEntry.configure(state = "disabled")

#Voltage max
Vmax = ctk.CTkLabel(window, text = "Vmax (V):", font = ("Roboto", 14))
Vmax.grid(row = 8, column =0 , sticky = 'w', padx = 10, pady = 5)
vmax_var = ctk.StringVar()
VmaxEntry = ctk.CTkEntry(window, textvariable = vmax_var, width= 200, font = ("Roboto", 14) )
VmaxEntry.grid(row =8, column = 1, padx = 10, pady =5)
vmax_var.set("0.0")
VmaxEntry.configure(state="disabled")

#Cycle
Cycle = ctk.CTkLabel(window, text = "Cycle:", font = ("Roboto", 14))
Cycle.grid(row = 9, column = 0,sticky = 'w', padx= 10, pady = 5)
cycle_var = ctk.StringVar()
cycleEntry = ctk.CTkEntry(window, textvariable=cycle_var, width= 200, font = ("Roboto", 14))
cycleEntry.grid(row = 9, column= 1, padx = 10, pady = 5)
cycle_var.set("0.0")
cycleEntry.configure(state = "disabled")

#Scan Rate
Scanrate = ctk.CTkLabel(window, text = "Scan Rate (mV/s):", font= ("Roboto", 14))
Scanrate.grid(row = 10, column = 0, sticky = 'w', padx = 10, pady = 5)
scanrate_var = ctk.StringVar()
scanrateEntry = ctk.CTkEntry(window, textvariable=scanrate_var, width = 200, font = ("Roboto", 14))
scanrateEntry.grid(row = 10, column = 1, padx = 10, pady = 5)
scanrate_var.set("0.0")
scanrateEntry.configure(state = "disabled")

#Text additional parameter for DPV
add_DPV = ctk.CTkLabel(window, text = "Additional Parameter For DPV Method:", font =("Roboto", 14))
add_DPV.grid (row = 11, column = 0, sticky = 'w', padx = 10, pady = 5)

#Vincrement
Vincrem = ctk.CTkLabel(window, text= "Vinc (mV):", font = ("Roboto", 14))
Vincrem.grid(row =12, column = 0, sticky = 'w', padx =10, pady =5)
vincrem_var = ctk.StringVar()
VincremEntry = ctk.CTkEntry(window, textvariable = vincrem_var, width = 200, font = ("Roboto", 14))
VincremEntry.grid(row = 12, column = 1, padx = 10, pady = 5)
vincrem_var.set("0.0")
VincremEntry.configure(state = "disabled")

#V amplitude
Amp = ctk.CTkLabel(window, text = "Vamp (mV):", font = ("Roboto", 14))
Amp.grid(row = 13, column = 0, sticky = 'w', padx = 10, pady = 5)
amp_var = ctk.StringVar()
ampEntry = ctk.CTkEntry(window, textvariable= amp_var, width= 200, font = ("Roboto", 14))
ampEntry.grid(row = 13, column =1, padx = 10, pady = 5)
amp_var.set("0.0")
ampEntry.configure(state = "disabled")

#Tsampling
Sampling = ctk.CTkLabel(window, text = "Tsampling (ms):", font = ("Roboto", 14))
Sampling.grid(row = 14, column = 0, sticky = 'w', padx = 10, pady = 5)
sampling_var = ctk.StringVar()
samplingEntry = ctk.CTkEntry(window, textvariable=sampling_var, width = 200, font = ("Roboto", 14))
samplingEntry.grid(row = 14, column = 1, padx =10, pady = 5)
sampling_var.set("0.0")
samplingEntry.configure(state = "disabled")

#Tpulse
Pulse = ctk.CTkLabel(window, text = "Tpulse (ms):", font=("Roboto", 14))
Pulse.grid(row = 15, column = 0, padx = 10, pady =5, sticky = 'w')
pulse_var = ctk.StringVar()
pulseEntry = ctk.CTkEntry(window, textvariable= pulse_var, width = 200, font =("Roboto", 14))
pulseEntry.grid(row = 15, column = 1, padx =10, pady =5)
pulse_var.set("0.0")
pulseEntry.configure(state = "disabled")

#Progress bar
progress_bar = ctk.CTkProgressBar(window, mode = "indeterminate", width= 500, height= 25)
progress_bar.grid(column = 0, row = 16, columnspan = 2, padx = 10, pady = 10, sticky = 'w')

#Start Button
start = ctk.CTkButton(window, text = "Start", height = 37, width= 150, font = ("Roboto", 20) , command= StartButton)
start.grid(row = 17, column = 0, padx = 5, pady = 15)

#Reset Button
reset = ctk.CTkButton(window, text= "Reset", height = 37, width = 150, font =("Roboto", 20), command=ResetButton)
reset.grid(row = 17, column =1, padx = 5, pady=  15)

#Text Press Reset
reset_txt = ctk.CTkLabel(window, text="Press Reset", font = ("Roboto", 20))
reset_txt.grid(row = 20, column = 0, padx = 10, pady = 5, sticky = 'n', columnspan = 2)
reset2_txt = ctk.CTkLabel(window, text = "after changing the measurement method or finish measuring", font = ("Roboto", 14))
reset2_txt.grid(row = 21, column = 0, padx = 10, pady = 5, sticky = 'n', columnspan = 2)

#Samples Concentration
frame = ctk.CTkFrame(window, height = 300, width= 250)
frame.grid(row = 1, column = 2, rowspan = 100, padx = (30,10), pady  = 10, sticky = 'ne')

#Create a canvas to display the plot
#Make a Canvas for showing graph
fig = plt.figure(figsize=(12, 8), dpi = 100)
ax1 = None
ax2 = None
ax = None
canvas = None

#creta separate tkinter canvas
tk_canvas = ctk.CTkCanvas(frame, height = 800, width = 1000)
tk_canvas.grid(row = 1, column= 2, padx= 10, pady=10, sticky= 'nse' )

#Add Logo PS Dual
LOGO_PATH = "C:\TA2\output_dark.png"
add_logo = ctk.CTkImage(light_image = Image.open(os.path.join(LOGO_PATH)), size = (200,200))
logo = ctk.CTkLabel(master = frame, image = add_logo, text = "")
logo.grid(row = 100, column  = 2, rowspan = 20, sticky = 'e', padx = 10, pady = 10)

#Make a Frame
frame2 = ctk.CTkFrame(frame, height= 20, width= 20)
frame2.grid(row = 4, column = 2, rowspan = 100, padx = 10, pady = 10, sticky = 'n')

concentration = ctk.CTkLabel(frame2, text = "Ion Concentration in Solution", font = ("Roboto", 20))
concentration.grid(row = 3, column =  2, padx = 10, pady = (10,0), sticky = 'ne')

#Channel 1
Result1 = ctk.CTkLabel(frame2, text = "Channel 1 (mM):", font = ("Roboto", 14))
Result1.grid(row = 4, column = 1, padx = (5,2), pady = 5, sticky = 'n')
result1 = ctk.CTkTextbox(frame2, width = 200, height= 5, font = ("Roboto", 14))
result1.grid(row = 4, column = 2, padx = 2, pady =5, sticky = 'n')

#Channel 2
Result2 = ctk.CTkLabel(frame2, text = "Channel 2 (mM):", font = ("Roboto", 14))
Result2.grid(row = 5, column = 1, padx = (5,2), pady = 5, sticky = 'n')
result2 = ctk.CTkTextbox(frame2, width = 200, height = 5, font = ("Roboto", 14))
result2.grid(row =5, column = 2, padx =2, pady = (5,10), sticky= 'n')

window.mainloop()   



