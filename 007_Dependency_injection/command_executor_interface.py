from typing import Protocol

class CommandExecutorInterface(Protocol):
    def execute(self, command: str) -> str:
        ...