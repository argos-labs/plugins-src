import os

keys = [x for x in os.environ.keys()]
for key in keys:
    print(f'<{key}>=<{os.environ[key]}>')

