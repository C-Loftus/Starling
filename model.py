from deepspeech import Model
import wave
from io import BytesIO

import ffmpeg
import numpy as np


class SpeechToTextEngine:
    def __init__(self, model_path, scorer_path):
        self.model = Model(model_path=model_path)
        self.model.enableExternalScorer(scorer_path=scorer_path)

    def run(self):
        # audio = BytesIO(audio)
        # with wave.Wave_read(audio) as wav:
        wav = wave.Wave_read("Assets/recorded.wav")
        audio = np.frombuffer(wav.readframes(wav.getnframes()), np.int16)
        result = self.model.stt(audio_buffer=audio)
        return result