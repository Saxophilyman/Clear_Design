from typing import Protocol


class CleanerInterface(Protocol):
    def move(self, distance: int) -> str:
        ...

    def turn(self, angle: int) -> str:
        ...

    def set_cleaning_mode(self, mode: str) -> str:
        ...

    def start_cleaning(self) -> str:
        ...

    def stop_cleaning(self) -> str:
        ...