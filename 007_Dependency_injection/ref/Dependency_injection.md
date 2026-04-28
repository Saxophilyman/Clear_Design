Всё же я привык к Java подобному варианту решений, да и в целом с каждым новым примером возникает всё больше удивления и восхищения. 
Как сама идея stateless решение имеет смысл, но оно достаточно минимально упрощённое. В эталоне же просто кладезь концепций. 
Мысли об очередях даже не приходило, такой маленький пример, а в нём и о масштабировании и об асинхронности и об агентах и воркерах. 
Это очень крутой уровень для меня и в полном осознанном смысле я не пробовал строить подобные рабочие системы, 
а всё что использовалось было настолько сокрыто под капотом (предполагаю, что с Kafka работает близкая идея), 
что даже не воспринималось в данном ключе, а здесь как бы показывается внутренний механизм. 
Можно передать не только состояние, но и команду, настроить асинхронную обработку, настроить простую связь с клиентом. 
Сами же минусы для меня выглядят естественными, с их высокой сложностью и увеличивающимся количеством нюансов, пока мне больше кажется, 
что под каждую сложность нужно найти своё решение. Но очень интересно, что будет дальше, ведь есть же концепции и сложнее и универсальнее, но рассмотреть вот так изнутри.. 
Постарался построчно разобраться с эталонным примером "для себя"

Пока высылаю своё скромное видение DI

```python
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
```

```python
from cleaner_interface import CleanerInterface


class CommandExecutor:
    def __init__(self, cleaner: CleanerInterface):
        self.cleaner = cleaner

    def execute(self, command: str) -> str:
        parts = command.split()
        cmd = parts[0]

        if cmd == "move":
            distance = int(parts[1])
            return self.cleaner.move(distance)

        if cmd == "turn":
            angle = int(parts[1])
            return self.cleaner.turn(angle)

        if cmd == "set":
            mode = parts[1]
            return self.cleaner.set_cleaning_mode(mode)

        if cmd == "start":
            return self.cleaner.start_cleaning()

        if cmd == "stop":
            return self.cleaner.stop_cleaning()

        raise ValueError(f"Неизвестная команда: {command}")
```

```python
from typing import Protocol

class CommandExecutorInterface(Protocol):
    def execute(self, command: str) -> str:
        ...
```

```python
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
```