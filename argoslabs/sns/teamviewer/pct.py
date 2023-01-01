token = '..'
url_account = 'https://webapi.teamviewer.com//api/v1/account'
url_group = 'https://webapi.teamviewer.com//api/v1/groups'
url_sessions = 'https://webapi.teamviewer.com//api/v1/sessions'
url_meetings = 'https://webapi.teamviewer.com//api/v1/meetings'
url_meetings_id = 'https://webapi.teamviewer.com//api/v1/meetings/m137-49-888'
url_contacts = 'https://webapi.teamviewer.com//api/v1/contacts'
url_devices = 'https://webapi.teamviewer.com//api/v1/devices'
url_teamviewerpolicies = 'https://webapi.teamviewer.com//api/v1/teamviewerpolicies'
import requests
headers = {'Authorization': 'Bearer {}'.format(token)}
# res = requests.get(url_account, headers=headers)
#res = requests.get(url_sessions, headers=headers)
#res = requests.get(url_meetings, headers=headers)
# res = requests.post(url_meetings, headers=headers, schema.json={'subject':'argos-tech-meeting',
#                                                          'start':'2020-11-05T17:00:00Z',
#                                                          'end':'2020-11-05T19:00:00Z'})
res = requests.delete(url_meetings_id, headers=headers)
#res = requests.get(url_contacts, headers=headers)
#res = requests.get(url_devices, headers=headers)
print(res.content)