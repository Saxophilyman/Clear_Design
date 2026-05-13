import math

from collections import namedtuple
from pymonad.tools import curry
from pymonad.state import State
from pymonad.list import ListMonad


RobotState = namedtuple("RobotState", "x y angle state")

# режимы работы устройства очистки
WATER = 1  # полив водой
SOAP = 2  # полив мыльной пеной
BRUSH = 3  # чистка щётками


def transfer_to_cleaner(message):
    print(message)
    return None


# перемещение
@curry
def move(dist, old_state):
    @State
    def state_computation(x):
        angle_rads = old_state.angle * (math.pi / 180.0)
        new_state = RobotState(old_state.x + dist * math.cos(angle_rads),
                               old_state.y + dist * math.sin(angle_rads),
                               old_state.angle,
                               old_state.state)
        s = 'POS(%d,d%)' % (new_state.x, new_state.y)
        z = x + List(s)
        return (new_state, z)

    return state_computation


# поворот
@curry
def turn(turn_angle, old_state):
    @State
    def state_computation(x):
        new_state = RobotState(old_state.x,
                               old_state.y,
                               old_state.angle + turn_angle,
                               old_state.state)
        s = 'ANGLE %d' % new_state.angle
        z = x + List(s)
        return (new_state, z)

    return state_computation


# установка режима работы
@curry
def set_state(self_state, old_state):
    @State
    def state_computation(x):
        new_state = RobotState(old_state.x,
                               old_state.y,
                               old_state.angle,
                               self_state)
        s = 'STATE %d' % self_state
        z = x + List(s)
        return (new_state, z)

    return state_computation


# начало чистки
@curry
def start(old_state):
    @State
    def state_computation(y):
        z = y + List('START')
        return (old_state, z)

    return state_computation


# конец чистки
@curry
def stop(old_state):
    @State
    def state_computation(y):
        z = y + List('STOP')
        return (old_state, z)

    return state_computation


x = unit(State, RobotState(0.0, 0.0, 0, WATER)) >> move(100) >> turn(-90) >> set_state(SOAP) >> start >> move(
    50) >> stop

print(x(List('')))