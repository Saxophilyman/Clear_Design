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