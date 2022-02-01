#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
MODEL_PATH='src/vosk_bindings/model'
AUDIO_PATH='src/Assets/test.wav'

class VoskModel:
    def __init__(self):
        self.model = Model(MODEL_PATH)

    def run_inference(self, mode,conf, audio_path=AUDIO_PATH):
        if not os.path.exists(MODEL_PATH):
            print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            exit (1)

        wf = wave.open(audio_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print ("Audio file must be WAV format mono PCM.")
            exit (1)


        # You can also specify the possible word or phrase list as JSON list, the order doesn't have to be strict
        rec = KaldiRecognizer(self.model, wf.getframerate())

        results = []
        results.append(rec.FinalResult())
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                results.append(rec.Result())
            else:
                rec.PartialResult()

        results.append(rec.FinalResult())
        output = ""
        for i in results:
            output += i.split("\"")[3] + " "
        output.strip()
        return output


    def command_mode_command_list(conf):
        letters = "one two three four five six seven eight nine zero"
        modifiers = "shift alt ctrl super enter"
        alphabet = conf.get_alphabet()
        ctx = conf.get_context_cmds("command_mode")

if __name__ == "__main__":
    mode=None
    conf = None
    v = VoskModel()
    p =v.run_inference(mode,conf)
    print(p)