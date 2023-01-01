import os


def pywalker(path):
    for root, dirs, files in os.walk(path):
        # for dir in dirs:
        #     d = os.path.join(root, dir)
        #     assert(os.path.isdir(d))
        #     print(d)
        for file_ in files:
            f = os.path.join(root, file_)
            print(f)
            assert (os.path.isfile(f))

if __name__ == '__main__':
    pywalker('C:\work')