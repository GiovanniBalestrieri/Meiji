import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import signal


val_x = []
val_y = []
val_z = []

with open("data.csv",'rb') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        val_x.append(float(row[1]))
        val_y.append(float(row[2]))
        val_z.append(float(row[3]))

plt.figure(1)
#plt.subplot(211)
plt.plot(val_y, 'b', sp.signal.medfilt(val_y,5),'r')
plt.grid()
#plt.subplot(212)
#plt.plot(val_z,'r')
plt.show()
