

class RobotController:
    def execute(self, command: str) -> str:
        parts = command.split()
        distance = parts[1]
        return f'POS {distance},0'