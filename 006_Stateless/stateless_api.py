import pure_robot


def handle_command(transfer, state: pure_robot.RobotState, command: str) -> pure_robot.RobotState:
    parts = command.split()
    cmd = parts[0]

    if cmd == "move":
        return pure_robot.move(transfer, int(parts[1]), state)

    if cmd == "turn":
        return pure_robot.turn(transfer, int(parts[1]), state)

    if cmd == "set":
        return pure_robot.set_state(transfer, parts[1], state)

    if cmd == "start":
        return pure_robot.start(transfer, state)

    if cmd == "stop":
        return pure_robot.stop(transfer, state)

    raise ValueError(f"Неизвестная команда: {command}")


def handle_program(transfer, state: pure_robot.RobotState, commands: list[str]) -> pure_robot.RobotState:
    current_state = state

    for command in commands:
        current_state = handle_command(transfer, current_state, command)

    return current_state