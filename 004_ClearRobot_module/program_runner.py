from command_executor import CommandExecutor


class ProgramRunner:
    def __init__(self, executor: CommandExecutor):
        self.executor = executor

    def run(self, commands: list[str]) -> list[str]:
        results = []

        for command in commands:
            result = self.executor.execute(command)
            print(result)
            results.append(result)

        return results