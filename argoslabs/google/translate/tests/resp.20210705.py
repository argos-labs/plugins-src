import json
import pprint

with open('resp.20210705.txt', encoding='utf-8') as ifp:
    jstr = ifp.read()
js = json.loads(jstr)
pprint.pprint(js)
