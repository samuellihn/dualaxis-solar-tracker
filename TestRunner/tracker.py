import time
from typing import Union

import serial

from message import *

panelSerial = serial.Serial()
panelSerial.port = 'COM7'
panelSerial.baudrate = 115200
panelSerial.timeout = 10
panelSerial.open()

initial_time = time.time()
if panelSerial.is_open:
    print(panelSerial)


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


Y_THRESHOLD = 15
X_THRESHOLD = 15

Y_MIN = 60
Y_MAX = 120
X_MIN = 60
X_MAX = 120

X_INCR = 1
Y_INCR = 1
# Main loop
while True:
    # Request data
    move_panel(ServoPos(300, 300))
    frame = get_panel_data()

    # Calculate avg values
    avg_top = (frame.photo_tr + frame.photo_tl) / 2
    avg_bot = (frame.photo_br + frame.photo_bl) / 2
    avg_right = (frame.photo_tr + frame.photo_br) / 2
    avg_left = (frame.photo_tl + frame.photo_bl) / 2

    # Calculate differentials
    y_diff = (avg_top - avg_bot)
    x_diff = (avg_right - avg_left)
    total_ldr = sum([avg_top, avg_bot, avg_right, avg_left])

    if y_diff > Y_THRESHOLD:
        if frame.tilt < Y_MAX:
            move_panel(ServoPos(300, frame.tilt + Y_INCR))
    elif y_diff < -Y_THRESHOLD:
        if frame.tilt > Y_MIN:
            move_panel(ServoPos(300, frame.tilt - Y_INCR))

    if x_diff > X_THRESHOLD:
        if frame.pan < X_MAX:
            move_panel(ServoPos(frame.pan + X_INCR, 300))
    elif x_diff < -X_THRESHOLD:
        if frame.pan > X_MIN:
            move_panel(ServoPos(frame.pan - X_INCR, 300))

    time.sleep(0.1)
