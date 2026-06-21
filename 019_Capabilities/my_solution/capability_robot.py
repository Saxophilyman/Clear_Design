from __future__ import annotations
import math
from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable, Mapping, TypeAlias

WATER = "water"
SOAP = "soap"
BRUSH = "brush"


@dataclass(frozen=True)
class _RobotState:
    x: float
    y: float
    angle: int
    mode: str

@dataclass(frozen=True)
class _Resources:
    water: int
    soap: int

@dataclass(frozen=True)
class Result:
    status: str
    message: str


Operation: TypeAlias = Callable[..., tuple[Result, "Capabilities"]]
Capabilities: TypeAlias = Mapping[str, Operation]


def create_robot(water: int = 1, soap: int = 1, transfer: Callable[[str], None] = print) -> Capabilities:
    return _build_capabilities(
        state=_RobotState(
            x=0.0,
            y=0.0,
            angle=0,
            mode=WATER
        ),
        resources=_Resources(
            water=water,
            soap=soap
        ),
        log=[],
        blocked=False,
        transfer=transfer
    )


def _build_capabilities(state: _RobotState, resources: _Resources, log: list[str], blocked: bool,
                        transfer: Callable[[str], None]) -> Capabilities:

    def next_api(new_state: _RobotState, new_resources: _Resources = resources, new_log: list[str] | None = None,
                 new_blocked: bool = blocked) -> Capabilities:
        return _build_capabilities(
            state=new_state,
            resources=new_resources,
            log=log if new_log is None else new_log,
            blocked=new_blocked,
            transfer=transfer
        )

    def emit(status: str, message: str, new_state: _RobotState, new_resources: _Resources = resources, new_blocked: bool = blocked) -> tuple[Result, Capabilities]:
        transfer(message)

        return (
            Result(status, message),
            next_api(
                new_state = new_state,
                new_resources=new_resources,
                new_log=log + [message],
                new_blocked=new_blocked
            )
        )

    def move(distance: int) -> tuple[Result, Capabilities]:
        angle_rads = math.radians(state.angle)

        target_x = state.x + distance * math.cos(angle_rads)
        target_y = state.y + distance * math.sin(angle_rads)

        new_x = max(0, min(100, target_x))
        new_y = max(0, min(100, target_y))

        hit_barrier = target_x != new_x or target_y != new_y

        new_state = _RobotState(
            x=new_x,
            y=new_y,
            angle=state.angle,
            mode=state.mode
        )

        if hit_barrier:
            return emit(
                status="HIT_BARRIER",
                message=f"HIT_BARRIER at ({int(new_x)}, {int(new_y)})",
                new_state=new_state,
                new_blocked=True
            )

        return emit(
            status="MOVE_OK",
            message=f"POS({int(new_x)}, {int(new_y)})",
            new_state=new_state,
            new_blocked=False
        )

    def turn(angle: int) -> tuple[Result, Capabilities]:
        new_state = _RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle + angle,
            mode=state.mode
        )

        return emit(
            status="TURN_OK",
            message=f"ANGLE {new_state.angle}",
            new_state=new_state,
            new_blocked=False
        )

    def set_mode(mode: str) -> tuple[Result, Capabilities]:
        new_state = _RobotState(
            x=state.x,
            y=state.y,
            angle=state.angle,
            mode=mode
        )

        return emit(
            status="STATE_OK",
            message=f"STATE {mode}",
            new_state=new_state
        )

    def start() -> tuple[Result, Capabilities]:
        new_resources = resources

        if state.mode == WATER:
            new_resources = _Resources(
                water=resources.water - 1,
                soap=resources.soap
            )

        elif state.mode == SOAP:
            new_resources = _Resources(
                water=resources.water,
                soap=resources.soap - 1
            )

        return emit(
            status="START_OK",
            message=f"START WITH {state.mode}",
            new_state=state,
            new_resources=new_resources
        )

    def stop() -> tuple[Result, Capabilities]:
        return emit(
            status="STOP_OK",
            message="STOP",
            new_state=state
        )

    def status() -> tuple[Result, Capabilities]:
        message = (
            f"x={state.x}, y={state.y}, angle={state.angle}, "
            f"mode={state.mode}, water={resources.water}, soap={resources.soap}, "
            f"log={log}"
        )

        return (
            Result("STATUS", message),
            next_api(
                new_state=state,
                new_resources=resources,
                new_log=log,
                new_blocked=blocked
            )
        )

    def can_start() -> bool:
        if state.mode == WATER:
            return resources.water > 0

        if state.mode == SOAP:
            return resources.soap > 0

        return state.mode == BRUSH

    api: dict[str, Operation] = {}

    if not blocked:
        api["move"] = move

    api["turn"] = turn

    if resources.water > 0:
        api["set_water"] = lambda: set_mode(WATER)

    if resources.soap > 0:
        api["set_soap"] = lambda: set_mode(SOAP)

    api["set_brush"] = lambda: set_mode(BRUSH)

    if can_start():
        api["start"] = start

    api["stop"] = stop
    api["status"] = status

    return MappingProxyType(api)