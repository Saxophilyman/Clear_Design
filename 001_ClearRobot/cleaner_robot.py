

class RobotController:
    def __init__(self):
        self.x = 0
        self.y = 0

    def execute(self, command: str) -> str:
        parts = command.split()
        distance = int(parts[1])
        self.x += distance
        return f'POS {self.x},{self.y}'

    # Move (двигаться вперед на заданное число метров),
    # Turn (поворот на месте на заданный угол в градусах),
    # Set (выбрать одно из трёх устройств очистки:
    #  - полив водой,
    #  - полив мыльной пеной,
    #  - чистка метлой),
    # Start (включить устройство очистки)
    # Stop (выключить устройство очистки).