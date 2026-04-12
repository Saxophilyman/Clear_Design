from cleaner_robot import RobotController
# Move (двигаться вперед на заданное число метров)
def test_move_from_start():
    robot = RobotController()
    result = robot.execute('move 100')
    assert result == 'POS 100,0'

def test_move_another_from_start():
    robot = RobotController()
    result = robot.execute('move 50')
    assert result == 'POS 50,0'

def test_move_twice_plus_position():
    robot = RobotController()
    robot.execute('move 100')
    result = robot.execute('move 50')
    assert result == 'POS 150,0'

# Turn (поворот на месте на заданный угол в градусах)
def test_turn_changes_angle():
    robot = RobotController()
    result = robot.execute('turn -90')
    assert result == 'ANGLE -90'

def test_move_after_turn_changes():
    robot = RobotController()
    robot.execute('turn 90')
    result = robot.execute('move 50')
    assert result == 'POS 0,50'

def test_move_after_negative_turn_changes():
    robot = RobotController()
    robot.execute('turn -90')
    result = robot.execute('move 50')
    assert result == 'POS 0,-50'

# Set (выбрать одно из трёх устройств очистки)
def test_set_cleaning_mode_soap():
    robot = RobotController()
    result = robot.execute('set soap')
    assert result == 'STATE soap'

def test_set_cleaning_mode_water():
    robot = RobotController()
    result = robot.execute('set water')
    assert result == 'STATE water'

def test_set_cleaning_mode_brush():
    robot = RobotController()
    result = robot.execute('set brush')
    assert result == 'STATE brush'

def test_start_with_current_mode():
    robot = RobotController()
    result = robot.execute('start')
    assert result == 'START WITH water'

def test_start_uses_selected_cleaning_mode():
    robot = RobotController()
    robot.execute('set soap')
    result = robot.execute('start')
    assert result == 'START WITH soap'

def test_stop():
    robot = RobotController()
    result = robot.execute('stop')
    assert result == 'STOP'

def test_full_program_commands_example():
    robot = RobotController()

    results = [
        robot.execute('move 100'),
        robot.execute('turn -90'),
        robot.execute('set soap'),
        robot.execute('start'),
        robot.execute('move 50'),
        robot.execute('stop')
    ]

    assert results == [
        'POS 100,0',
        'ANGLE -90',
        'STATE soap',
        'START WITH soap',
        'POS 100,-50',
        'STOP'
    ]
# Входная программа управления роботом представляет собой
# список команд (строки),
# которые выполняются последовательно одна за одной.
def test_run_executes_program():
    robot = RobotController()

    commands = [
        'move 100',
        'turn -90',
        'set soap',
        'start',
        'move 50',
        'stop'
    ]

    results = robot.run(commands)

    assert results == [
        'POS 100,0',
        'ANGLE -90',
        'STATE soap',
        'START WITH soap',
        'POS 100,-50',
        'STOP'
    ]