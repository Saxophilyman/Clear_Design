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
    # -- либо текущую позицию: POS x,y (команда move),


    # -- либо текущий угол поворота в градусах: ANGLE a (команда turn),
    # -- либо текущее состояние устройства очистки (одно из трёх): STATE water/soap/brush (команда set),
    # -- либо начало работы с текущим состоянием устройства очистки: START WITH water/soap/brush (команда start),
    # -- либо прекращение работы: STOP (команда stop).

    # 'move 100',
    # 'turn -90',
    # 'set soap',
    # 'start',
    # 'move 50',
    # 'stop'