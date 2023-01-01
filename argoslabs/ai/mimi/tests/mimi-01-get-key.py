
# https://mimi.readme.io/docs/first-step#section-%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9%E3%83%88%E3%83%BC%E3%82%AF%E3%83%B3%E3%81%AE%E7%99%BA%E8%A1%8C

import os
import sys
import csv
import json
import asyncio
import requests
import websockets

# ################################################################################
# SAMPLES_PER_CHUNK = 1024
# async def recognize(token, file_data):
#     headers = {
#         "Authorization": "Bearer {}".format(token),
#         "x-mimi-process": "nict-asr",  # when using NICT engine use "nict-asr"
#         "x-mimi-input-language": "ja",
#         "Content-Type": "audio/x-pcm;bit=16;rate=16000;channels=1",
#     }
#
#     try:
#         resp = ""
#         async with websockets.connect(
#                 "wss://service.mimi.fd.ai:443",
#                 extra_headers=headers
#         ) as ws:
#
#             file_size = len(file_data)
#             sent_size = 0
#             while sent_size < file_size:
#                 await ws.send(file_data[sent_size:sent_size +
#                                                   SAMPLES_PER_CHUNK * 2])
#                 sent_size += SAMPLES_PER_CHUNK * 2
#             await ws.send(json.dumps({"command": "recog-break"}))
#             while True:
#                 resp = await ws.recv()
#                 print(resp)
#                 if json.loads(resp)['status'] == 'recog-finished':
#                     print('recog-finished: received all from server.')
#                     break
#
#     except websockets.exceptions.ConnectionClosed:
#         print('connection closed from server')
#
#     return resp


################################################################################
class Mimi(object):
    LANGS = ('ja', 'en', 'es', 'fr', 'id', 'ko', 'my', 'th', 'vi', 'zh')

    # ==========================================================================
    def __init__(self, app_id, client_id, secret):
        self.app_id = app_id
        self.client_id = client_id
        self.secret = secret
        # for internal
        self.token = None
        self.get_token()

    # ==========================================================================
    def get_token(self):
        files = {
            'grant_type': (None,
                           'https://auth.mimi.fd.ai/grant_type/client_credentials'),
            'client_id': (None, f'{self.app_id}:{self.client_id}'),
            'client_secret': (None, f'{self.secret}'),
        }
        data = {
            'scope': 'https://apis.mimi.fd.ai/auth/asr/websocket-api-service;'
                     'https://apis.mimi.fd.ai/auth/asr/http-api-service;'
                     'https://apis.mimi.fd.ai/auth/nict-asr/http-api-service;'
                     'https://apis.mimi.fd.ai/auth/nict-asr/websocket-api-service;'
                     'https://apis.mimi.fd.ai/auth/nict-tts/http-api-service;'
                     'https://apis.mimi.fd.ai/auth/nict-tra/http-api-service',
        }

        rp = requests.post('https://auth.mimi.fd.ai/v2/token', files=files,
                           data=data)
        jd = json.loads(rp.content)
        # print(rp.content)
        if rp.status_code // 10 != 20:
            raise ReferenceError(f'Cannot get token: {jd.get("error")}')
        self.token = jd['accessToken']
        return self.token

    # ==========================================================================
    def audio_recognize(self, raw_file):
        if not os.path.exists(raw_file):
            raise IOError(f'Cannot read raw file {raw_file}')
        try:
            headers = {
                'Content-Type': 'audio/x-pcm;bit=16;rate=16000;channels=1',
                'x-mimi-process': 'asr',
                'x-mimi-input-language': 'ja',
                'Authorization': f'Bearer {self.token}',
            }
            with open(raw_file, 'rb') as ifp:
                file_data = ifp.read()
            rp = requests.post('https://service.mimi.fd.ai/',
                               headers=headers, data=file_data)
            if rp.status_code // 10 != 20:
                raise ReferenceError(f'Cannot recognize audio: {rp.content.decode()}')
            jd = json.loads(rp.content)
            ch = ('pronunciation','result','start','end')
            c = csv.writer(sys.stdout, lineterminator='\n')
            c.writerow(ch)
            for rd in jd.get('response',[]):
                row = [
                    rd['pronunciation'], rd['result'],
                    rd['time'][0], rd['time'][1]
                ]
                c.writerow(row)
        except Exception as e:
            raise

    # ==========================================================================
    def tts(self, lang, text, outfile):
        if lang not in self.LANGS:
            raise ValueError(f'Not supported language "{lang}"')
        headers = {
            'Authorization': f'Bearer {self.token}',
        }
        data = {
            'text': text,
            'lang': lang,
            'engine': 'nict',
        }

        url = 'https://tts.mimi.fd.ai/speech_synthesis'
        resp = requests.post(url, headers=headers, data=data)
        if resp.status_code // 10 != 20:
            msg = f'TTS error: {resp.content.decode()}'
            sys.stderr.write(f'{msg}\n')
            # raise RuntimeError(msg)
        with open(outfile, 'wb') as fout:
            fout.write(resp.content)

    # ==========================================================================
    def tranlate(self, in_lang, text, out_lang):
        if in_lang not in self.LANGS:
            raise ValueError(f'Not supported language "{in_lang}" for input')
        if out_lang not in self.LANGS:
            raise ValueError(f'Not supported language "{out_lang}" for output')
        headers = {
            'Authorization': f'Bearer {self.token}',
        }
        data = {
            'text': text,
            'source_lang': in_lang,
            'target_lang': out_lang,
        }

        url = 'https://tra.mimi.fd.ai/machine_translation'
        resp = requests.post(url, headers=headers, data=data)
        if resp.status_code // 10 != 20:
            msg = f'Translate error: {resp.content.decode()}'
            sys.stderr.write(f'{msg}\n')
            # raise RuntimeError(msg)
        else:
            print(resp.json())


