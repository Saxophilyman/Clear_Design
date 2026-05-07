import pure_robot


class RobotApi:
    def setup(self, fn, transfer):
        self.f_transfer = transfer
        self.fn = fn

    def make(self, command: str) -> pure_robot.RobotState:
        if not hasattr(self, "cleaner_state"):
            self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

        cmd = command.split('')
        fun = self.fn(cmd)
        if cmd[0] == 'move':
            self.cleaner_state = fun(self.f_transfer, int(cmd[1]), self.cleaner_state)
        elif cmd[0] == 'turn':
            self.cleaner_state = fun(self.f_transfer, int(cmd[1]), self.cleaner_state)
        elif cmd[0] == 'set':
            self.cleaner_state = fun(self.f_transfer, cmd[1], self.cleaner_state)
        elif cmd[0] == 'start':
            self.cleaner_state = fun(self.f_transfer, self.cleaner_state)
        elif cmd[0] == 'stop':
            self.cleaner_state = fun(self.f_transfer, self.cleaner_state)
        return self.cleaner_state

    def __call__(self, command):
        return self.make(command)


def transfer_to_cleaner(message: str) -> None:
    print(message)


def double_move(transfer, dist, state):
    return pure_robot.move(transfer, dist * 2, state)


def robotFn(cmd):
    if cmd[0] == 'move':
        return pure_robot.move
    elif cmd[0] == 'turn':
        return pure_robot.turn
    elif cmd[0] == 'set':
        return pure_robot.set_state
    elif cmd[0] == 'start':
        return pure_robot.start
    elif cmd[0] == 'stop':
        return pure_robot.stop
    return None

def robotFn2(cmd):
    if cmd[0] == 'move':
        return double_move
    return robotFn(cmd)


api = RobotApi()
# api.setup(robotFn, transfer_to_cleaner)
api.setup(robotFn2, transfer_to_cleaner)
