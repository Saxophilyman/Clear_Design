from cleaner_interface import CleanerInterface


class CommandExecutor:
    def __init__(self, cleaner: CleanerInterface):
        self.cleaner = cleaner

    def execute(self, command: str) -> str:
        parts = command.split()
        cmd = parts[0]

        if cmd == "move":
            distance = int(parts[1])
            return self.cleaner.move(distance)

        if cmd == "turn":
            angle = int(parts[1])
            return self.cleaner.turn(angle)

        if cmd == "set":
            mode = parts[1]
            return self.cleaner.set_cleaning_mode(mode)

        if cmd == "start":
            return self.cleaner.start_cleaning()

        if cmd == "stop":
            return self.cleaner.stop_cleaning()

        raise ValueError(f"Неизвестная команда: {command}")
