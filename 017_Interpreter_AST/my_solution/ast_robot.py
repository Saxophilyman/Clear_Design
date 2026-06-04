from dataclasses import dataclass
from typing import Protocol, Callable

import pure_robot


def transfer_to_cleaner(message: str) -> None:
    print(message)


@dataclass(frozen=True)
class RobotContext:
    state: pure_robot.RobotState
    log: list[str]


@dataclass(frozen=True)
class MoveResponse:
    distance: int
    success: bool
    message: str


@dataclass(frozen=True)
class TurnResponse:
    angle: int
    success: bool
    message: str


@dataclass(frozen=True)
class StateResponse:
    mode: str
    success: bool
    message: str


@dataclass(frozen=True)
class SimpleResponse:
    success: bool
    message: str


class RobotProgram(Protocol):
    def interpret(self, interpreter: "RobotInterpreter", context: RobotContext) -> RobotContext:
        pass


@dataclass(frozen=True)
class Stop:
    def interpret(self, interpreter: "RobotInterpreter", context: RobotContext) -> RobotContext:
        return interpreter.interpret_stop(self, context)


@dataclass(frozen=True)
class Move:
    distance: int
    next: Callable[[MoveResponse], RobotProgram]

    def interpret(self, interpreter: "RobotInterpreter", context: RobotContext) -> RobotContext:
        return interpreter.interpret_move(self, context)


@dataclass(frozen=True)
class Turn:
    angle: int
    next: Callable[[TurnResponse], RobotProgram]

    def interpret(self, interpreter: "RobotInterpreter", context: RobotContext) -> RobotContext:
        return interpreter.interpret_turn(self, context)


@dataclass(frozen=True)
class SetState:
    mode: str
    next: Callable[[StateResponse], RobotProgram]

    def interpret(self, interpreter: "RobotInterpreter", context: RobotContext) -> RobotContext:
        return interpreter.interpret_set_state(self, context)


@dataclass(frozen=True)
class Start:
    next: Callable[[SimpleResponse], RobotProgram]

    def interpret(self, interpreter: "RobotInterpreter", context: RobotContext) -> RobotContext:
        return interpreter.interpret_start(self, context)


class RobotInterpreter:
    def interpret(self, program: RobotProgram, context: RobotContext) -> RobotContext:
        return program.interpret(self, context)

    def interpret_move(self, node: Move, context: RobotContext) -> RobotContext:
        if node.distance <= 0:
            response = MoveResponse(
                distance=node.distance,
                success=False,
                message=f"MOVE_FAILED {node.distance}"
            )

            next_node = node.next(response)

            return next_node.interpret(self, RobotContext(
                state=context.state,
                log=context.log + [response.message]
            ))

        new_state = pure_robot.move(transfer_to_cleaner, node.distance, context.state)

        response = MoveResponse(
            distance=node.distance,
            success=True,
            message=f"MOVE_OK {node.distance}"
        )

        next_node = node.next(response)

        return next_node.interpret(self, RobotContext(
            state=context.state,
            log=context.log + [response.message]
        ))

    def interpret_turn(self, node: Turn, context: RobotContext) -> RobotContext:
        new_state = pure_robot.turn(transfer_to_cleaner, node.angle, context.state)

        response = TurnResponse(angle=node.angle, success=True, message=f"TURN_OK {node.angle}")

        next_node = node.next(response)

        return next_node.interpret(self, RobotContext(
            state=new_state,
            log=context.log + [response.message]
        ))

    def interpret_set_state(self, node: SetState, context: RobotContext) -> RobotContext:
        if node.mode not in (
                pure_robot.WATER,
                pure_robot.SOAP,
                pure_robot.BRUSH
        ):
            response = StateResponse(
                mode=node.mode,
                success=False,
                message=f"STATE_FAILED {node.mode}"
            )

            next_node = node.next(response)

            return next_node.interpret(self, RobotContext(
                state=context.state,
                log=context.log + [response.message]
            ))

        new_state = pure_robot.set_state(transfer_to_cleaner, node.mode, context.state)

        response = StateResponse(
            mode=node.mode,
            success=True,
            message=f"STATE_OK {node.mode}"
        )

        next_node = node.next(response)

        return next_node.interpret(self, RobotContext(
            state=new_state,
            log=context.log + [response.message]
        ))

    def interpret_start(self, node: Start, context: RobotContext) -> RobotContext:
        pure_robot.start(transfer_to_cleaner, context.state)

        response = SimpleResponse(
            success=True,
            message="START_OK"
        )

        next_node = node.next(response)

        return next_node.interpret(self, RobotContext(
            state=context.state,
            log=context.log + [response.message]
        ))

    def interpret_stop(self, node: Stop, context: RobotContext) -> RobotContext:
        pure_robot.stop(transfer_to_cleaner, context.state)

        return RobotContext(
            state=context.state,
            log=context.log + ["STOP"]
        )


def create_initial_context() -> RobotContext:
    return RobotContext(
        state=pure_robot.RobotState(
            x=0.0,
            y=0.0,
            angle=0,
            cleaning_mode=pure_robot.WATER
        ),
        log=[]
    )
