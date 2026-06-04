from dataclasses import dataclass
from typing import List, Protocol, Dict, Callable, Optional
from enum import Enum
import math
from abc import ABC, abstractmethod
import threading
import time


@dataclass
class RobotState:
    x: float
    y: float
    angle: float
    state: int

    def with_changes(self, **kwargs) -> 'RobotState':
        return RobotState(
            x=kwargs.get('x', self.x),
            y=kwargs.get('y', self.y),
            angle=kwargs.get('angle', self.angle),
            state=kwargs.get('state', self.state)
        )


class CleaningMode(Enum):
    WATER = 1
    SOAP = 2
    BRUSH = 3


class Event(ABC):
    @abstractmethod
    def get_event_type(self) -> str:
        pass


@dataclass
class MoveRequestedEvent(Event):
    robot_id: str
    distance: float

    def get_event_type(self) -> str:
        return f'MOVE_REQUESTED {self.distance}'


@dataclass
class TurnRequestedEvent(Event):
    robot_id: str
    angle: float

    def get_event_type(self) -> str:
        return f'TURN_REQUESTED {self.angle}'


@dataclass
class StateChangeRequestedEvent(Event):
    robot_id: str
    new_state: CleaningMode

    def get_event_type(self) -> str:
        return f'STATE_CHANGE_REQUESTED {self.new_state.name}'


@dataclass
class StartRequestedEvent(Event):
    robot_id: str

    def get_event_type(self) -> str:
        return 'START_REQUESTED'


@dataclass
class StopRequestedEvent(Event):
    robot_id: str

    def get_event_type(self) -> str:
        return 'STOP_REQUESTED'


@dataclass
class RobotMovedEvent(Event):
    robot_id: str
    old_x: float
    old_y: float
    new_x: float
    new_y: float
    distance: float

    def get_event_type(self) -> str:
        return f'ROBOT_MOVED from ({self.old_x}, {self.old_y}) to ({self.new_x}, {self.new_y})'


@dataclass
class RobotTurnedEvent(Event):
    robot_id: str
    old_angle: float
    new_angle: float

    def get_event_type(self) -> str:
        return f'ROBOT_TURNED from {self.old_angle} to {self.new_angle}'


@dataclass
class RobotStateChangedEvent(Event):
    robot_id: str
    old_state: int
    new_state: int

    def get_event_type(self) -> str:
        return f'ROBOT_STATE_CHANGED from {self.old_state} to {self.new_state}'


@dataclass
class RobotStartedEvent(Event):
    robot_id: str

    def get_event_type(self) -> str:
        return 'ROBOT_STARTED'


@dataclass
class RobotStoppedEvent(Event):
    robot_id: str

    def get_event_type(self) -> str:
        return 'ROBOT_STOPPED'


class Command(Protocol):
    def to_events(self, robot_id: str) -> List[Event]:
        pass

    def get_command_type(self) -> str:
        pass


@dataclass
class MoveCommand:
    distance: float

    def to_events(self, robot_id: str) -> List[Event]:
        return [MoveRequestedEvent(robot_id, self.distance)]

    def get_command_type(self) -> str:
        return f'MOVE {self.distance}'


@dataclass
class TurnCommand:
    angle: float

    def to_events(self, robot_id: str) -> List[Event]:
        return [TurnRequestedEvent(robot_id, self.angle)]

    def get_command_type(self) -> str:
        return f'TURN {self.angle}'


@dataclass
class SetStateCommand:
    new_state: CleaningMode

    def to_events(self, robot_id: str) -> List[Event]:
        return [StateChangeRequestedEvent(robot_id, self.new_state)]

    def get_command_type(self) -> str:
        return f'SET_STATE {self.new_state.name}'


@dataclass
class StartCommand:
    def to_events(self, robot_id: str) -> List[Event]:
        return [StartRequestedEvent(robot_id)]

    def get_command_type(self) -> str:
        return 'START'


@dataclass
class StopCommand:
    def to_events(self, robot_id: str) -> List[Event]:
        return [StopRequestedEvent(robot_id)]

    def get_command_type(self) -> str:
        return 'STOP'


class EventStore:
    def __init__(self):
        self._events: List[Event] = []
        self._subscribers: List[Callable[[Event], None]] = []
        self._lock = threading.RLock()  # !!! RLock

    def append_events(self, events: List[Event]) -> None:
        with

    def get_all_events(self) -> List[Event]:

    def subscribe(self, callback: Callable[[Event], None]) -> None:


class StateProjector:
    def __init__(self, initial_state: RobotState):

    def project_state(self, robot_id: str, events: List[Event]) -> RobotState:


class CommandHandler:
    def __init__(self, event_store: EventStore):

    def handle_command(self, robot_id: str, command: Command) -> None:


class EventProcessor(ABC):
    def __init__(self, event_store: EventStore, state_projector: StateProjector):

    @abstractmethod
    def _handle_event(self, event: Event) -> None:
        pass

    def _get_current_state(self, robot_id: str) -> RobotState:

    def _emit_events(self, events: List[Event]) -> None:

class MovementProcessor(EventProcessor):
    def _handle_event(self, event: Event) -> None:

    def _handle_move_request(self, event: MoveRequestedEvent) -> None:

    def _handle_turn_request(self, event: TurnRequestedEvent) -> None:

class StateProcessor(EventProcessor):
    def _handle_event(self, event: Event) -> None:

    def _handle_state_change_request(self, event: StateChangeRequestedEvent) -> None:

    def _handle_start_request(self, event: StartRequestedEvent) -> None:

    def _handle_stop_request(self, event: StartRequestedEvent) -> None:

class LoggingProcessor(EventProcessor):
    def _handle_event(self, event: Event) -> None: