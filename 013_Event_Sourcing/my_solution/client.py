from event_sourcing_robot import *

event_store = EventStore()
command_handler = CommandHandler(event_store)

robot_id = "robot-1"

command_handler.handle(MoveCommand(robot_id, 100))
command_handler.handle(TurnCommand(robot_id, -90))
command_handler.handle(SetStateCommand(robot_id, "soap"))
command_handler.handle(StartCommand(robot_id))
command_handler.handle(MoveCommand(robot_id, 50))
command_handler.handle(StopCommand(robot_id))

events = event_store.get_events(robot_id)
final_state = rebuild_state(events)

print("Events:")
for event in events:
    print(event)

print("Final state:")
print(final_state)