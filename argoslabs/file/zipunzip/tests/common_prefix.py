import os
from pprint import pprint

flist = list()
flist.append(os.path.abspath(r'__init__.py'))
flist.append(os.path.abspath(r'../__init__.py'))
flist.append(os.path.abspath(r'../..\__init__.py'))
pprint(flist)
print(f'{"*" * 100}')

x = list()
for f in flist:
    x.append(f.split(os.path.sep))
pprint(x)
print(f'{"*" * 100}')
lcp = os.path.commonprefix(x)
pprint(lcp)
print(f"'{os.path.sep.join(lcp)}'")

# x.append(os.path.abspath(r'v:/Bots').split(os.path.sep))
