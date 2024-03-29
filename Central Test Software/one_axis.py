import time
from typing import Union

import serial

from message import *

panelSerial = serial.Serial()
panelSerial.port = 'COM7'
panelSerial.baudrate = 38400
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
    if line.startswith(b'?'):
        frame = PanelData()
        frame.deserialize(line)
        return frame


# while True:
#     pan, tilt = input().split(" ")
#     move_panel(ServoPos(pan, tilt))
#
#     frame = get_panel_data()
#     print(frame.tilt, frame.pan)
#     time.sleep(0.01)

f = open("data/one-axis.txt", "w+")

K = 60
for phi in range(K, -K -1, -3):
    move_panel(ServoPos(0, phi))
    frame = get_panel_data()
    if frame is None:
        phi -= 1
        continue
    s = str(phi) + "," + str(frame.panel_v) + "," + str(frame.photo_tl) + "," + str(frame.photo_tr) + "," + str(
        frame.photo_bl) + "," + str(frame.photo_br)
    f.write(s + "\n")
    print(s)
    time.sleep(0.6)
f.close()
