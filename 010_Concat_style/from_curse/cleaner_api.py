import pure_robot


class CatApi:

    def __init__(self):
        self.stack = [pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)]

    def exec(self, code):
        heap = code.split(' ')
        for itm in heap:
            self.compose(itm)
        if len(self.stack) > 0:
            return self.stack[0]
        return None

    def compose(self, fn):
        if fn == 'move':
            v = self.pop()
            state = self.pop()
            new_state = pure_robot.move(transfer, int(v), state)
            self.push(new_state)
        elif fn == 'turn':
            v = self.pop()
            state = self.pop()
            new_state = pure_robot.turn(transfer, int(v), state)
            self.push(new_state)
        elif fn == 'set':
            v = self.pop()
            state = self.pop()
            new_state = pure_robot.set_state(transfer, v, state)
            self.push(new_state)
        elif fn == 'start':
            state = self.pop()
            new_state = pure_robot.start(transfer, state)
            self.push(new_state)
        elif fn == 'stop':
            state = self.pop()
            new_state = pure_robot.stop(transfer, state)
            self.push(new_state)
        else:
            self.push(fn)

    def pop(self):
        v = self.stack[-1]
        self.stack.pop()
        return v

    def push(self, v):
        self.stack.append(v)


def transfer(message):
    print(message)
