

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

        if cmd == 'start':
            return f'START WITH {self.cleaning_mode}'

        if cmd == 'stop':
            return 'STOP'


    def run(self, commands: list[str]) -> list[str]:
        results = []
        for command in commands:
            result = self.execute(command)
            print(result)
            results.append(result)

        return results




# - направления как все градусы
# - валидация на команды и значения
# - рефакторинг структуры