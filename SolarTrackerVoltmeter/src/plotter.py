import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial
import time

# initialize serial port
ser = serial.Serial()
ser.port = 'COM11'  # Arduino serial port
ser.baudrate = 115200
ser.timeout = 10  # specify timeout when using readline()
ser.open()
initial_time = time.time()
if ser.is_open == True:
    print("\nAll right, serial port now open. Configuration:\n")
    print(ser, "\n")  # print serial parameters

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
timestamps = []
voltages = []  # store relative frequency here
currents = []
powers = []


# This function is called periodically from FuncAnimation
def animate(i, timestamp, voltage, current, power):

    # Acquire and parse data from serial port
    while ser.inWaiting():
        line = ser.readline()  # ascii
        line = line.decode("utf8")
        line_as_list = line.split(',')
        v = float(line_as_list[0])

        # Add x and y to lists
        voltage.append(v)
        timestamp.append(time.time() - initial_time)

    # Limit x and y lists to 20 items

    # Draw x and y lists
    ax.clear()
    ax.plot(timestamp, voltages, label="Voltage vs. Time")



# Set up plot to call animate() function periodically
ser.flushInput()
ani = animation.FuncAnimation(fig, animate, fargs=(timestamps, voltages, currents, powers), interval=10)
# Format plot
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.30)
plt.ylabel("Voltage (V)")
plt.axis([0, None, None, None])  # Use for arbitrary number of trials
plt.show()
