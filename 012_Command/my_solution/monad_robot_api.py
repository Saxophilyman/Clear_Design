from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

import pure_robot

# настраиваем типизацию
T = TypeVar("T")
U = TypeVar("U")

TransferFunction = Callable[[str], None]
# состояние, результат+новое состояние
StateFunction = Callable[[pure_robot.RobotState], tuple[T, pure_robot.RobotState]]


@dataclass(frozen=True)
class StateMonad(Generic[T]):
    run: StateFunction[T]

    # строит вычисление
    def bind(self, next_function: Callable[[T], "StateMonad[U]"]) -> "StateMonad[U]":
        def new_run(state: pure_robot.RobotState) -> tuple[U, pure_robot.RobotState]:
            value, new_state = self.run(state)
            next_monad = next_function(value)
            return next_monad.run(new_state)

        return StateMonad(new_run)

    def __rshift__(self, next_function: Callable[[T], "StateMonad[U]"]) -> "StateMonad[U]":
        return self.bind(next_function)


# начальная команда
def unit(value: T) -> StateMonad[T]:
    def run(state: pure_robot.RobotState) -> tuple[T, pure_robot.RobotState]:
        return value, state

    return StateMonad(run)


def move(transfer: TransferFunction, distance: int) -> StateMonad[pure_robot.RobotState]:
    def run(state: pure_robot.RobotState) -> tuple[pure_robot.RobotState, pure_robot.RobotState]:
        new_state = pure_robot.move(transfer, distance, state)
        return new_state, new_state

    return StateMonad(run)


def turn(transfer: TransferFunction, angle: int) -> StateMonad[pure_robot.RobotState]:
    def run(state: pure_robot.RobotState) -> tuple[pure_robot.RobotState, pure_robot.RobotState]:
        new_state = pure_robot.turn(transfer, angle, state)
        return new_state, new_state

    return StateMonad(run)


def set_state(transfer: TransferFunction, mode: str) -> StateMonad[pure_robot.RobotState]:
    def run(state: pure_robot.RobotState) -> tuple[pure_robot.RobotState, pure_robot.RobotState]:
        new_state = pure_robot.set_state(transfer, mode, state)
        return new_state, new_state

    return StateMonad(run)


def start(transfer: TransferFunction) -> StateMonad[pure_robot.RobotState]:
    def run(state: pure_robot.RobotState) -> tuple[pure_robot.RobotState, pure_robot.RobotState]:
        new_state = pure_robot.start(transfer, state)
        return new_state, new_state

    return StateMonad(run)


def stop(transfer: TransferFunction) -> StateMonad[pure_robot.RobotState]:
    def run(state: pure_robot.RobotState) -> tuple[pure_robot.RobotState, pure_robot.RobotState]:
        new_state = pure_robot.stop(transfer, state)
        return new_state, new_state

    return StateMonad(run)
