import os, random, string

length = 13
chars = string.ascii_letters + string.digits + '!@#$%^&*()'
random.seed = (os.urandom(1024))
pg = ''.join(random.choice(chars) for i in range(length))
print(pg)
