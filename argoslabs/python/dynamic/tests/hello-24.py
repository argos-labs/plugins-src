import sys

name="{name}"

if __name__ == '__main__':
    sys.stdout.write('__name__="%s":, Hello "%s"!' % (__name__, name))
else:  # builtins
    sys.stdout.write('__name__="%s":, Hello "%s"!' % (__name__, name))

sys.exit(0)
