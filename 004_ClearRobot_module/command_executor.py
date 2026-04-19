from robot import Robot


class CommandExecutor:
    def __init__(self, robot: Robot):
        self.robot = robot

    def execute(self, command: str) -> str:
        parts = command.split()
        cmd = parts[0]

        if cmd == "move":
            distance = int(parts[1])
            return self.robot.move(distance)

        if cmd == "turn":
            angle = int(parts[1])
            return self.robot.turn(angle)

        if cmd == "set":
            mode = parts[1]
            return self.robot.set_cleaning_mode(mode)

        if cmd == "start":
            return self.robot.start_cleaning()

        if cmd == "stop":
            return self.robot.stop_cleaning()

        raise ValueError(f"Неизвестная команда: {command}")
