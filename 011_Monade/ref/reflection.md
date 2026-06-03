В целом на определённом уровне удалось уловить суть работы в конкатенативном стиле, использование стёка 
позволяет организовать последовательную и в некотором роде автоматическую работу, предоставляя пользователю 
доступ к выполнению в одну строку. В стёке хранятся сами аргументы. Я постарался сохранить принципы и преимущества DI
с возможной заменой реализации из предыдущего примера.   
Но по сравнению с эталоном разбор строки на команды через стек выглядит словно взяли откуда-то кусочек механики 
и просто его вставили, основная сущность словно лежит снаружи. Приём полноценной работы через стек совместно
с состоянием выглядит более целостным и лаконичным. Сам api получается как бы построенным через стёк.

Если бы я знал питон или другой функциональный ЯП, то, возможно, мне было бы проще разобраться с концепцией монады.
Но я впервые слышу о ней (не считая материалов лаборатории) в практическом смысле и пришлось изрядно погуглить,
чтобы познакомиться и немножко понять её смысл и применение.  
Во-первых, это тип данных, во-вторых, это контейнер хранящий произвольный тип данных, в-третьих, должна быть функция 
связывания.
В очередной раз встречаясь с концепцией более высокого уровня, не могу не отметить, что помимо сложности - это интересно
и в то же время вновь меняет и разрывает уже установившиеся представления. С другой стороны через курс последовательно
привыкаешь, что состояние храниться и переиспользуется в самой структуре данных, 
что даже монада воспринимается логически вытекающей из всего предыдущего.
Bind будет работать с состоянием, остальное будет плюс-минус неизменно, остаётся разобраться с синтаксисом, типизацией 
и шаблоном конструкций.   

```python
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

import pure_robot

# настраиваем типизацию
T = TypeVar("T")
U = TypeVar("U")

TransferFunction = Callable[[str], None]
# состояние, результат+новое состояние
StateFunction = Callable[[pure_robot.RobotState], tuple[T, pure_robot.RobotState]]


@dataclass(frozen=True)
class StateMonad(Generic[T]):
    run: StateFunction[T]

    # строит вычисление
    def bind(self, next_function: Callable[[T], "StateMonad[U]"]) -> "StateMonad[U]":
        def new_run(state: pure_robot.RobotState) -> tuple[U, pure_robot.RobotState]:
            value, new_state = self.run(state)
            next_monad = next_function(value)
            return next_monad.run(new_state)

        return StateMonad(new_run)

    def __rshift__(self, next_function: Callable[[T], "StateMonad[U]"]) -> "StateMonad[U]":
        return self.bind(next_function)


# начальная команда
def unit(value: T) -> StateMonad[T]:
    def run(state: pure_robot.RobotState) -> tuple[T, pure_robot.RobotState]:
        return value, state

    return StateMonad(run)


def move(transfer: TransferFunction, distance: int) -> StateMonad[pure_robot.RobotState]:
    def run(state: pure_robot.RobotState) -> tuple[pure_robot.RobotState, pure_robot.RobotState]:
        new_state = pure_robot.move(transfer, distance, state)
        return new_state, new_state

    return StateMonad(run)


def turn(transfer: TransferFunction, angle: int) -> StateMonad[pure_robot.RobotState]:
    def run(state: pure_robot.RobotState) -> tuple[pure_robot.RobotState, pure_robot.RobotState]:
        new_state = pure_robot.turn(transfer, angle, state)
        return new_state, new_state

    return StateMonad(run)


def set_state(transfer: TransferFunction, mode: str) -> StateMonad[pure_robot.RobotState]:
    def run(state: pure_robot.RobotState) -> tuple[pure_robot.RobotState, pure_robot.RobotState]:
        new_state = pure_robot.set_state(transfer, mode, state)
        return new_state, new_state

    return StateMonad(run)


def start(transfer: TransferFunction) -> StateMonad[pure_robot.RobotState]:
    def run(state: pure_robot.RobotState) -> tuple[pure_robot.RobotState, pure_robot.RobotState]:
        new_state = pure_robot.start(transfer, state)
        return new_state, new_state

    return StateMonad(run)


def stop(transfer: TransferFunction) -> StateMonad[pure_robot.RobotState]:
    def run(state: pure_robot.RobotState) -> tuple[pure_robot.RobotState, pure_robot.RobotState]:
        new_state = pure_robot.stop(transfer, state)
        return new_state, new_state

    return StateMonad(run)

```

Предполагаю, что клиент также должен быть минимально неизменным, с простым набором вызывающих команд, 
но как это сейчас завернуть всё в серверный api пока не совсем ясно, подожду примера эталона)

```python
import pure_robot
from monad_robot_api import unit, move, turn, set_state, start, stop


def transfer(message: str) -> None:
    print(message)


initial_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

program = (unit(initial_state)
           >> (lambda _: move(transfer, 100))
           >> (lambda _: turn(transfer, -90))
           >> (lambda _: set_state(transfer, pure_robot.SOAP))
           >> (lambda _: start(transfer))
           >> (lambda _: move(transfer, 50))
           >> (lambda _: stop(transfer))
           )

result, final_state = program.run(initial_state)

print(result)
print(final_state)
```