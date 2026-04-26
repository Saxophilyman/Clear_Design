import pure_robot
from stateless_api import handle_program


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

    final_state = handle_program(
        transfer=transfer_to_cleaner,
        state=initial_state,
        commands=commands
    )

    print(
        final_state.x,
        final_state.y,
        final_state.angle,
        final_state.cleaning_mode
    )


if __name__ == "__main__":
    main()