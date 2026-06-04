import pure_robot

from ast_robot import *


program = Move(
    100,
    lambda move_response:
    Turn(
        -90,
        lambda turn_response:
        SetState(
            pure_robot.SOAP,
            lambda state_response:
            Start(
                lambda start_response:
                Move(
                    50,
                    lambda second_move_response:
                    Stop()
                )
            )
        )
    )
)


interpreter = RobotInterpreter()

result = interpreter.interpret(
    program,
    create_initial_context()
)

print("Final state:")
print(result.state)

print("Log:")
print(result.log)