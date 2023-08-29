# import sphinxapi
# client = sphinxapi.SphinxClient()
# client.SetServer('192.168.35.241', 36307)
# qr = client.Query('apple')
# print(qr)


import pymysql
db = pymysql.connect(host='192.168.35.241',port=36307,user='',passwd='',charset='utf8',db='')
cur = db.cursor()
# qry = 'desc engdict_index'
sphinx_qry = 'apple'
qry = f'SELECT id, word, part from engdict_index WHERE MATCH(\'{sphinx_qry}\') limit 20;'
cur.execute(qry)
row = cur.fetchall()
print(row)
cur.close();db.close()

