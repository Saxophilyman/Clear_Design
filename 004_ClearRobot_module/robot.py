import math


class Robot:
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.angle = 0
        self.cleaning_mode = self.WATER

    def move(self, distance: int) -> str:
        angle_rads = math.radians(self.angle)
        self.x += distance * math.cos(angle_rads)
        self.y += distance * math.sin(angle_rads)

        self.x = round(self.x)
        self.y = round(self.y)

        return f"POS {int(self.x)},{int(self.y)}"

    def turn(self, angle: int) -> str:
        self.angle += angle
        return f"ANGLE {self.angle}"

    def set_cleaning_mode(self, mode: str) -> str:
        if mode not in (self.WATER, self.SOAP, self.BRUSH):
            raise ValueError(f"Неизвестный режим очистки: {mode}")

        self.cleaning_mode = mode
        return f"STATE {self.cleaning_mode}"

    def start_cleaning(self) -> str:
        return f"START WITH {self.cleaning_mode}"

    @staticmethod
    def stop_cleaning() -> str:
        return "STOP"