from robot import Robot
from command_executor import CommandExecutor
from program_runner import ProgramRunner


def create_executor() -> CommandExecutor:
    robot = Robot()
    return CommandExecutor(robot)


# Move (двигаться вперед на заданное число метров)
def test_move_from_start():
    executor = create_executor()
    result = executor.execute("move 100")
    assert result == "POS 100,0"


def test_move_another_from_start():
    executor = create_executor()
    result = executor.execute("move 50")
    assert result == "POS 50,0"


def test_move_twice_plus_position():
    executor = create_executor()
    executor.execute("move 100")
    result = executor.execute("move 50")
    assert result == "POS 150,0"


# Turn (поворот на месте на заданный угол в градусах)
def test_turn_changes_angle():
    executor = create_executor()
    result = executor.execute("turn -90")
    assert result == "ANGLE -90"


def test_move_after_turn_changes():
    executor = create_executor()
    executor.execute("turn 90")
    result = executor.execute("move 50")
    assert result == "POS 0,50"


def test_move_after_negative_turn_changes():
    executor = create_executor()
    executor.execute("turn -90")
    result = executor.execute("move 50")
    assert result == "POS 0,-50"


# Set (выбрать одно из трёх устройств очистки)
def test_set_cleaning_mode_soap():
    executor = create_executor()
    result = executor.execute("set soap")
    assert result == "STATE soap"


def test_set_cleaning_mode_water():
    executor = create_executor()
    result = executor.execute("set water")
    assert result == "STATE water"


def test_set_cleaning_mode_brush():
    executor = create_executor()
    result = executor.execute("set brush")
    assert result == "STATE brush"


def test_start_with_current_mode():
    executor = create_executor()
    result = executor.execute("start")
    assert result == "START WITH water"


def test_start_uses_selected_cleaning_mode():
    executor = create_executor()
    executor.execute("set soap")
    result = executor.execute("start")
    assert result == "START WITH soap"


def test_stop():
    executor = create_executor()
    result = executor.execute("stop")
    assert result == "STOP"


def test_full_program_commands_example():
    executor = create_executor()
    results = [
        executor.execute("move 100"),
        executor.execute("turn -90"),
        executor.execute("set soap"),
        executor.execute("start"),
        executor.execute("move 50"),
        executor.execute("stop"),
    ]

    assert results == [
        "POS 100,0",
        "ANGLE -90",
        "STATE soap",
        "START WITH soap",
        "POS 100,-50",
        "STOP",
    ]


def test_run_executes_program():
    robot = Robot()
    executor = CommandExecutor(robot)
    runner = ProgramRunner(executor)

    commands = [
        "move 100",
        "turn -90",
        "set soap",
        "start",
        "move 50",
        "stop",
    ]

    results = runner.run(commands)

    assert results == [
        "POS 100,0",
        "ANGLE -90",
        "STATE soap",
        "START WITH soap",
        "POS 100,-50",
        "STOP",
    ]