import csv
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
    print(line.decode("utf8"))
    if line.startswith(b'?'):
        frame = PanelData()
        frame.deserialize(line)
        return frame


Y_THRESHOLD = 100
X_THRESHOLD = 100

Y_MIN = -110
Y_MAX = 110
X_MIN = -110
X_MAX = 110

DELAY = 4000

csv_file = open("data/tracker_" + str(DELAY) + "ms_96s.csv", "w+", newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(
    ["Timestamp", "Panel Voltage", "Panel Current", "Panel Power", "TR", "TL", "BR", "BL", "Pan", "Tilt"])

X_INCR = 2
Y_INCR = 2
# Main loop
# if it doesn't move within this amount of frames, assume it's reached a good position
INACTIVE_FRAMES = 5
inactive_countdown = INACTIVE_FRAMES
inactive_amount_ms = DELAY
allowed = True
timeout = 0
time.sleep(4)

move_panel(ServoPos(0, -60))
get_panel_data()
input("to start?")
print("starting")

while True:
    moved_x = True
    moved_y = True
    # Request data
    move_panel(ServoPos(150, 150))
    frame = get_panel_data()

    if frame is None:
        continue

    csv_writer.writerow([datetime.utcnow()] + frame.to_csv_row())

    if not allowed:
        timeout -= 40
        if timeout <= 0:
            allowed = True
            timeout = 0
            inactive_countdown = INACTIVE_FRAMES
        else:
            continue

    # Calculate avg values
    avg_top = (frame.photo_tr + frame.photo_tl) / 2
    avg_bot = (frame.photo_br + frame.photo_bl) / 2
    avg_right = (frame.photo_tr + frame.photo_br) / 2
    avg_left = (frame.photo_tl + frame.photo_bl) / 2

    # Calculate differentials
    y_diff = (avg_top - avg_bot)
    x_diff = (avg_right - avg_left)

    if y_diff > Y_THRESHOLD:
        if frame.tilt < Y_MAX:
            move_panel(ServoPos(150, frame.tilt + Y_INCR))
            get_panel_data()  # flush serial
    elif y_diff < -Y_THRESHOLD:
        if frame.tilt > Y_MIN:
            move_panel(ServoPos(150, frame.tilt - Y_INCR))
            get_panel_data()  # flush serial
    else:
        moved_x = False

    if frame.tilt < 0:
        if x_diff > X_THRESHOLD:
            if frame.pan < X_MAX:
                move_panel(ServoPos(frame.pan + X_INCR, 150))
                get_panel_data()  # flush serial
        elif x_diff < -X_THRESHOLD:
            if frame.pan > X_MIN:
                move_panel(ServoPos(frame.pan - X_INCR, 150))
                get_panel_data()  # flush serial
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

    if not (moved_x or moved_y):
        inactive_countdown -= 1

    if inactive_countdown <= 0:
        allowed = False
        timeout = inactive_amount_ms
    time.sleep(0.04)


csv_file.close()
