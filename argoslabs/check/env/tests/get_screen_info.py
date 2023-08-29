# from screeninfo import get_monitors
from argoslabs.check.env.screeninfo import get_monitors

for m in get_monitors():
    print(str(m))



