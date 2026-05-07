При всём старании сократить количество параметров, не рассматривал идею возможности функции сразу выбирать новую функцию.
Старался реализовать через промежуточный слой - обработчика команд, но при этом немного отошёл от фишки DI, 
в итоге в сравнении с эталонным примером мой robot_operation в каком-то роде оказался слишком "многозадачным",
одновременно выбирая действие, вызывая функцию и управляя выполнением.
Насколько помню из других материалов функция, вызывающая и возвращающая функцию - это функция высшего порядка.
А выбор и вычисление по факту запроса - является поздним связыванием. При этом то, что можно заменить функцию по DI
похоже на функциональный полиморфизм.  
Непосредственно к курсу это не относится, но интересно наглядно посмотреть на эти приёмы(шаблоны) в практическом использовании.
Также для меня сложнее уже определить типизацию, т.к. программа должна как бы работать с разным количеством и типом параметров 

```python
from typing import Callable

import pure_robot

TransferFunction = Callable[[str], None]
RobotFunction = Callable[..., pure_robot.RobotState]
RobotFunctionSelector = Callable[[str], RobotFunction | None]


class RobotConcatApi:
    fn: RobotFunctionSelector
    f_transfer: TransferFunction
    cleaner_state: pure_robot.RobotState
    stack: list[str]

    def setup(self, fn: RobotFunctionSelector, transfer: TransferFunction) -> None:
        self.fn = fn
        self.f_transfer = transfer

    def make(self, pipeline: str) -> pure_robot.RobotState:
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

        if not hasattr(self, 'stack'):
            self.stack = []

        commands: list[str] = pipeline.split()

        for command in commands:
            self.execute_token(command)

        return self.cleaner_state

    def execute_token(self, command: str) -> None:
        fun: RobotFunction | None = self.fn(command)

        if fun is None:
            self.stack.append(command)
            return

        if command == "move":
            dist: int = int(self.stack.pop())
            self.cleaner_state = fun(self.f_transfer, dist, self.cleaner_state)
            return

        if command == "turn":
            angle: int = int(self.stack.pop())
            self.cleaner_state = fun(self.f_transfer, angle, self.cleaner_state)
            return

        if command == "set":
            mode: str = self.stack.pop()
            self.cleaner_state = fun(self.f_transfer, mode, self.cleaner_state)
            return

        if command == "start":
            self.cleaner_state = fun(self.f_transfer, self.cleaner_state)
            return

        if command == "stop":
            self.cleaner_state = fun(self.f_transfer, self.cleaner_state)
            return

        raise ValueError(f"Неизвестная команда: {command}")

    def __call__(self, pipeline: str) -> pure_robot.RobotState:
        return self.make(pipeline)


def transfer_to_cleaner(message: str) -> None:
    print(message)


def double_move(transfer: TransferFunction, dist: int, state: pure_robot.RobotState) -> pure_robot.RobotState:
    return pure_robot.move(transfer, dist * 2, state)


def robotFn(token: str) -> RobotFunction | None:
    if token == "move":
        return pure_robot.move
    elif token == "turn":
        return pure_robot.turn
    elif token == "set":
        return pure_robot.set_state
    elif token == "start":
        return pure_robot.start
    elif token == "stop":
        return pure_robot.stop

    return None


def robotFn2(token: str) -> RobotFunction | None:
    if token == "move":
        return double_move

    return robotFn(token)


api = RobotConcatApi()
api.setup(robotFn2, transfer_to_cleaner)

```