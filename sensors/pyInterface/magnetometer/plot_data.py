import csv, sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

val_x = []
val_y = []
val_z = []
yaw = []

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

with open("calibrate_values.csv",'rb') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    for row in reader:
        print(row)
        val_x.append(float(row[1]))
        val_y.append(float(row[2]))
        val_z.append(float(row[3]))
        yaw.append(row[4])
        ax.scatter(val_x[-1],val_y[-1],val_z[-1],c='b',marker='^')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()

      
