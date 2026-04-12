

class RobotController:
    def __init__(self):
        self.x = 0
        self.y = 0

    def execute(self, command: str) -> str:
        parts = command.split()
        distance = int(parts[1])
        self.x += distance
        return f'POS {self.x},{self.y}'