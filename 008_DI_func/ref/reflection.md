Когда-то я читал и разбирал DI. Всё было логично, ясно и элегантно в своём решении, 
но сейчас я понимаю, что в памяти сохранилась скорее сама концепция и идея, и способы использования в Spring, 
нежели её наглядное воплощение. Поэтому так ценно было ещё раз пройтись и повторить по основам. 
К тому же python до сих пор остаётся для меня чужеродным, а потому немного магическим.  
Само же задание выглядело гораздо проще предыдущего. Вся суть сводится к использованию интерфейса и возможной замены реализации.  
Сложнее обстоит с возможностью DI через функции, как минимум надо было разобраться в возможностях языка, а также 
перейти к пониманию сменяемости функций и их получения как обычного параметра.  
Вообще, хоть это и не относится к курсу напрямую, но разницу между ООП и функциональным языком постоянно приходится уяснять для себя

```python
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
```

```python
from typing import Callable

from pure_robot import RobotState

TransferFunction = Callable[[str], None]

MoveFunction = Callable[[TransferFunction, int, RobotState], RobotState]
TurnFunction = Callable[[TransferFunction, int, RobotState], RobotState]
SetStateFunction = Callable[[TransferFunction, str, RobotState], RobotState]
StateOnlyFunction = Callable[[TransferFunction, RobotState], RobotState]

def apply_command(
        transfer: TransferFunction,
        state: RobotState,
        command: str,
        move_func: MoveFunction,
        turn_func: TurnFunction,
        set_state_func: SetStateFunction,
        start_func: StateOnlyFunction,
        stop_func: StateOnlyFunction
) -> RobotState:
    parts = command.split()
    cmd = parts[0]

    if cmd == "move":
        return move_func(transfer, int(parts[1]), state)

    if cmd == "turn":
        return turn_func(transfer, int(parts[1]), state)

    if cmd == "set":
        return set_state_func(transfer, parts[1], state)

    if cmd == "start":
        return start_func(transfer, state)

    if cmd == "stop":
        return stop_func(transfer, state)

    raise ValueError(f"Неизвестная команда: {command}")


def run_program(
        transfer: TransferFunction,
        state: RobotState,
        commands: list[str],
        move_func: MoveFunction,
        turn_func: TurnFunction,
        set_state_func: SetStateFunction,
        start_func: StateOnlyFunction,
        stop_func: StateOnlyFunction
) -> RobotState:
    current_state = state

    for command in commands:
        current_state = apply_command(
            transfer=transfer,
            state=current_state,
            command=command,
            move_func=move_func,
            turn_func=turn_func,
            set_state_func=set_state_func,
            start_func=start_func,
            stop_func=stop_func
        )

    return current_state

```

```python
import pure_robot
from functional_di_api import run_program

def transfer_to_cleaner(message: str) -> None:
    print(message)

def main():
    commands = [
        "move 100",
        "turn -90",
        "set soap",
        "start",
        "move 50",
        "stop"
    ]

    initial_state = pure_robot.RobotState(
        x=0.0,
        y=0.0,
        angle=0,
        cleaning_mode=pure_robot.WATER
    )

    final_state = run_program(
        transfer=transfer_to_cleaner,
        state=initial_state,
        commands=commands,
        move_func=pure_robot.move,
        turn_func=pure_robot.turn,
        set_state_func=pure_robot.set_state,
        start_func=pure_robot.start,
        stop_func=pure_robot.stop
    )

    print(
        final_state.x,
        final_state.y,
        final_state.angle,
        final_state.cleaning_mode
    )


if __name__ == "__main__":
    main()
```