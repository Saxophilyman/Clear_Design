from robot import Robot
from command_executor import CommandExecutor
from program_runner import ProgramRunner


def main():
    commands = [
        "move 100",
        "turn -90",
        "set soap",
        "start",
        "move 50",
        "stop"
    ]

    robot = Robot()
    executor = CommandExecutor(robot)
    runner = ProgramRunner(executor)

    runner.run(commands)


if __name__ == "__main__":
    main()