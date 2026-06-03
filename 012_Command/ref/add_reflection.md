касаемо логирования - имеется небольшое нарушение SRP
В реальном проекте имеет смысл вынести log отдельно, а не прописывать его в каждой команде.
Это позволит иметь единую точку для изменений

Start/Stop могли бы иметь поля bool для отслеживания реальных изменений состояний

говоря о CommandExecutor - исполнитель является накопителем команд.
Но можно подумать и о чистой функции. На размышление.

Общая схема:
Command = объект, который инкапсулирует действие

Каждая команда знает:
 - как применить себя к состоянию
 - как описать себя в логе

Исполнитель знает:
 - как выполнить список команд последовательно

```python
    def execute_all(self, initial_state: RobotState) -> tuple[RobotState, List[str]]:
        current_state = initial_state
        logs = []

        for cmd in self.commands:
            logs.append(cmd.log())
            current_state = cmd.execute(current_state)

        return current_state, logs
```
current_state накапливает результат, каждая команда делает из него new_current_state
`cmd.execute(current_state)`  
logs - также накапливает свои логи
