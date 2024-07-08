import logging
import time

import requests

from ASR.rapid_paraformer import RapidParaformer


class ASRService():
    # def __init__(self, config_path):
    #     logging.info('Initializing ASR Service...')
    #     self.paraformer = RapidParaformer(config_path)
    #
    # def infer(self, wav_path):
    #     stime = time.time()
    #     result = self.paraformer(wav_path)
    #     logging.info('ASR Result: %s. time used %.2f.' % (result, time.time() - stime))
    #     return result[0]

    def __init__(self):
        pass

    def file_upload(self, wav_path):
        upload_api_url = "http://192.168.10.201:8888/api/upload"
        source = 1
        files = {"files": open(wav_path, "rb")}
        data = {'source': source}

        response = requests.post(upload_api_url, files=files, data=data)
        return response.json()

    def infer(self, wav_path):
        ASR_API_URL = "http://192.168.10.220:5052/api/spe2text/ai_en"
        audio_url = self.file_upload(wav_path)
        sid = "1234"
        data = {'sid': sid, 'audio_url': audio_url}
        response = requests.post(ASR_API_URL,data=data)

        return response.json()


if __name__ == '__main__':
    service = ASRService()

    # print(wav_path)
    wav_path = 'ASR/test_wavs/'
    result = service.infer(wav_path)
    print(result)
