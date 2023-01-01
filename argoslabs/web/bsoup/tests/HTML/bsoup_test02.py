from bs4 import BeautifulSoup

hf1_list = (
    '17.html',
)

for hf in hf1_list:
    print('\n\n%s' % ('=' * 100))

    with open(hf, encoding='utf8') as ifp:
        hstr = ifp.read()
    soup = BeautifulSoup(hstr, 'lxml')

    # r = soup.text.strip()
    # print(r)

    kwargs = {
        'name': 'div',
        # 'class': 's-image',
        'data-asin': True,
        'data-index': True,
        # "class": 'sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 AdHolder sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28',
    }
    fa = soup.find_all(**kwargs)
    if fa:
        for t in fa:
            if t.text.lower().find('xike 4 pcs') >= 0:
                pass
            rs = t.find('h2')
            if rs:
                print('<%s>' % rs.text.strip())

    # fa = soup.find_all(name='div', class_="search-list-view__price-container")
    # if fa:
    #     for t in fa:
    #         rs = t.find(name='span', class_='gcprice-value')
    #         print('<%s>' % rs.text.strip(), end=', ')
    #         rs = t.find(name='span', class_='gcprice-unit')
    #         print('<%s>' % rs.text.strip())

