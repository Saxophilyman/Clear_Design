import pure_robot
from cleaner_api import RobotCommand, command_to_queue

# клиент
c = RobotCommand(input_state=pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER),
                 command='move 100')
c = command_to_queue(c)
c.command = 'turn -90'
c = command_to_queue(c)
c.command = 'set soap'
c = command_to_queue(c)
c.command = 'start'
c = command_to_queue(c)
c.command = 'move 50'
c = command_to_queue(c)
c.command = 'stop'
c = command_to_queue(c)

for i in range(1000):
    c.command = 'turn -90'
    c = command_to_queue(c)

print(c.state.x)
