Очень сложно, какие-то вещи получилось уловить, но здесь реальная архитектура. 
Выделены отдельные роли, каждая отвечает за свои задачи.  
Интересен сам переход с модели состояния, где нам как бы и не важно было какие изменения происходили,
на его историю и "снимки" этой истории.  
Также постарался сохранить независимым ядро, но уже не знаю насколько это является сейчас значимым.
В эталоне логика выполнятся в самом Event Sourcing. 

Забавно, что имеющиеся минусы в количестве гораздо больше, чем в предыдущих стилях. 
Но это и совершенно другой уровень Системы. К тому же эти минусы начинают более наглядно говорить об особенностях системы.
Всё же пока это выглядит чем-то слишком сильным и сложным и далёким от решения задач повседневности

Курс начинает напоминать высшие уровни задач по SQL=)

```python
from dataclasses import dataclass
from typing import Protocol

import pure_robot


def silent_transfer(message: str) -> None:
    pass


def create_initial_state() -> pure_robot.RobotState:
    return pure_robot.RobotState(
        x=0.0,
        y=0.0,
        angle=0,
        cleaning_mode=pure_robot.WATER
    )


class Event(Protocol):
    robot_id: str


class ResultEvent(Protocol):
    robot_id: str

    def apply(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        pass


class Command(Protocol):
    robot_id: str

    def to_event(self) -> Event | None:
        pass


@dataclass(frozen=True)
class MoveRequestedEvent:
    robot_id: str
    distance: int


@dataclass(frozen=True)
class TurnRequestedEvent:
    robot_id: str
    angle: int


@dataclass(frozen=True)
class CleaningModeChangeRequestedEvent:
    robot_id: str
    mode: str


@dataclass(frozen=True)
class StartRequestedEvent:
    robot_id: str


@dataclass(frozen=True)
class StopRequestedEvent:
    robot_id: str


@dataclass(frozen=True)
class RobotMovedEvent:
    robot_id: str
    distance: int

    def apply(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.move(
            silent_transfer,
            self.distance,
            state
        )


@dataclass(frozen=True)
class RobotTurnedEvent:
    robot_id: str
    angle: int

    def apply(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.turn(
            silent_transfer,
            self.angle,
            state
        )


@dataclass(frozen=True)
class RobotCleaningModeChangedEvent:
    robot_id: str
    mode: str

    def apply(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.set_state(
            silent_transfer,
            self.mode,
            state
        )


@dataclass(frozen=True)
class RobotStartedEvent:
    robot_id: str

    def apply(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.start(
            silent_transfer,
            state
        )


@dataclass(frozen=True)
class RobotStoppedEvent:
    robot_id: str

    def apply(self, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.stop(
            silent_transfer,
            state
        )


@dataclass(frozen=True)
class MoveCommand:
    robot_id: str
    distance: int

    def to_event(self) -> Event | None:
        if self.distance <= 0:
            return None

        return MoveRequestedEvent(
            robot_id=self.robot_id,
            distance=self.distance
        )


@dataclass(frozen=True)
class TurnCommand:
    robot_id: str
    angle: int

    def to_event(self) -> Event | None:
        return TurnRequestedEvent(
            robot_id=self.robot_id,
            angle=self.angle
        )


@dataclass(frozen=True)
class SetStateCommand:
    robot_id: str
    mode: str

    def to_event(self) -> Event | None:
        if self.mode not in (
                pure_robot.WATER,
                pure_robot.SOAP,
                pure_robot.BRUSH
        ):
            return None

        return CleaningModeChangeRequestedEvent(
            robot_id=self.robot_id,
            mode=self.mode
        )


@dataclass(frozen=True)
class StartCommand:
    robot_id: str

    def to_event(self) -> Event | None:
        return StartRequestedEvent(
            robot_id=self.robot_id
        )


@dataclass(frozen=True)
class StopCommand:
    robot_id: str

    def to_event(self) -> Event | None:
        return StopRequestedEvent(
            robot_id=self.robot_id
        )


class EventProcessor(Protocol):
    def process(
            self,
            event: Event,
            event_store: "EventStore"
    ) -> None:
        pass


class EventStore:
    def __init__(self) -> None:
        self.events: list[Event] = []
        self.processors: list[EventProcessor] = []

    def subscribe(self, processor: EventProcessor) -> None:
        self.processors.append(processor)

    def append(self, event: Event) -> None:
        self.events.append(event)

        for processor in self.processors:
            processor.process(event, self)

    def get_events(self, robot_id: str) -> list[Event]:
        return [
            event
            for event in self.events
            if event.robot_id == robot_id
        ]

    def get_result_events(self, robot_id: str) -> list[ResultEvent]:
        result_events: list[ResultEvent] = []

        for event in self.get_events(robot_id):
            if hasattr(event, "apply"):
                result_events.append(event)

        return result_events


def rebuild_state(events: list[ResultEvent]) -> pure_robot.RobotState:
    state = create_initial_state()

    for event in events:
        state = event.apply(state)

    return state


class CommandHandler:
    def __init__(self, event_store: EventStore) -> None:
        self.event_store = event_store

    def handle(self, command: Command) -> None:
        event = command.to_event()

        if event is not None:
            self.event_store.append(event)


class MoveProcessor:
    def process(self, event: Event, event_store: EventStore) -> None:
        if not isinstance(event, MoveRequestedEvent):
            return

        past_result_events = event_store.get_result_events(event.robot_id)
        current_state = rebuild_state(past_result_events)

        event_store.append(
            RobotMovedEvent(
                robot_id=event.robot_id,
                distance=event.distance
            )
        )


class TurnProcessor:
    def process(self, event: Event, event_store: EventStore) -> None:
        if not isinstance(event, TurnRequestedEvent):
            return

        event_store.append(
            RobotTurnedEvent(
                robot_id=event.robot_id,
                angle=event.angle
            )
        )


class CleaningModeProcessor:
    def process(self, event: Event, event_store: EventStore) -> None:
        if not isinstance(event, CleaningModeChangeRequestedEvent):
            return

        past_result_events = event_store.get_result_events(event.robot_id)
        current_state = rebuild_state(past_result_events)

        if current_state.cleaning_mode == event.mode:
            return

        event_store.append(
            RobotCleaningModeChangedEvent(
                robot_id=event.robot_id,
                mode=event.mode
            )
        )


class StartProcessor:
    def process(self, event: Event, event_store: EventStore) -> None:
        if not isinstance(event, StartRequestedEvent):
            return

        event_store.append(
            RobotStartedEvent(
                robot_id=event.robot_id
            )
        )


class StopProcessor:
    def process(self, event: Event, event_store: EventStore) -> None:
        if not isinstance(event, StopRequestedEvent):
            return

        event_store.append(
            RobotStoppedEvent(
                robot_id=event.robot_id
            )
        )
```

```python
from stream_robot import *


event_store = EventStore()

event_store.subscribe(MoveProcessor())
event_store.subscribe(TurnProcessor())
event_store.subscribe(CleaningModeProcessor())
event_store.subscribe(StartProcessor())
event_store.subscribe(StopProcessor())

command_handler = CommandHandler(event_store)

robot_id = "robot-1"

command_handler.handle(MoveCommand(robot_id, 100))
command_handler.handle(TurnCommand(robot_id, -90))
command_handler.handle(SetStateCommand(robot_id, "soap"))
command_handler.handle(StartCommand(robot_id))
command_handler.handle(MoveCommand(robot_id, 50))
command_handler.handle(StopCommand(robot_id))

print("Events:")
for event in event_store.get_events(robot_id):
    print(event)

result_events = event_store.get_result_events(robot_id)
final_state = rebuild_state(result_events)

print("Final state:")
print(final_state)
```