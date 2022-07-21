import csv
import math
import time
from typing import Union

import serial

from message import *
from datetime import datetime

panelSerial = serial.Serial()
panelSerial.port = 'COM7'
panelSerial.baudrate = 115200
panelSerial.timeout = 10
panelSerial.open()

initial_time = time.time()
if panelSerial.is_open:
    print(panelSerial)
SLEEP_TIME = 5


def move_panel(position: ServoPos) -> None:
    buf = position.serialize()
    panelSerial.write(buf)


def get_panel_data() -> Union[PanelData, None]:
    line = panelSerial.readline()
    if line.startswith(b'?'):
        frame = PanelData()
        frame.deserialize(line)
        return frame


# LDR differential values to filter out low-amplitude sensor noise
Y_THRESHOLD = 25
X_THRESHOLD = 25

# Mechanical axis inputs
Y_MIN = -110
Y_MAX = 110
X_MIN = -110
X_MAX = 110

# Time between adjustment intervals
DELAY = 40

# Increment to move servo every polling loop
X_INCR = 2
Y_INCR = 2

# if it doesn't move within this amount of frames, assume it's reached a good position
INACTIVE_FRAMES = 5

# csv_file = open("data/tracker_" + str(DELAY) + "ms_96s.csv", "w+", newline='')
# csv_writer = csv.writer(csv_file)
# csv_writer.writerow(
#     ["Timestamp", "Panel Voltage", "Panel Current", "Panel Power", "TR", "TL", "BR", "BL", "Pan", "Tilt"])

# Home servo on initialization
move_panel(ServoPos(0, -60))
get_panel_data()
input("Press ENTER to start: ")
print("Starting trial...")

inactive_countdown = INACTIVE_FRAMES
inactive_amount_ms = DELAY
allowed = True
timeout = 0
time.sleep(4)

# Main loop
while True:
    moved_x = True
    moved_y = True

    # Request data
    move_panel(ServoPos(150, 150))
    frame = get_panel_data()

    if frame is None:
        continue

    mw = round((frame.panel_v * frame.panel_i) * 1000) / 1000
    print(
        f"Voltage: {str(frame.panel_v).rjust(4)} volts, Current: {str(frame.panel_i).rjust(4)} mAmps, Power: {str(mw).rjust(5)}  mWatts")

    # Set DELAY timeout
    if not allowed:
        timeout -= 40
        if timeout <= 0:
            allowed = True
            timeout = 0
            inactive_countdown = INACTIVE_FRAMES
        else:
            continue

    # Calculate average light values for panel
    avg_top = (frame.photo_tr + frame.photo_tl) / 2
    avg_bot = (frame.photo_br + frame.photo_bl) / 2
    avg_right = (frame.photo_tr + frame.photo_br) / 2
    avg_left = (frame.photo_tl + frame.photo_bl) / 2

    # Calculate differential light values
    y_diff = (avg_top - avg_bot)
    x_diff = (avg_right - avg_left)

    # Move servo according to threshold
    if y_diff > Y_THRESHOLD:
        if frame.tilt < Y_MAX:
            move_panel(ServoPos(150, frame.tilt + Y_INCR))
            get_panel_data()  # Flush serial buffer
    elif y_diff < -Y_THRESHOLD:
        if frame.tilt > Y_MIN:
            move_panel(ServoPos(150, frame.tilt - Y_INCR))
            get_panel_data()
    else:
        moved_x = False

    if frame.tilt < 0:
        if x_diff > X_THRESHOLD:
            if frame.pan < X_MAX:
                move_panel(ServoPos(frame.pan + X_INCR, 150))
                get_panel_data()
        elif x_diff < -X_THRESHOLD:
            if frame.pan > X_MIN:
                move_panel(ServoPos(frame.pan - X_INCR, 150))
                get_panel_data()
        else:
            moved_y = False
    else:
        if x_diff > X_THRESHOLD:
            if frame.pan > X_MIN:
                move_panel(ServoPos(frame.pan - X_INCR, 150))
                get_panel_data()  # flush serial
        elif x_diff < -X_THRESHOLD:
            if frame.pan < X_MAX:
                move_panel(ServoPos(frame.pan + X_INCR, 150))
                get_panel_data()  # flush serial
        else:
            moved_y = False

    # If no movement is necessary, assume inactivity (no change in value)
    if not (moved_x or moved_y):
        inactive_countdown -= 1

    if inactive_countdown <= 0:
        allowed = False
        timeout = inactive_amount_ms
    time.sleep(0.04)
