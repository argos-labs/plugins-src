import os
import glob
import chardet

with open('jpn-01.csv', encoding='utf-8') as ifp:
    rs = ifp.read()
    with open('jpn-01.out2.csv', 'w', encoding='euc_jp') as ofp:
        ofp.write(rs)

for f in glob.glob('*.csv'):
    bn = os.path.basename(f)
    with open(f, 'rb') as ifp:
        rs = ifp.read()
        dr = chardet.detect(rs)
        print(f'[{bn}]:{dr}')

# https://docs.python.org/3.7/library/codecs.html#standard-encodings

