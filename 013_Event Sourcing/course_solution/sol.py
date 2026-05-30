from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import math
from typing import Protocol, List, Dict, Optional


@dataclass
class RobotState:
    x: float
    y: float
    angle: float
    state: int


class CleaningMode(Enum):
    WATER = 1
    SOAP = 2
    BRUSH = 3


class Event(ABC):
    @abstractmethod
    def apply(self, state: RobotState) -> RobotState:
        pass

    @abstractmethod
    def get_event_type(self) -> str:
        pass


@dataclass
class RobotMovedEvent(Event):
    distance: float

    def apply(self, state: RobotState) -> RobotState:
        angle_rads = state.angle * (math.pi / 180.0)
        return RobotState(
            x=state.x + self.distance * math.cos(angle_rads),
            y=state.y + self.distance * math.sin(angle_rads),
            angle=state.angle,
            state=state.state
        )

    def get_event_type(self) -> str:
        return f'ROBOT_MOVED {self.distance}'


@dataclass
class RobotTurnedEvent(Event):
    angle: float

    def apply(self, state: RobotState) -> RobotState:
        return RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle + self.angle,
            state=state.state
        )

    def get_event_type(self) -> str:
        return f'ROBOT_TURNED {self.angle}'


@dataclass
class RobotStateChangeEvent(Event):
    new_state: CleaningMode

    def apply(self, state: RobotState) -> RobotState:
        return RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle,
            state=self.new_state.value
        )

    def get_event_type(self) -> str:
        return f'ROBOT_STATE_CHANGE {self.new_state.name}'


@dataclass
class RobotStartedEvent(Event):
    def apply(self, state: RobotState) -> RobotState:
        return state

    def get_event_type(self) -> str:
        return 'ROBOT_STARTED'


@dataclass
class RobotStoppedEvent(Event):
    def apply(self, state: RobotState) -> RobotState:
        return state

    def get_event_type(self) -> str:
        return 'ROBOT_STOPPED'


class Command(Protocol):
    def handle(self, current_state: RobotState) -> List[Event]:
        pass

    def get_command_type(self) -> str:
        pass


@dataclass
class MovedCommand:
    distance: float

    def handle(self, current_state: RobotState) -> List[Event]:
        return [RobotMovedEvent(self.distance)]

    def get_command_type(self) -> str:
        return f'MOVE {self.distance}'


@dataclass
class TurnCommand:
    angle: float

    def handle(self, current_state: RobotState) -> List[Event]:
        return [RobotTurnedEvent(self.angle)]

    def get_command_type(self) -> str:
        return f'TURN {self.angle}'


@dataclass
class SetStateCommand:
    new_state: CleaningMode

    def handle(self, current_state: RobotState) -> List[Event]:
        return [RobotStateChangeEvent(self.new_state)]

    def get_command_type(self) -> str:
        return f'SET_STATE {self.new_state.name}'


@dataclass
class StartCommand:
    def handle(self, current_state: RobotState) -> List[Event]:
        return [RobotStartedEvent()]

    def get_command_type(self) -> str:
        return 'START'


@dataclass
class StopCommand:
    def handle(self, current_state: RobotState) -> List[Event]:
        return [RobotStoppedEvent()]

    def get_command_type(self) -> str:
        return 'STOP'


class EventStore:
    def __init__(self):
        self._events: Dict[str, List[Event]] = {}

    def append_events(self, robot_id: str, events: List[Event]) -> None:
        if robot_id not in self._events:
            self._events[robot_id] = []
        self._events[robot_id].extend(events)

    def get_events(self, robot_id: str) -> List[Event]:
        return self._events.get(robot_id, [])

    def get_events_from_version(self, robot_id: str, from_version: int) -> List[Event]:
        events = self.get_events(robot_id)
        return events[from_version:] if from_version < len(events) else []


class StateProjector:
    def __init__(self, initial_state: RobotState):
        self._initial_state = initial_state

    def project_state(self, events: List[Event]) -> RobotState:
        current_state = self._initial_state
        for event in events:
            current_state = event.apply(current_state)
        return current_state


class CommandHandler:
    def __init__(self, event_store: EventStore, state_projector: StateProjector):
        self._event_store = event_store
        self._state_projector = state_projector

    def handle_command(self, robot_id: str, command: Command) -> RobotState:
        events = self._event_store.get_events(robot_id)
        current_state = self._state_projector.project_state(events)

        new_events = command.handle(current_state)

        if new_events:
            self._event_store.append_events(robot_id, new_events)

        all_events = self._event_store.get_events(robot_id)
        return self._state_projector.project_state(all_events)


class TimeTravel:
    def __init__(self, event_store: EventStore, state_projector: StateProjector):
        self._event_store = event_store
        self._state_projector = state_projector

    def get_state_at_version(self, robot_id: str, version: int) -> Optional[RobotState]:
        events = self._event_store.get_events(robot_id)

        if version < 0 or version > len(events):
            return None

        events_to_apply = events[:version]
        return self._state_projector.project_state(events_to_apply)

    def get_current_version(self, robot_id: str) -> int:
        return len(self._event_store.get_events(robot_id))
