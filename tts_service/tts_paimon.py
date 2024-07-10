import time
import requests
import logging

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


class TTService:
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
