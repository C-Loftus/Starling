from deepspeech import Model
import wave
from io import BytesIO
import subprocess

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

# stt --model model.pbmm --scorer s.scorer --audio ../Assets/recorded.wav
def runModel(audio_path):

    p = subprocess.Popen(["stt", "--model", "COQUI/model.tflite", "--scorer", "COQUI/s.scorer", "--audio", audio_path], \
                    stdout=subprocess.PIPE)
    return iter(p.stdout.readline, b'')


if __name__ == "__main__":
    output = runModel("Assets/good_test.wav")
    for line in output:
        print(line)