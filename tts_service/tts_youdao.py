import requests
from tts_service.AuthV3Util import addAuthParams
import logging

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)
# 您的应用ID
APP_KEY = '1fd553a249e9de05'
# 您的应用密钥
APP_SECRET = 'GY3hlLFO9ROPteVnbLr8Fg0G8RjJa3ZK'


class TTSService:
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
