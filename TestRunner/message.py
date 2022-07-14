class ServoPos:
    pan: int
    tilt: int

    def __init__(self, pan, tilt):
        self.pan = pan
        self.tilt = tilt

    def serialize(self):
        return bytes(f"{self.pan},{self.tilt}\n", "utf8")


class PanelData:
    panel_v: float
    panel_i: float
    panel_p: float

    photo_tr: int
    photo_tl: int
    photo_br: int
    photo_bl: int

    pan: int
    tilt: int

    def deserialize(self, data: bytes):
        data = data.decode("ascii")[:-2]
        data = data[1:]
        panel, photo, servo = data.split("|")

        self.panel_v, self.panel_i, self.panel_p = map(float, panel.split(","))
        self.photo_tr, self.photo_tl, self.photo_br, self.photo_bl = map(int, photo.split(","))
        self.pan, self.tilt = map(int, servo.split(","))
