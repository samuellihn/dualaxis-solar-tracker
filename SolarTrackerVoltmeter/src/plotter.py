import csv
import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial
import time
import datetime

from datetime import datetime

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
fig = plt.figure(figsize=(12, 12))
ax1 = fig.add_subplot(3, 1, 1)
ax2 = fig.add_subplot(3, 1, 2, sharex=ax1)
ax3 = fig.add_subplot(3, 1, 3, sharex=ax1)
timestamps = []
voltages = []  # store relative frequency here
currents = []
powers = []
input("to start?")

csv_file = open("../data/tracker_2000ms_96s.csv", "w+", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Timestamp", "Servo Voltage", "Servo Current", "Servo Power"])

# This function is called periodically from FuncAnimation
def animate(i, timestamp, voltage, current, power):
    # Acquire and parse data from serial port
    while ser.inWaiting():
        line = ser.readline()  # ascii
        line = line.decode("utf8")
        line_as_list = line.split(',')
        try:
            v, i, p = map(float, line_as_list)
        except:
            continue
        t = time.time() - initial_time


        # Add x and y to lists
        voltage.append(v)
        current.append(i)
        power.append(p)
        timestamp.append(t)
        csv_writer.writerow([datetime.utcnow(), v, i, p])


    # # Limit x and y lists to 20 items
    voltage = voltage[-1000:]
    power = power[-1000:]
    timestamp = timestamp[-1000:]
    current = current[-1000:]

    # Draw x and y lists
    ax1.clear()
    ax1.plot(timestamp, voltage, label="Voltage vs. Time")
    ax2.clear()
    ax2.plot(timestamp, current, label="Current vs. Time")
    ax3.clear()
    ax3.plot(timestamp, power, label="Power vs. Time")
    ax1.set_title("Voltage")
    ax2.set_title("Current")
    ax3.set_title("Power")


# Set up plot to call animate() function periodically
ser.flushInput()
ani = animation.FuncAnimation(fig, animate, fargs=(timestamps, voltages, currents, powers), interval=40)
# Format plot
plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), rotation=45.0)
plt.subplots_adjust(bottom=0.30)
plt.axis([0, None, None, None])  # Use for arbitrary number of trials
plt.show()
csv_file.close()
