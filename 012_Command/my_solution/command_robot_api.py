from dataclasses import dataclass
from typing import Callable, Protocol

import pure_robot

TransferFunction = Callable[[str], None]


# Интерфейс на всех
class RobotCommand(Protocol):
    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        pass


@dataclass(frozen=True)
class MoveCommand:
    distance: int

    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.move(transfer, self.distance, state)


@dataclass(frozen=True)
class TurnCommand:
    angle: int

    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.turn(transfer, self.angle, state)


@dataclass(frozen=True)
class SetStateCommand:
    mode: str

    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.set_state(transfer, self.mode, state)


@dataclass(frozen=True)
class StartCommand:
    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.start(transfer, state)


@dataclass(frozen=True)
class StopCommand:
    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.stop(transfer, state)


class RobotCommandApi:
    transfer: TransferFunction

    def __init__(self) -> None:
        self.transfer = transfer_to_cleaner

    def execute(self, commands: list[RobotCommand]) -> pure_robot.RobotState:
        state = pure_robot.RobotState(
            x=0.0,
            y=0.0,
            angle=0,
            cleaning_mode=pure_robot.WATER)

        # условный fold
        for command in commands:
            state = command.execute(self.transfer, state)

        return state

def transfer_to_cleaner(message: str) -> None:
    print(message)

api = RobotCommandApi()