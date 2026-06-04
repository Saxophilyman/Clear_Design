from sol import *

def main():
    event_store = EventStore()
    initial_state = RobotState(0.0, 0.0, 0, CleaningMode.WATER.value)
    state_projector = StateProjector(initial_state)

    command_handler = CommandHandler(event_store)

    movement_processor = MovementProcessor(event_store, state_projector)
    state_processor = StateProcessor(event_store, state_projector)
    logging_processor = LoggingProcessor(event_store, state_projector)

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
        print(f"\n--- Cmd {i+1}: {cmd.get_command_type()} ---")
        command_handler.handle_command(robot_id, cmd)

        time.sleep(0.1)

        current_state = state_projector.project_state(robot_id,
                                                      event_store.get_events_for_robot(robot_id))
        print(f"State: {current_state}")

    print(f"\n=== All events ({len(event_store.get_all_events())}) ===")
    for i, event in enumerate(event_store.get_all_events()):
        print(f"{i+1}. {event.get_event_type()}")