from deepspeech import Model
import wave
from io import BytesIO
import subprocess

import ffmpeg
import numpy as np
import nemo.collections.asr as nemo_asr

# TODO https://stt.readthedocs.io/en/latest/Python-API.html
from stt import Model
# stt_en_conformer_ctc_medium.nemo

MODEL_PATH = "COQUI/model.tflite"
SCORER_PATH = "COQUI/large_vocabulary.scorer"

# class SpeechToTextEngine:
#     def __init__(self, model_path, scorer_path):
#         self.model = Model(model_path=model_path)
#         self.model.enableExternalScorer(scorer_path=scorer_path)

#     def run(self):
#         wav = wave.Wave_read("Assets/recorded.wav")
#         audio = np.frombuffer(wav.readframes(wav.getnframes()), np.int16)
#         result = self.model.stt(audio_buffer=audio)
#         return result

# stt --model model.pbmm --scorer s.scorer --audio ../Assets/recorded.wav
def runModel(audio_path):

    p = subprocess.Popen(["stt", "--model", MODEL_PATH, "--scorer", SCORER_PATH, "--audio", audio_path], \
                    stdout=subprocess.PIPE)
    return iter(p.stdout.readlinbe, b'')


def runNEMO():
    asr_model = nemo_asr.models.EncDecCTCModelBPE.from_pretrained(model_name="nvidia/stt_en_conformer_ctc_medium")


if __name__ == "__main__":
    output = runModel("Assets/good_test.wav")
    for line in output:
        print(line)