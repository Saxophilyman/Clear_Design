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

