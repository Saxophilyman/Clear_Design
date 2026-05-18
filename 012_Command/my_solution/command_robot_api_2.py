from dataclasses import dataclass
from typing import Callable, Protocol
import pure_robot

WATER = pure_robot.WATER
SOAP = pure_robot.SOAP
BRUSH = pure_robot.BRUSH

TransferFunction = Callable[[str], None]


class RobotCommand(Protocol):
    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        pass

    def log(self) -> str:
        pass


@dataclass(frozen=True)
class MoveCommand:
    distance: int

    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.move(transfer, self.distance, state)

    def log(self) -> str:
        return f'MOVE {self.distance}'


@dataclass(frozen=True)
class TurnCommand:
    angle: int

    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.turn(transfer, self.angle, state)

    def log(self) -> str:
        return f'TURN {self.angle}'


@dataclass(frozen=True)
class SetStateCommand:
    mode: str

    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.set_state(transfer, self.mode, state)

    def log(self) -> str:
        return f"SET_STATE {self.mode}"


@dataclass(frozen=True)
class StartCommand:

    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.start(transfer, state)

    def log(self) -> str:
        return "START"


@dataclass(frozen=True)
class StopCommand:

    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.stop(transfer, state)

    def log(self) -> str:
        return "STOP"


class CommandExecutor:
    transfer: TransferFunction
    commands: list[RobotCommand]

    def __init__(self) -> None:
        self.commands = []
        self.transfer = self.transfer_to_cleaner

    def add_command(self, command: RobotCommand) -> None:
        self.commands.append(command)

    def execute_all(self, initial_state: pure_robot.RobotState) -> tuple[pure_robot.RobotState, list[str]]:
        current_state = initial_state
        logs: list[str] = []

        for command in self.commands:
            logs.append(command.log())

            current_state = command.execute(self.transfer, current_state)

        return current_state, logs

    def transfer_to_cleaner(self, message: str) -> None:
        print(message)


def create_initial_state() -> pure_robot.RobotState:
    return pure_robot.RobotState(
        x=0,
        y=0,
        angle=0,
        cleaning_mode=WATER
    )
