# from fleep import get as fleep_get
import fleep


# print(dir(fleep))
with open("test0003.mp3", "rb") as file:
    info = fleep.get(file.read(128))

print(info.type)
print(info.extension)
print(info.mime)
