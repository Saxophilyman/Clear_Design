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