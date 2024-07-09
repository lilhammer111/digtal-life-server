import uuid
import base64
import hashlib
import json
import time
import requests

YOUDAO_URL = 'https://openapi.youdao.com/asrapi'

APP_KEY = 'your_app_key'

APP_SECRET = 'your_app_secret'


class ASRService():
    def __init__(self):
        pass

    def truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def encrypt(self, signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()

    def do_request(self, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(YOUDAO_URL, data=data, headers=headers)

    def infer(self, wav_path):
        lang_type = "zh-CHS"  # 'zh-CHS' yue
        with open(wav_path, 'rb') as file_wav:
            q = base64.b64encode(file_wav.read()).decode('utf-8')
        data = {}
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = APP_KEY + self.truncate(q) + salt + curtime + APP_SECRET
        sign = self.encrypt(signStr)
        data['appKey'] = APP_KEY
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign
        data['signType'] = "v2"
        data['langType'] = lang_type
        data['rate'] = 16000
        data['format'] = 'wav'
        data['channel'] = 1
        data['type'] = 1

        response = self.do_request(data)
        data = response.content

        result_str = data.decode('utf-8')
        data = json.loads(result_str)
        result_text = data["result"][0]
        print(result_text)
        return result_text


if __name__ == '__main__':
    service = ASRService()

    # print(wav_path)
    wav_path = './test_wavs/A1_NAME1.wav'
    result = service.infer(wav_path)
    print(result)
