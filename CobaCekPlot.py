import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv


file = 'Resistor 10k all.csv'
df = pd.read_csv(file)

#Read total amount of column
total_column = len(df.axes[1])

x = [];
y1 = [];
y2 = [];
    
if total_column == 2 : #1 Channel
    x = df[df.columns[0]]
    y1 = df[df.columns[1]]

    x_max = max(x)
    x_min = min(x)
    
    y1_max = max(y1)
    y1_min = min(y1)

    plt.plot(x, y1, 'red')
    plt.xlabel("Voltage(V)")
    plt.ylabel("Current(µA)")
    plt.title("Voltammogram")
    plt.axis([x_min, x_max, y1_min, y1_max])
    plt.grid()
    plt.show()

elif total_column == 3 : #2 Channel
    x = df[df.columns[0]]
    y1 = df[df.columns[1]]
    y2 = df[df.columns[2]]
    
    x_min = min(x)
    x_max = max(x)

    y1_min = min(y1)
    y1_max = max(y1)
    
    y2_min = min(y2)
    y2_max = max(y2)

    plt.subplot(211)
    #plt.scatter(x, y1, linewidth= 0.00001, color='red', label = "Channel 1")
    plt.plot(x, y1, 'r')
    plt.xlabel("Voltage(V)")
    plt.ylabel("Current(µA)")
    plt.axis([x_min, x_max, y1_min, y1_max])
    plt.grid()

    #Subplot for channel 2
    plt.subplot(212)
    #plt.scatter(x, y2, linewidth = 0.001, color = 'green', label = "Channel 2")
    plt.plot(x, y2, 'g')
    plt.xlabel("Voltage(V)")
    plt.ylabel("Current(µA)")
    plt.axis([x_min, x_max, y2_min, y2_max])
    plt.grid()
    
    #Naming the main graph
    plt.suptitle("Voltammogram")   
    plt.show()
