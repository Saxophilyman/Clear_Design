import  math
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

    new_x = round(state.x + distance * math.cos(angle_rads))
    new_y = round(state.y + distance * math.sin(angle_rads))

    new_state = RobotState(
        x=new_x,
        y=new_y,
        angle=state.angle,
        cleaning_mode=state.cleaning_mode
    )

    transfer(f"POS {int(new_state.x)},{int(new_state.y)}")
    return new_state

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
    if mode not in(WATER, SOAP, BRUSH):
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
    return state

def stop(transfer, state: RobotState) -> RobotState:
    transfer(f"STOP")
    return state

