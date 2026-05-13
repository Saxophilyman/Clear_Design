from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

import pure_robot

T = TypeVar("T")
U = TypeVar("U")

TransferFunction = Callable[[str], None]

StateFunction = Callable[[pure_robot.RobotState], tuple[T, pure_robot.RobotState]]


@dataclass(frozen=True)
class StateMonad(Generic[T]):
    run_function: StateFunction[T]

    def bind(self, next_function: Callable[[T], "StateMonad[U]"]) -> "StateMonad[U]":
        def composed(state: pure_robot.RobotState) -> tuple[U, pure_robot.RobotState]:
            value, new_state = self.run_function(state)
            next_monad = next_function(value)
            return next_monad.run_function(new_state)

        return StateMonad(composed)

    def __rshift__(self, next_monad: "StateMonad[U]") -> "StateMonad[U]":
        return self.bind(lambda _: next_monad)

    def run(self, initial_state: pure_robot.RobotState) -> tuple[T, pure_robot.RobotState]:
        return self.run_function(initial_state)


class RobotApi:
    transfer: TransferFunction
    initial_state: pure_robot.RobotState

    def __init__(self):
        self.transfer = self.transfer_to_cleaner
        self.initial_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

    def transfer_to_cleaner(self, message: str) -> None:
        print(message)

    def move(self, distance: int) -> StateMonad[pure_robot.RobotState]:
        def action(state: pure_robot.RobotState):
            new_state = pure_robot.move(self.transfer, distance, state)
            return new_state, new_state

        return StateMonad(action)

    def turn(self, angle: int) -> StateMonad[pure_robot.RobotState]:
        def action(state: pure_robot.RobotState):
            new_state = pure_robot.turn(self.transfer, angle, state)
            return new_state, new_state

        return StateMonad(action)

    def set_state(self, mode: str) -> StateMonad[pure_robot.RobotState]:
        def action(state: pure_robot.RobotState):
            new_state = pure_robot.set_state(self.transfer, mode, state)
            return new_state, new_state

        return StateMonad(action)

    def start(self) -> StateMonad[pure_robot.RobotState]:
        def action(state: pure_robot.RobotState):
            new_state = pure_robot.start(self.transfer, state)
            return new_state, new_state

        return StateMonad(action)

    def stop(self) -> StateMonad[pure_robot.RobotState]:
        def action(state: pure_robot.RobotState):
            new_state = pure_robot.stop(self.transfer, state)
            return new_state, new_state

        return StateMonad(action)

    def __rshift__(self, next_monad: StateMonad[U]) -> StateMonad[U]:
        return StateMonad(lambda state: (state, state)) >> next_monad

api = RobotApi()