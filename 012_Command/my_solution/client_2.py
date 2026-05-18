from command_robot_api_2 import *

executor = CommandExecutor()

executor.add_command(MoveCommand(100))
executor.add_command(TurnCommand(-90))
executor.add_command(SetStateCommand(SOAP))
executor.add_command(StartCommand())
executor.add_command(MoveCommand(50))
executor.add_command(StopCommand())

initial_state = create_initial_state()

final_state, logs = executor.execute_all(initial_state)

print("Final state:", final_state)
print("Command log:", logs)
