from dataclasses import dataclass
from typing import List, Protocol, Any
from enum import Enum
import math


# Состояние робота
@dataclass
class RobotState:
    x: float
    y: float
    angle: float
    state: int


# Режим работы
class CleaningMode(Enum):
    WATER = 1
    SOAP = 2
    BRUSH = 3


# Протокол для команд
class Command(Protocol):
    def execute(self, state: RobotState) -> RobotState:
        pass

    def log(self) -> str:
        pass


# Конкретные команды
@dataclass
class MoveCommand:
    distance: float

    def execute(self, state: RobotState) -> RobotState:
        angle_rads = state.angle * (math.pi / 180)
        return RobotState(
            x=state.x + self.distance * math.cos(angle_rads),
            y=state.y + self.distance * math.sin(angle_rads),
            angle=state.angle,
            state=state.state
        )

    def log(self) -> str:
        return f'MOVE {self.distance}'


@dataclass
class TurnCommand:
    angle: float

    def execute(self, state: RobotState) -> RobotState:
        return RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle + self.angle,
            state=state.state
        )

    def log(self) -> str:
        return f'TURN {self.angle}'

@dataclass
class SetStateCommand:
    new_state: CleaningMode

    def execute(self, state: RobotState) -> RobotState:
        return RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle,
            state=self.new_state.value
        )

    def log(self) -> str:
        return f'SET_STATE {self.new_state.name}'

@dataclass
class StartCommand:
    def execute(self, state: RobotState) -> RobotState:
        return state

    def log(self) -> str:
        return f'START'

@dataclass
class StopCommand:
    def execute(self, state: RobotState) -> RobotState:
        return state

    def log(self) -> str:
        return 'STOP'

# Исполнитель команд
class CommandExecutor:
    def __init__(self):
        self.commands: List[Command] = []

    def add_command(self, command: Command):
        self.commands.append(command)

    def execute_all(self, initial_state: RobotState) -> tuple[RobotState, List[str]]:
        current_state = initial_state
        logs = []

        for cmd in self.commands:
            logs.append(cmd.log())
            current_state = cmd.execute(current_state)

        return current_state, logs

# Пример использования
def main():
    # Создаем исполнителя
    executor = CommandExecutor()

    # Добавляем команды
    executor.add_command(MoveCommand(100))
    executor.add_command(TurnCommand(-90))
    executor.add_command(SetStateCommand(CleaningMode.SOAP))
    executor.add_command(StartCommand())
    executor.add_command(MoveCommand(50))
    executor.add_command(StopCommand())

    # Выполняем все команды
    initial_state = RobotState(0.0, 0.0, 0, CleaningMode.WATER.value)
    final_state, logs = executor.execute_all(initial_state)

    # Выводим результаты
    print("Final state:", final_state)
    print("Command log:", logs)