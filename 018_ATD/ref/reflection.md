Очень классное и элегантное решение. Сами узлы просто возвращают узлы с состоянием,
Интерпретатор достаточно прост и в связке с узлами оказывается эффективен и универсален.
Интересно и применение принципа типизации.  
Не раз ещё буду обдумывать пример решения и задания. Также и вариант с DSL.
В целом же с удовольствием бы перепрошёл и вник бы во все нюансы курса ещё раз. 
Очень много содержания. И очень сложно.

Попытаюсь отправить пример АТД

```python
import math
from dataclasses import dataclass


WATER = "water"
SOAP = "soap"
BRUSH = "brush"


@dataclass(frozen=True)
class _Robot:
    _x: float
    _y: float
    _angle: int
    _cleaning_mode: str


def create_robot() -> _Robot:
    return _Robot(
        _x=0.0,
        _y=0.0,
        _angle=0,
        _cleaning_mode=WATER
    )


def move(robot: _Robot, distance: int) -> _Robot:
    angle_rads = math.radians(robot._angle)

    new_x = round(robot._x + distance * math.cos(angle_rads))
    new_y = round(robot._y + distance * math.sin(angle_rads))

    return _Robot(
        _x=new_x,
        _y=new_y,
        _angle=robot._angle,
        _cleaning_mode=robot._cleaning_mode
    )


def turn(robot: _Robot, angle: int) -> _Robot:
    return _Robot(
        _x=robot._x,
        _y=robot._y,
        _angle=robot._angle + angle,
        _cleaning_mode=robot._cleaning_mode
    )


def set_state(robot: _Robot, mode: str) -> _Robot:
    if mode not in (WATER, SOAP, BRUSH):
        raise ValueError(f"Неизвестный режим очистки: {mode}")

    return _Robot(
        _x=robot._x,
        _y=robot._y,
        _angle=robot._angle,
        _cleaning_mode=mode
    )


def start(robot: _Robot) -> _Robot:
    print(f"START WITH {robot._cleaning_mode}")
    return robot


def stop(robot: _Robot) -> _Robot:
    print("STOP")
    return robot


def get_position(robot: _Robot) -> tuple[float, float]:
    return robot._x, robot._y


def get_angle(robot: _Robot) -> int:
    return robot._angle


def get_cleaning_mode(robot: _Robot) -> str:
    return robot._cleaning_mode
```

```python
from robot_adt import *

robot = create_robot()

robot = move(robot, 100)
robot = turn(robot, -90)
robot = set_state(robot, SOAP)
robot = start(robot)
robot = move(robot, 50)
robot = stop(robot)

print(get_position(robot))
print(get_angle(robot))
print(get_cleaning_mode(robot))
```