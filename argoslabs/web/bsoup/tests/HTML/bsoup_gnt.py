import re
import sys
from bs4 import BeautifulSoup

hf1_list = (
    'gnt-1.html',
    'gnt-2.html',
    'gnt-3.html',
)

subs = (
    (re.compile(r'[\n\r]+', re.MULTILINE), '\n'),
    (re.compile(r'[ \t]+'), ' '),
)
for hf in hf1_list:
    print('\n\n%s' % ('=' * 100))

    with open(hf, 'rb') as ifp:
        hstr = ifp.read()
    soup = BeautifulSoup(hstr, 'lxml')

    # r = soup.text.strip()
    # print(r)

    fo = soup
    # fo = fo.find('table')
    # fo = fo.find_all('table')
    # print(len(fo))
    # for i, sfo in enumerate(fo):
    #     st = sfo.text
    #     if st.find('72,240') < 0:
    #         continue
    #     for rec, sub_str in subs:
    #         st = rec.sub(st, sub_str)
    #     print('\n\n%s' % ('-' * 100))
    #     print('[%d] %s' % (i+1, st))

    # fo = fo.select('body > table > tr > td > table > tr > td > table > tr > td > table')
    # fo = fo.select('body > table > tr:nth-of-type(4) > table')
    fo = fo.select_one('body > table > tr:nth-of-type(4) > td:nth-of-type(1) > table:nth-of-type(1)')
    fo = fo.select_one('tr:nth-of-type(10) > td:nth-of-type(1) > table:nth-of-type(1)')
    fo = fo.select_one('tr:nth-of-type(1) > td:nth-of-type(1) > table:nth-of-type(1)')
    fo = fo.select_one('tr:nth-of-type(4) > td:nth-of-type(1) > table:nth-of-type(1)')
    fo = fo.find_all('td')
    for f in fo:
        print(f.text.strip())
