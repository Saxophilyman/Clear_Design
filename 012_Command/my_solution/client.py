import pure_robot

from command_robot_api import *

commands = [
    MoveCommand(100),
    TurnCommand(-90),
    SetStateCommand(pure_robot.SOAP),
    StartCommand(),
    MoveCommand(50),
    StopCommand()
]

final_state = api.execute(commands)

print(final_state)