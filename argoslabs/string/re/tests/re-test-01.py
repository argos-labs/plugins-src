import re


def test_01():
    rec = re.compile(r'\w+')
    r = rec.findall('hello tom and jerry')
    print(r)


def test_02():
    rec = re.compile(r'tom|jerry')
    r = rec.findall('hello tom and jerry')
    print(r)


if __name__ == '__main__':
    test_01()
    test_02()

