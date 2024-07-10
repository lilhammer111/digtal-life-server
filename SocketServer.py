import argparse
import os
import socket
import time
import logging
import traceback

import librosa
import soundfile

from SentimentEngine import SentimentEngine
from utils.FlushingFileHandler import FlushingFileHandler
from ASR import ASRService
from GPT import llm
from tts_service.tts import TTSService_YD, TTSService_PM

console_logger = logging.getLogger()
console_logger.setLevel(logging.INFO)
FORMAT = '%(asctime)s %(levelname)s %(message)s'
console_handler = console_logger.handlers[0]
console_handler.setFormatter(logging.Formatter(FORMAT))
console_logger.setLevel(logging.INFO)
file_handler = FlushingFileHandler("log.log", formatter=logging.Formatter(FORMAT))
file_handler.setFormatter(logging.Formatter(FORMAT))
file_handler.setLevel(logging.INFO)
console_logger.addHandler(file_handler)
console_logger.addHandler(console_handler)


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Unsupported value encountered.')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=33333)
    parser.add_argument("--character", type=str, default="alfaright", nargs='?', required=False)
    parser.add_argument("--kimi-key", type=str, default="sk-TtCrzHinIyVKEeaAvIuQPDZtixxADloU9QDlwVoYNdxh2tf9",
                        required=False)
    parser.add_argument("--kimi-model", type=str)
    return parser.parse_args()


class Server:
    def __init__(self, args):
        # SERVER STUFF
        self.addr = None
        self.conn = None
        logging.info('Initializing Server...')
        self.host = "0.0.0.0"
        self.port = args.port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1048576)
        self.s.bind((self.host, self.port))
        self.tmp_recv_file = 'tmp/server_received.wav'
        self.tmp_proc_file = 'tmp/server_processed.wav'

        # hard coded character map
        self.char_name = {
            'alfaright': 'character_paimon',
        }

        # PARAFORMER
        self.paraformer = ASRService.ASRService()

        # CHAT GPT
        self.kimi = llm.KimiService(args)

        # tts_service
        # self.tts = TTSService_YD()  # 有道API
        self.tts = TTSService_PM()  # 派蒙API

        # Sentiment Engine
        self.sentiment = SentimentEngine.SentimentEngine()

    def handle(self):
        """handle client request"""
        logging.info(f"Connected by {self.addr}")
        self.conn.sendall(b'%s' % self.char_name[arguments.character].encode())
        while True:
            try:
                file = self.__receive_file()
                # print('file received: %s' % file)
                with open(self.tmp_recv_file, 'wb') as f:
                    f.write(file)
                    logging.info('WAV file received and saved.')
                ask_text = self.process_voice()

                resp_text = self.kimi.answer(ask_text)
                self.send_voice(resp_text)
                self.notice_stream_end()
            except Exception as e:
                logging.error(e.__str__())
                logging.error(traceback.format_exc())
                break

    def listen(self):
        """
        listen socket connection request
        """
        self.s.listen()

        logging.info(f"Server is listening on {self.host}:{self.port}...")
        while True:
            self.conn, self.addr = self.s.accept()
            self.handle()
        # self.conn.close()
        # logging.info(f"Connection closed.")

    def notice_stream_end(self):
        time.sleep(0.5)
        self.conn.sendall(b'stream_finished')

    def send_voice(self, resp_text, senti_or=None):
        self.tts.read_save(resp_text, self.tmp_proc_file)

        with open(self.tmp_proc_file, 'rb') as f:
            senddata = f.read()
        if senti_or:
            senti = senti_or
        else:
            senti = self.sentiment.infer(resp_text)
        senddata += b'?!'
        senddata += b'%i' % senti
        self.conn.sendall(senddata)
        time.sleep(0.5)
        logging.info('WAV SENT, size %i' % len(senddata))

    def __receive_file(self):
        file_data = b''
        while True:
            data = self.conn.recv(1024)
            # print(data)
            self.conn.send(b'sb')
            if data[-2:] == b'?!':
                file_data += data[0:-2]
                break
            if not data:
                # logging.info('Waiting for WAV...')
                continue
            file_data += data

        return file_data

    def fill_size_wav(self):
        with open(self.tmp_recv_file, "r+b") as f:
            # Get the size of the file
            size = os.path.getsize(self.tmp_recv_file) - 8
            # Write the size of the file to the first 4 bytes
            f.seek(4)
            # set wav file ChunkSize manually
            f.write(size.to_bytes(4, byteorder='little'))
            f.seek(40)
            # set wav file Subchunk2Size manually
            f.write((size - 28).to_bytes(4, byteorder='little'))
            f.flush()

    def process_voice(self):
        # stereo to mono
        self.fill_size_wav()
        y, sr = librosa.load(self.tmp_recv_file, sr=None, mono=False)
        y_mono = librosa.to_mono(y)
        y_mono = librosa.resample(y_mono, orig_sr=sr, target_sr=16000)
        soundfile.write(self.tmp_recv_file, y_mono, 16000)
        text = self.paraformer.infer(self.tmp_recv_file)

        return text


if __name__ == '__main__':
    try:
        arguments = parse_args()
        s = Server(arguments)
        s.listen()
    except Exception as e:
        logging.error(e.__str__())
        logging.error(traceback.format_exc())
        raise e