################################################################################
if __name__ == '__main__':
    app_id = '7246da6c9b904c70b397cc9d79c87df3'
    client_id = '1bb787b35c0e4e02927fd265d36b6a08'
    secret = '9d80babb8f6978f9edd1025a7711bc97c89403a0ad3141cc08e5cb52c23cccce6c' \
             '666c2b171fcace7bce37d600c78bfcd23e592408a6dec13c98568bd4405b64a271' \
             'f26364dd20b3a463463bd97e3ceb8362ce5654ffaa6e244be4845c0b2112ac3dd6' \
             '943b84c2d9e6029df70c9ba2b5ee9bda61a5121549be920f66b37f126a496df3a8' \
             '39ee52f5ae71c021c5eb66c623558840cdbc874108e734c1271f1bfdafa9f98262' \
             '728d7c607b00e6dd00d6c9bffa5f790f48b5d801195b9ba4156bd7dc500445dd97' \
             'ac2eac4379f88dde58c24f24606d5f5f9693587212cbc396651de387909132c474' \
             'ae3720269ce748bd12412f0df0f1000cbcc6bf4b31cd4948d6'
    try:
        mm = Mimi(app_id, client_id, secret)
        mm.audio_recognize('mimi.example/audio.raw')
        # mm.tts('ko', '안녕하세요? 저는 Jerry 입니다.', 'tts-out.wav')
        # mm.tts('ja', 'フェアリーデバイセズ共通サインイン', 'tts-out.wav')
        mm.tts('en', 'Hello world!', 'tts-out.wav')
        mm.tranlate('en', 'Hello world!', 'ja')  # ja => other or other => ja
        mm.audio_recognize('mimi.example/audio.raw')
    except Exception as e:
        sys.stderr.write(f'Error: {e}')

    # output
    # pronunciation,result,start,end
    # トリアエズ,とりあえず,460,960
    # ハラゴシラエ,腹ごしらえ,960,1690
    #
    # ['こんにちは。']
    #
    # pronunciation,result,start,end
    # トリアエズ,とりあえず,460,960
    # ハラゴシラエ,腹ごしらえ,960,1690