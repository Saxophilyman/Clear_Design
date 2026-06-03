from sol import *

def main():

    event_store = EventStore()
    initial_state = RobotState(0.0, 0.0, 0, CleaningMode.WATER.value)
    state_projector = StateProjector(initial_state)
    command_handler = CommandHandler(event_store, state_projector)
    time_travel = TimeTravel(event_store, state_projector)

    robot_id = "robot_001"


    commands = [
        MoveCommand(100),
        TurnCommand(-90),
        SetStateCommand(CleaningMode.SOAP),
        StartCommand(),
        MoveCommand(50),
        StopCommand()
    ]

    for i, cmd in enumerate(commands):
        print(f"Cmd {i+1}: {cmd.get_command_type()}")
        final_state = command_handler.handle_command(robot_id, cmd)
        print(f"State: {final_state}")
        print()

    print("=== Time Travel Demo ===")
    current_version = time_travel.get_current_version(robot_id)
    print(f"curr: {current_version}")

    state_at_version_3 = time_travel.get_state_at_version(robot_id, 3)
    print(f"State 3-: {state_at_version_3}")

    events = event_store.get_events(robot_id)
    for i, event in enumerate(events):
        print(f"Event {i+1}: {event.get_event_type()}")