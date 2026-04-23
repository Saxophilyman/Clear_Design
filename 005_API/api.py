from pure_robot import RobotState, WATER, make


class RobotAPI:
    def __init__(self, transfer):
        self.transfer = transfer

    def run(self, commands: list[str]) -> RobotState:
        initial_state = RobotState(
            x=0.0,
            y=0.0,
            angle=0,
            cleaning_mode=WATER
        )
        return make(self.transfer, commands, initial_state)