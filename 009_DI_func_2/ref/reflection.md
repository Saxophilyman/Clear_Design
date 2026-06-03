Иногда приходится себе напоминать, что курс прежде всего про архитектуру, а не про специфику реализации или технические моменты.
Повторю для себя, что у нас ведётся работа с несколькими составными, из которых сейчас можно выделить:
1) ядро, как pure_robot. В котором имеются свои базовые функции
2) api, cleaner_apy для передачи всей сформированной настройки клиенту
3) client, который пользуется готовым Api и в идеале не должен ничего знать про внутреннюю работу ядра

Существенное отличие от эталона заключается в том, что по итогу у клиента получается готовый api, без лишних раскрытий,
что позволяет продолжать его использовать даже при смене реализации. 
В моей же попытке, клиент каждый раз сам должен настроить всю необходимую передачу. 
С __call__ прежде пришлось разобраться самостоятельно, но в примере яснее показан способ его применения и сила его использования. 
Общая же логика как DI вроде бы отражена: функция как зависимость, передача извне, работа с состоянием, основной модуль неизменен. 
Но даже в моём случае была видна проблема передачи нескольких параметров/функций.   
Попробую сделать вариант с одной функцией.  
Ядро также должно остаться неизменным, как и клиентское api

```python
from dataclasses import dataclass
from typing import Callable

import pure_robot


# вводим прослойку для обработки команд и их типирования
@dataclass(frozen=True)
class RobotCommand:
    name: str
    value: str | None = None


TransferFunction = Callable[[str], None]

RobotFunction = Callable[[RobotCommand, TransferFunction, pure_robot.RobotState], pure_robot.RobotState]


class RobotApi:
    robot_function: RobotFunction
    transfer_function: TransferFunction
    cleaner_state: pure_robot.RobotState

    def setup(self, robot_function: RobotFunction, transfer_function: TransferFunction) -> None:
        self.robot_function = robot_function
        self.transfer_function = transfer_function

    def make(self, command: str) -> pure_robot.RobotState:
        if not hasattr(self, "cleaner_state"):
            self.cleaner_state = pure_robot.RobotState(
                x=0.0,
                y=0.0,
                angle=0,
                cleaning_mode=pure_robot.WATER
            )

        robot_command = self.parse_command(command)

        self.cleaner_state = self.robot_function(robot_command, self.transfer_function, self.cleaner_state)

        return self.cleaner_state

    def parse_command(self, command) -> RobotCommand:
        parts = command.split()

        if len(parts) == 0:
            raise ValueError("Нет команды")

        name = parts[0]
        value = parts[1] if len(parts) > 1 else None

        return RobotCommand(name=name, value=value)

    def __call__(self, command: str) -> pure_robot.RobotState:
        return self.make(command)


def transfer_to_cleaner(message: str) -> None:
    print(message)


def robot_operation(command: RobotCommand, transfer: TransferFunction,
                    state: pure_robot.RobotState) -> pure_robot.RobotState:
    if command.name == 'move':
        return pure_robot.move(transfer, int(command.value), state)

    if command.name == 'turn':
        return pure_robot.turn(transfer, int(command.value), state)

    if command.name == 'set':
        return pure_robot.set_state(transfer, command.value, state)

    if command.name == 'start':
        return pure_robot.start(transfer, state)

    if command.name == 'stop':
        return pure_robot.stop(transfer, state)

api = RobotApi()

api.setup(robot_operation, transfer_to_cleaner)
```
насколько в питоне некоторые вещи лаконичны