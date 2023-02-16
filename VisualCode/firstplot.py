import numpy as np
import matplotlib.pyplot as plt
import csv

csv_filename = 'testplot.csv'
with open(csv_filename) as f:
   
   reader = np.loadtxt(csv_filename, delimiter=";")
    
print(reader)
length = (len(reader))

print(reader[1,1])

plt.axis([-1.5, 1.5, -600, 600])

for i in range(length):
    plt.scatter(reader[i,0], reader[i,1], linewidth= 1, color='blue')
    plt.pause(0.005)

plt.show()