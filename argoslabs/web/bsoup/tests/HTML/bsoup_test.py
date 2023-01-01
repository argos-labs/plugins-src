from bs4 import BeautifulSoup

hf1_list = (
    '1.html',
    '2.html',
    '3.html',
    '4.html',
    '5.html',
)

for hf in hf1_list:
    print('\n\n%s' % ('=' * 100))

    with open(hf) as ifp:
        hstr = ifp.read()
    soup = BeautifulSoup(hstr, 'html.parser')


    # fa = soup.find_all('input', id="endecaKeyword")
    # if fa:
    #     for t in fa:
    #         print('<%s>' % t.attrs['value'])


    fa = soup.find_all(name='div', class_="search-list-view__content")
    if fa:
        for t in fa:
            rs = t.find('h2')
            print('<%s>' % rs.text.strip())

    fa = soup.find_all(name='div', class_="search-list-view__price-container")
    if fa:
        for t in fa:
            rs = t.find(name='span', class_='gcprice-value')
            print('<%s>' % rs.text.strip(), end=', ')
            rs = t.find(name='span', class_='gcprice-unit')
            print('<%s>' % rs.text.strip())


hf2_list = (
    '6.html',
    '7.html',
    '8.html',
    '9.html',
    '10.html',
)

for hf in hf2_list:
    print('\n\n%s' % ('=' * 100))

    with open(hf) as ifp:
        hstr = ifp.read()
    soup = BeautifulSoup(hstr, 'html.parser')

    # for one item

    # fa = soup.find_all('h2', class_="pdp")
    # if fa:
    #     for t in fa:
    #         rs = t
    #         print('<%s>' % rs.text.strip())

    fa = soup.find_all(name='h3', class_="pdp")
    if fa:
        for t in fa:
            rs = t
            print('<%s>' % rs.text.strip())

    fa = soup.find_all(name='span', id="listPriceDiv")
    if fa:
        for t in fa:
            rs = t
            print('<%s>' % rs.text.strip())

    # for list

    fa = soup.find_all(name='h4', class_="ui header v4-tn-title")
    if fa:
        for t in fa:
            rs = t
            print('<%s>' % rs.text.strip())

    fa = soup.find_all(name='span', class_="v4-tn-your-price")
    if fa:
        for t in fa:
            rs = t
            print('<%s>' % rs.text.strip())

