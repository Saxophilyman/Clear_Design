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
        with self._lock:
            self._events.extend(events)
            for event in events:
                for subscriber in self._subscribers:
                    try:
                        subscriber(event)
                    except Exception as e:
                        print(f"Error in subscriber: {e}")

    def get_all_events(self) -> List[Event]:
        with self._lock:
            return self._events.copy()

    def get_events_for_robot(self, robot_id: str) -> List[Event]:
        with self._lock:
            return [e for e in self._events if hasattr(e, 'robot_id') and e.robot_id == robot_id]

    def subscribe(self, callback: Callable[[Event], None]) -> None:
        self._subscribers.append(callback)


class StateProjector:
    def __init__(self, initial_state: RobotState):
        self._initial_state = initial_state

    def project_state(self, robot_id: str, events: List[Event]) -> RobotState:
        current_state = self._initial_state

        for event in events:
            if not hasattr(event, 'robot_id') or event.robot_id != robot_id:
                continue

            if isinstance(event, RobotMovedEvent):
                current_state = current_state.with_changes(x=event.new_x, y=event.new_y)
            elif isinstance(event, RobotTurnedEvent):
                current_state = current_state.with_changes(angle=event.new_angle)
            elif isinstance(event, RobotStateChangedEvent):
                current_state = current_state.with_changes(state=event.new_state)
            return current_state


class CommandHandler:
    def __init__(self, event_store: EventStore):
        self._event_store = event_store

    def handle_command(self, robot_id: str, command: Command) -> None:
        events = command.to_events(robot_id)
        self._event_store.append_events(events)


class EventProcessor(ABC):
    def __init__(self, event_store: EventStore, state_projector: StateProjector):
        self._event_store = event_store
        self._state_projector = state_projector
        self._event_store.subscribe(self._handle_event)

    @abstractmethod
    def _handle_event(self, event: Event) -> None:
        pass

    def _get_current_state(self, robot_id: str) -> RobotState:
        all_events = self._event_store.get_events_for_robot(robot_id)
        result_events = [e for e in all_events if
                         isinstance(e, (RobotMovedEvent, RobotTurnedEvent, RobotStateChangedEvent))]
        return self._state_projector.project_state(robot_id, result_events)

    def _emit_events(self, events: List[Event]) -> None:
        if events:
            self._event_store.append_events(events)


class MovementProcessor(EventProcessor):
    def _handle_event(self, event: Event) -> None:
        if isinstance(event, MoveRequestedEvent):
            self._handle_move_request(event)
        elif isinstance(event, TurnRequestedEvent):
            self._handle_turn_request(event)

    def _handle_move_request(self, event: MoveRequestedEvent) -> None:
        print(f"[MovementProcessor] Processing move request for robot {event.robot_id}")

        current_state = self._get_current_state(event.robot_id)

        angle_rads = current_state.angle * (math.pi / 180)
        new_x = current_state.x + event.distance * math.cos(angle_rads)
        new_y = current_state.y + event.distance * math.sin(angle_rads)

        result_event = RobotMovedEvent(
            robot_id=event.robot_id,
            old_x=current_state.x,
            old_y=current_state.y,
            new_x=new_x,
            new_y=new_y,
            distance=event.distance
        )

        self._emit_events([result_event])

    def _handle_turn_request(self, event: TurnRequestedEvent) -> None:
        print(f"[MovementProcessor] Processing turn request for robot {event.robot_id}")

        current_state = self._get_current_state(event.robot_id)
        new_angle = current_state.angle + event.angle

        result_event = RobotTurnedEvent(
            robot_id=event.robot_id,
            old_angle=current_state.angle,
            new_angle=new_angle
        )

        self._emit_events([result_event])


class StateProcessor(EventProcessor):
    def _handle_event(self, event: Event) -> None:
        if isinstance(event, StateChangeRequestedEvent):
            self._handle_state_change_request(event)
        elif isinstance(event, StartRequestedEvent):
            self._handle_start_request(event)
        elif isinstance(event, StopRequestedEvent):
            self._handle_stop_request(event)

    def _handle_state_change_request(self, event: StateChangeRequestedEvent) -> None:
        print(f"[StateProcessor] Processing state change request for robot {event.robot_id}")

        current_state = self._get_current_state(event.robot_id)

        result_event = RobotStateChangedEvent(
            robot_id=event.robot_id,
            old_state=current_state.state,
            new_state=event.new_state.value
        )

        self._emit_events([result_event])

    def _handle_start_request(self, event: StartRequestedEvent) -> None:
        print(f"[StateProcessor] Processing start request for robot {event.robot_id}")

        result_event = RobotStartedEvent(robot_id=event.robot_id)
        self._emit_events([result_event])

    def _handle_stop_request(self, event: StopRequestedEvent) -> None:
        print(f"[StateProcessor] Processing stop request for robot {event.robot_id}")

        result_event = RobotStoppedEvent(robot_id=event.robot_id)
        self._emit_events([result_event])


class LoggingProcessor(EventProcessor):
    def _handle_event(self, event: Event) -> None:
        print(f"[LoggingProcessor] Event logged: {event.get_event_type()}")
