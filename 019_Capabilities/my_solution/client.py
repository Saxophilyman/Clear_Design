from capability_robot import create_robot


robot = create_robot(
    water=1,
    soap=1
)

print(robot.keys())

result, robot = robot["move"](100)
print(result)
print(robot.keys())

result, robot = robot["turn"](-90)
print(result)
print(robot.keys())

result, robot = robot["set_soap"]()
print(result)
print(robot.keys())

result, robot = robot["start"]()
print(result)
print(robot.keys())

result, robot = robot["move"](50)
print(result)
print(robot.keys())

result, robot = robot["stop"]()
print(result)
print(robot.keys())

result, robot = robot["status"]()
print(result.message)