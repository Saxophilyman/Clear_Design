

class RobotController:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0

    def execute(self, command: str) -> str:
        parts = command.split()
        cmd = parts[0]
        value = int(parts[1])

        if cmd == 'move':
        # либо оптимизировать по 4м направлениям, либо уйти в математику по градусам
            if self.angle == 0:
                self.x += value
            elif self.angle == 90:
                self.y += value
            elif self.angle == 180:
                self.x -= value
            elif self.angle == -90:
                self.y -= value

            return f'POS {self.x},{self.y}'

        if cmd == 'turn':
            self.angle += value
            return f'ANGLE {self.angle}'

# как определить иные команды?

    # Move (двигаться вперед на заданное число метров),
    # Turn (поворот на месте на заданный угол в градусах),
    # Set (выбрать одно из трёх устройств очистки:
    #  - полив водой,
    #  - полив мыльной пеной,
    #  - чистка метлой),
    # Start (включить устройство очистки)
    # Stop (выключить устройство очистки).


# - другие команды
# - направления как все градусы