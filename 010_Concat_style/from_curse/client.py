from cleaner_api import CatApi

api = CatApi()
s = api.exec('100 move -90 turn soap set start 50 move stop')
print(s)