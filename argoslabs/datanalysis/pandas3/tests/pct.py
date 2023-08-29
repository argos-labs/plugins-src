import json
with open('C:/Users/MyGuide/Desktop/testbot/xtracta/results/163081225(1)-apple.json') as f:
    t = json.load(f)
dt = t['documents_response']['document']['field_data']['field']
dt = t['documents_response']['document']['field_data']['field_set']['row']
import pandas as pd
df = pd.DataFrame(dt)
f.close()
df.to_csv('fields.csv')
# df = pd.read_json('output/163081225(1).json')
# print(df.iloc[[0,1]])