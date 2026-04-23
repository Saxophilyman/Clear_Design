import math
from dataclasses import dataclass


WATER = "water"
SOAP = "soap"
BRUSH = "brush"


@dataclass(frozen=True)
class RobotState:
    x: float
    y: float
    angle: int
    cleaning_mode: str


def move(transfer, distance: int, state: RobotState) -> RobotState:
    angle_rads = math.radians(state.angle)

    new_x = state.x + distance * math.cos(angle_rads)
    new_y = state.y + distance * math.sin(angle_rads)

    new_x = round(new_x)
    new_y = round(new_y)

    transfer(f"POS {int(new_x)},{int(new_y)}")

    return RobotState(
        x=new_x,
        y=new_y,
        angle=state.angle,
        cleaning_mode=state.cleaning_mode
    )


def turn(transfer, angle: int, state: RobotState) -> RobotState:
    new_state = RobotState(
        x=state.x,
        y=state.y,
        angle=state.angle + angle,
        cleaning_mode=state.cleaning_mode
    )

    transfer(f"ANGLE {new_state.angle}")
    return new_state


def set_state(transfer, mode: str, state: RobotState) -> RobotState:
    if mode not in (WATER, SOAP, BRUSH):
        raise ValueError(f"Неизвестный режим очистки: {mode}")

    new_state = RobotState(
        x=state.x,
        y=state.y,
        angle=state.angle,
        cleaning_mode=mode
    )

    transfer(f"STATE {new_state.cleaning_mode}")
    return new_state


def start(transfer, state: RobotState) -> RobotState:
    transfer(f"START WITH {state.cleaning_mode}")
    return RobotState(
        x=state.x,
        y=state.y,
        angle=state.angle,
        cleaning_mode=state.cleaning_mode
    )


def stop(transfer, state: RobotState) -> RobotState:
    transfer("STOP")
    return RobotState(
        x=state.x,
        y=state.y,
        angle=state.angle,
        cleaning_mode=state.cleaning_mode
    )


def make(transfer, commands: list[str], state: RobotState) -> RobotState:
    current_state = state

    for command in commands:
        parts = command.split()
        cmd = parts[0]

        if cmd == "move":
            current_state = move(transfer, int(parts[1]), current_state)
        elif cmd == "turn":
            current_state = turn(transfer, int(parts[1]), current_state)
        elif cmd == "set":
            current_state = set_state(transfer, parts[1], current_state)
        elif cmd == "start":
            current_state = start(transfer, current_state)
        elif cmd == "stop":
            current_state = stop(transfer, current_state)
        else:
            raise ValueError(f"Неизвестная команда: {command}")

    return current_state