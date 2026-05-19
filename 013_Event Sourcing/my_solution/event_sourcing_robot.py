from dataclasses import dataclass
from typing import Protocol

import pure_robot


def create_initial_state() -> pure_robot.RobotState:
    return pure_robot.RobotState(
        x=0.0,
        y=0.0,
        angle=0,
        cleaning_mode=pure_robot.WATER
    )


def transfer_mes(message: str) -> None:
    pass


class RobotEvent(Protocol):
    robot_id: str

    def apply(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        pass


class RobotCommand(Protocol):
    robot_id: str

    def decide(self, state: pure_robot.RobotState) -> list[RobotEvent]:
        pass


@dataclass(frozen=True)
class RobotMovedEvent:
    robot_id: str
    distance: int

    def apply(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.move(transfer_mes, self.distance, state)


@dataclass(frozen=True)
class RobotTurnedEvent:
    robot_id: str
    angle: int

    def apply(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.turn(transfer_mes, self.angle, state)


@dataclass(frozen=True)
class RobotSetCleaningModeChangedEvent:
    robot_id: str
    mode: str

    def apply(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.set_state(transfer_mes, self.mode, state)


@dataclass(frozen=True)
class RobotStartedEvent:
    robot_id: str

    def apply(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.start(transfer_mes, state)


@dataclass(frozen=True)
class RobotStoppedEvent:
    robot_id: str

    def apply(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.stop(transfer_mes, state)


@dataclass(frozen=True)
class MoveCommand:
    robot_id: str
    distance: int

    def decide(self, state: pure_robot.RobotState) -> list[RobotEvent]:
        if self.distance <= 0:
            return []

        return [RobotMovedEvent(robot_id=self.robot_id, distance=self.distance)]


@dataclass(frozen=True)
class TurnCommand:
    robot_id: str
    angle: int

    def decide(self, state: pure_robot.RobotState) -> list[RobotEvent]:
        return [RobotTurnedEvent(robot_id=self.robot_id, angle=self.angle)]


@dataclass(frozen=True)
class SetStateCommand:
    robot_id: str
    mode: str

    def decide(self, state: pure_robot.RobotState) -> list[RobotEvent]:
        if self.mode not in (
                pure_robot.WATER,
                pure_robot.SOAP,
                pure_robot.BRUSH
        ):
            return []

        if state.cleaning_mode == self.mode:
            return []

        return [RobotSetCleaningModeChangedEvent(robot_id=self.robot_id, mode=self.mode)]


@dataclass(frozen=True)
class StartCommand:
    robot_id: str

    def decide(self, state: pure_robot.RobotState) -> list[RobotEvent]:
        return [RobotStartedEvent(robot_id=self.robot_id)]


@dataclass(frozen=True)
class StopCommand:
    robot_id: str

    def decide(self, state: pure_robot.RobotState) -> list[RobotEvent]:
        return [RobotStoppedEvent(robot_id=self.robot_id)]


class EventStore:
    def __init__(self) -> None:
        self.events: list[RobotEvent] = []

    def append(self, events: list[RobotEvent]) -> None:
        self.events.extend(events)

    def get_events(self, robot_id: str) -> list[RobotEvent]:
        return [
            event
            for event in self.events
            if event.robot_id == robot_id
        ]


def rebuild_state(events: list[RobotEvent]) -> pure_robot.RobotState:
    state = create_initial_state()

    for event in events:
        state = event.apply(state)

    return state


class CommandHandler:
    def __init__(self, event_store: EventStore) -> None:
        self.event_store = event_store

    def handle(self, command: RobotCommand) -> list[RobotEvent]:
        pass_events = self.event_store.get_events(command.robot_id)
        current_state = rebuild_state(pass_events)
        new_events = command.decide(current_state)
        self.event_store.append(new_events)
        return new_events
