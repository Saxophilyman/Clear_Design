from stream_robot import *


event_store = EventStore()

event_store.subscribe(MoveProcessor())
event_store.subscribe(TurnProcessor())
event_store.subscribe(CleaningModeProcessor())
event_store.subscribe(StartProcessor())
event_store.subscribe(StopProcessor())

command_handler = CommandHandler(event_store)

robot_id = "robot-1"

command_handler.handle(MoveCommand(robot_id, 100))
command_handler.handle(TurnCommand(robot_id, -90))
command_handler.handle(SetStateCommand(robot_id, "soap"))
command_handler.handle(StartCommand(robot_id))
command_handler.handle(MoveCommand(robot_id, 50))
command_handler.handle(StopCommand(robot_id))

print("Events:")
for event in event_store.get_events(robot_id):
    print(event)

result_events = event_store.get_result_events(robot_id)
final_state = rebuild_state(result_events)

print("Final state:")
print(final_state)