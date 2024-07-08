import wave

import numpy as np
import pyaudio

from TTS.tts import TTService

config_combo = [
        # ("TTS_/models/CyberYunfei3k.json", "TTS_/models/yunfei3k_69k.pth"),
        # ("TTS_/models/paimon6k.json", "TTS_/models/paimon6k_390k.pth"),
        # ("TTS_/models/ayaka.json", "TTS_/models/ayaka_167k.pth"),
        # ("TTS_/models/ningguang.json", "TTS_/models/ningguang_179k.pth"),
        # ("TTS_/models/nahida.json", "TTS_/models/nahida_129k.pth"),
        # ("TTS_/models_unused/miko.json", "TTS_/models_unused/miko_139k.pth"),
        # ("TTS_/models_unused/yoimiya.json", "TTS_/models_unused/yoimiya_102k.pth"),
        # ("TTS_/models/noelle.json", "TTS_/models/noelle_337k.pth"),
        # ("TTS_/models_unused/yunfeimix.json", "TTS_/models_unused/yunfeimix_122k.pth"),
        # ("TTS_/models_unused/yunfeineo.json", "TTS_/models_unused/yunfeineo_25k.pth"),
        # ("TTS_/models/yunfeimix2.json", "TTS_/models/yunfeimix2_47k.pth")
        ("TTS_/models_unused/zhongli.json", "TTS_/models_unused/zhongli_44k.pth"),
    ]
for cfg, model in config_combo:
    a = TTService(cfg, model, 'test', 1)
    p = pyaudio.PyAudio()
    audio = a.read('旅行者，今天是星期四，能否威我五十')
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=a.hps.data.sampling_rate,
                    output=True
                    )
    data = audio.astype(np.float32).tostring()
    stream.write(data)
    # Set the output file name
    output_file = "output.wav"

    # Set the audio properties
    num_channels = 1
    sample_width = 2  # Assuming 16-bit audio
    frame_rate = a.hps.data.sampling_rate

    # Convert audio data to 16-bit integers
    audio_int16 = (audio * np.iinfo(np.int16).max).astype(np.int16)

    # Open the output file in write mode
    with wave.open(output_file, 'wb') as wav_file:
        # Set the audio properties
        wav_file.setnchannels(num_channels)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(frame_rate)

        # Write audio data to the file
        wav_file.writeframes(audio_int16.tobytes())