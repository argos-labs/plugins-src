import requests

headers = {
    'accept': 'application/json',
    # requests won't add a boundary if this header is set when you pass files=
    # 'Content-Type': 'multipart/form-data',
}

params = {
    'api_token': 'de1af14b249fbb5df0380cf967b8bf3c',
}

files = {
    'file': open('inbody.png', 'rb'),
}

response = requests.post('https://easyocr.argos-labs.com/ocr', params=params, headers=headers, files=files)
