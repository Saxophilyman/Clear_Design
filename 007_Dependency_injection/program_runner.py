from command_executor_interface import CommandExecutorInterface


class ProgramRunner:
    def __init__(self, executor: CommandExecutorInterface):
        self.executor = executor

    def run(self, commands: list[str]) -> list[str]:
        results = []

        for command in commands:
            result = self.executor.execute(command)
            print(result)
            results.append(result)

        return results