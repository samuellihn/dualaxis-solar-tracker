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


while True:
    pan, tilt = input().split(" ")
    move_panel(ServoPos(pan, tilt))

    frame = get_panel_data()
    time.sleep(0.01)
