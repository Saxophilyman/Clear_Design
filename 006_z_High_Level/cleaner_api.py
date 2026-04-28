import pure_robot

class RobotCommand:
    # состояние + команда
    def __init__(self, input_state, command):
        self.state = input_state
        self.command = command

def transfer_to_cleaner(message):
    print (message)

##########

import queue
import threading

import pure_robot

# очереди для RobotCommand
input_queue = queue.Queue()
output_queue = queue.Queue()

# воркер и потоки
class ThreadRobo(threading.Thread):
    def __init__(self, in_queue, out_queue):
        super().__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        while True:
            command = self.in_queue.get()

            try:
                cleaner_state = command.state
                cmd = command.command.split()

                if cmd[0] == "move":
                    cleaner_state = pure_robot.move(
                        transfer_to_cleaner,
                        int(cmd[1]),
                        cleaner_state
                    )

                elif cmd[0] == "turn":
                    cleaner_state = pure_robot.turn(
                        transfer_to_cleaner,
                        int(cmd[1]),
                        cleaner_state
                    )

                elif cmd[0] == "set":
                    cleaner_state = pure_robot.set_state(
                        transfer_to_cleaner,
                        cmd[1],
                        cleaner_state
                    )

                elif cmd[0] == "start":
                    cleaner_state = pure_robot.start(
                        transfer_to_cleaner,
                        cleaner_state
                    )

                elif cmd[0] == "stop":
                    cleaner_state = pure_robot.stop(
                        transfer_to_cleaner,
                        cleaner_state
                    )

                else:
                    continue

                result = RobotCommand(
                    input_state=cleaner_state,
                    command="RESULT"
                )
                # на выходную очередь
                self.out_queue.put(result)

            finally:
                self.in_queue.task_done()

# выполнение
def command_to_queue(command):
    input_queue.put(command)

    result = output_queue.get()
    output_queue.task_done()

    return result

# количество воркеров
num_workers = 5
# их запуск
for _ in range(num_workers):
    worker = ThreadRobo(input_queue, output_queue)
    worker.daemon = True
    worker.start()