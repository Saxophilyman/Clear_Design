from cleaner_api import api

workflow = "100 move -90 turn soap set start 50 move stop"

state = api(workflow)

print(state)