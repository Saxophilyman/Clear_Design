

class RobotController:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.cleaning_mode = 'water'

    def execute(self, command: str) -> str:
        parts = command.split()
        cmd = parts[0]

        if cmd == 'move':
            value = int(parts[1])

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
            value = int(parts[1])
            self.angle += value
            return f'ANGLE {self.angle}'

        if cmd == 'set':
            self.cleaning_mode = parts[1]
            return f'STATE {self.cleaning_mode}'


# как определить иные команды?

    # Move (двигаться вперед на заданное число метров),
    # Turn (поворот на месте на заданный угол в градусах),
    # Set (выбрать одно из трёх устройств очистки:
    #  [+] полив водой,
    #  [] полив мыльной пеной,
    #  [] чистка метлой),
    # Start (включить устройство очистки)
    # Stop (выключить устройство очистки).


# - другие команды(3 из 5)
# - направления как все градусы
# - валидация на команды и значения
# - углы либо оптимизировать по 4м направлениям, либо уйти в математику по градусам