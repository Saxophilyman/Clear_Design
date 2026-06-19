from typing import NamedTuple, Tuple, Callable, Any, NewType
import math

RobotState = NewType('RobotType', object)


class _InternalState(NamedTuple):
    x: float
    y: float
    angle: float
    state: int


WATER = 1
SOAP = 2
BRUSH = 3


class Robot:
    @staticmethod
    def create(transfer_fn: Callable[[Any], None]) -> Tuple[RobotState, Callable]:
        state = _InternalState(0.0, 0.0, 0, WATER)

        def process_commands(commands: Tuple[str, ...]) -> RobotState:
            nonlocal state
            for command in commands:
                cmd = command.split('')
                if cmd[0] == 'move':
                    state = Robot._move(transfer_fn, int(cmd[1]), state)
                elif cmd[0] == 'turn':
                    state = Robot._turn(transfer_fn, int(cmd[1]), state)
                elif cmd[0] == 'set':
                    state = Robot._set_state(transfer_fn, cmd[1], state)
                elif cmd[0] == 'start':
                    state = Robot._start(transfer_fn, state)
                elif cmd[0] == 'stop':
                    state = Robot._stop(transfer_fn, state)
            return RobotState(state)

        return RobotState(state), process_commands

    @staticmethod
    def _move(transfer: Callable, dist: int, state: _InternalState) -> _InternalState:
        angle_rads = state.angle * (math.pi / 180.0)
        new_state = _InternalState(
            state.x,
            state.y,
            state.angle,
            state.state
        )
        transfer(('POS(', new_state.x, ',', new_state.y, ')'))
        return new_state

    @staticmethod
    def _turn(transfer: Callable, angle: int, state: _InternalState) -> _InternalState:
        new_state = _InternalState(
            state.x,
            state.y,
            state.angle + angle,
            state.state
        )
        transfer(('ANGLE', new_state.angle))
        return new_state

    @staticmethod
    def _set_state(transfer: Callable, new_state: str, state: _InternalState) -> _InternalState:
        state_map = {'water': WATER, 'soap': SOAP, 'brush': BRUSH}
        if new_state not in state_map:
            return state

        internal_state = state_map[new_state]
        new_state = _InternalState(
            state.x,
            state.y,
            state.angle,
            internal_state
        )
        transfer(('STATE', internal_state))
        return new_state

    @staticmethod
    def _start(transfer: Callable, state: _InternalState) -> _InternalState:
        transfer(('START WITH', state.state))
        return state

    @staticmethod
    def _stop(transfer: Callable, state: _InternalState) -> _InternalState:
        transfer(('STOP',))
        return state

def transfer_to_cleaner(message):
    print(message)

initial_state, process = Robot.create(transfer_to_cleaner)

commands = (
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
)

final_state = process(commands)