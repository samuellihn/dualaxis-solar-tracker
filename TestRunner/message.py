class ServoPos:
    pan: int
    tilt: int

    def __init__(self, pan, tilt):
        self.pan = int(pan)
        self.tilt = int(tilt)

    def serialize(self):
        return bytes(f"{round((self.pan + 135) / 1.5)},{round((self.tilt + 135) / 1.5)}\n", "utf8")

    @staticmethod
    def measure():
        return ServoPos(140, 140)


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
        self.pan *= 1.5
        self.tilt *= 1.5
        self.pan -= 135
        self.tilt -= 135

    def to_csv_row(self):
        return [
            self.panel_v, self.panel_i, self.panel_p,
            self.photo_tr, self.photo_tl, self.photo_br, self.photo_bl,
            self.pan, self.tilt
        ]
