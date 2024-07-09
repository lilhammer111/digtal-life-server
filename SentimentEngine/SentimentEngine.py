import requests
import logging

SentimentEngine_URL = 'http://192.168.10.225:8081/classify2'


class SentimentEngine():
    def __init__(self):
        logging.info('Initializing Sentiment Engine...')

    def infer(self, text):
        input_text = {
            'text': text
        }
        result = requests.post(url=SentimentEngine_URL, json=input_text)
        json_result = result.json()
        return json_result['result']
