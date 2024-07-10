import time

import requests
from tts_service.AuthV3Util import addAuthParams
import logging

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)
# 您的应用ID
APP_KEY = '1fd553a249e9de05'
# 您的应用密钥
APP_SECRET = 'GY3hlLFO9ROPteVnbLr8Fg0G8RjJa3ZK'


class TTSService_YD:
    def __init__(self):
        pass

    def read_save(self, text, filepath):
        q = text
        voiceName = "youxiaofu"
        format = 'wav'

        data = {'q': q, 'voiceName': voiceName, 'format': format}
        addAuthParams(APP_KEY, APP_SECRET, data)
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        res = self.doCall('https://openapi.youdao.com/ttsapi', header, data, 'post')
        self.saveFile(res, file_path=filepath)

    def doCall(self, url, header, params, method):
        if 'get' == method:
            return requests.get(url, params)
        elif 'post' == method:
            return requests.post(url, params, header)

    def saveFile(self, res, file_path):
        contentType = res.headers['Content-Type']
        if 'audio' in contentType:
            fo = open(file_path, "wb")
            fo.write(res.content)
            fo.close()
            print('save file path: ' + file_path)
        else:
            print(str(res.content, 'utf-8'))


class TTSService_PM:
    def __init__(self):
        pass

    def read_save(self, text, filename):
        stime = time.time()
        data = {"text": text}
        tts_resp = requests.post("http://192.168.10.216:5008", json=data)
        tts_resp.raise_for_status()
        tts_data = tts_resp.json()

        audio_resp = requests.get(tts_data["data"]["file_url"], stream=True)
        audio_resp.raise_for_status()

        with open(filename, 'wb') as f:
            for chunk in audio_resp.iter_content(chunk_size=8196):
                f.write(chunk)

        logging.info('VITS Synth Done, time used %.2f' % (time.time() - stime))
