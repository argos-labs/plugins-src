import requests

headers = {
    'accept': 'application/json',
}

response = requests.get('https://localhost/tasks/30e53981-307a-4003-95c9-d17484110648', headers=headers)