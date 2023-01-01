df = df.assign(
    IDS1=lambda x: x['Item Desc 1'].str.extract('^([\w\d\.]+)\s'),
    IDS2=lambda x: x['Item Desc 1'].str.extract('^[\w\d\.]+\s(\d+[- ][\d\.]+)'),
    IDS3=lambda x: x['Item Desc 1'].str.extract('^[\w\d\.]+\s\d+[- ][\d\.]+\s(ZN|ZY|YZ|ZINC|P&O|PHO|Phos|PLAIN|Plain|PLN)'),
    IDS4=lambda x: x['Item Desc 1'].str.extract('^[\w\d\.]+\s\d+[- ][\d\.]+\s(.+)$')
)
df = df.assign(
    ProductType=lambda x: x['IDS2'].str.extract('^([\d]+)[- ]'),
    Grade=lambda x: x['IDS2'].str.extract('[- ]([\d\.]+)$'),
    Finish=lambda x: x['IDS4'].str.extract('(ZN|ZY|YZ|ZINC|P&O|PHO|Olive|Drab|GEOMET 500A|GEOMET 500B|PLAIN|Plain|PLN)'),
    Diameter=lambda x: 'M' + x['IDS1'].str.extract('^M(\d+)X'),
    Pitch1=lambda x: x['IDS1'].str.len(),Pitch2=lambda x: x['IDS1'].str.extract('X([\d\.]+)X'),
    Length=lambda x: x['IDS1'].str.extract('X([\d\.]+)$'),
    Etc=lambda x: x['IDS4']
)
df = df.drop(columns=['IDS1', 'IDS2', 'IDS3', 'IDS4'])
df['Finish'] = df['Finish'].fillna('PLAIN')
df.loc[df['Item Desc 1'].isnull(), 'Finish'] = np.nan
df['Etc'] = df['Etc'].str.replace(
    '^(ZN\s*|ZY\s*|YZ\s*|ZINC\s*|P&O\s*|PHO\s*|Phos\s*|PLAIN\s*|Plain\s*|PLN\s*)','')
df['Etc'] = df['Etc'].str.replace('^(\.\d+)$',r'0\1')
df['Pitch1'] = df['Pitch1'].replace(np.nan, '')
df['Pitch1'] = df['Pitch1'].str.replace('^([1-9]+)',r'X')
df['Pitch1'] = df['Pitch1'].replace(np.nan, 'X')
