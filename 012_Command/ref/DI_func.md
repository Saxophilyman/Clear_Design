Не смотря, на лёгкость, с которой я писал в рефлексии, для меня решение в данном стиле казалось почти невозможным.
Типизация как усложняла, так и помогала. Думаю без неё я совсем бы запутался
Увлёкшись разбором понимание монады немного забыл, что даже занятие называется Архитектура на монадных состояниях
Насколько понимаю, получается практическая иллюстрация передачи контекста через монаду - монада работает с логом команд,
а цепочка работает с состоянием робота как значениями.   
RobotState выступает не совсем как монада, но передаётся как основное значение по "цепочке",
а лог наоборот выступает в качестве "состояния" монады. В моём же случае и первое и второе были одним и тем же.

Не знал я также и о библиотеках, что очень упрощает работу, но я тогда совсем бы не понял bind. 

Имеется куча вопросов и нюансов. Вводится большое количество абстракций с которыми я не был знаком.
Действительно одним из главных минусов, что данный подход требует "определённого" понимания монад))

----

Пробуя подход паттерна Command.  
Информация про концептуальные изменения пугает, интригует и дезориентирует, но пора уже ко всему этому привыкнуть.
Постараюсь придерживаться идеи, что, как и в монадах, команды будут выполняться не сразу, 
а строить список из описываемых действий к выполнению. Так называемое отложенное выполнение. 
И должно быть что-то такое(fold), что позволит состояние передавать между командами, но не хранить его между вызовами

```python
from dataclasses import dataclass
from typing import Callable, Protocol

import pure_robot

TransferFunction = Callable[[str], None]


# Интерфейс на всех
class RobotCommand(Protocol):
    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        pass


@dataclass(frozen=True)
class MoveCommand:
    distance: int

    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.move(transfer, self.distance, state)


@dataclass(frozen=True)
class TurnCommand:
    angle: int

    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.turn(transfer, self.angle, state)


@dataclass(frozen=True)
class SetStateCommand:
    mode: str

    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.set_state(transfer, self.mode, state)


@dataclass(frozen=True)
class StartCommand:
    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.start(transfer, state)


@dataclass(frozen=True)
class StopCommand:
    def execute(self, transfer: TransferFunction, state: pure_robot.RobotState) -> pure_robot.RobotState:
        return pure_robot.stop(transfer, state)


class RobotCommandApi:
    transfer: TransferFunction

    def __init__(self) -> None:
        self.transfer = transfer_to_cleaner

    def execute(self, commands: list[RobotCommand]) -> pure_robot.RobotState:
        state = pure_robot.RobotState(
            x=0.0,
            y=0.0,
            angle=0,
            cleaning_mode=pure_robot.WATER)

        # условный fold
        for command in commands:
            state = command.execute(self.transfer, state)

        return state

def transfer_to_cleaner(message: str) -> None:
    print(message)

api = RobotCommandApi()
```

```python
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
```
