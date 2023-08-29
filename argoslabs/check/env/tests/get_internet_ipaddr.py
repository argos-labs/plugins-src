import requests

# ip = requests.get('https://api.ipify.org').text
rp = requests.get('https://api.ipify.org')
if rp.status_code // 10 != 20:
    print('Public IP address is:', rp.text)
else:
    print('Cannot get public IP address')
