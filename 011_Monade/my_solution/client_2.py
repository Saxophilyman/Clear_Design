from monad_robot_api_2 import api


program = (
        api
        >> api.move(100)
        >> api.turn(-90)
        >> api.set_state("soap")
        >> api.start()
        >> api.move(50)
        >> api.stop()
)

result, final_state = program.run(api.initial_state)

print(result)
print(final_state)