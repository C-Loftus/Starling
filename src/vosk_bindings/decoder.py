#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
MODEL_PATH='src/vosk_bindings/model'
AUDIO_PATH='src/Assets/recorded.wav'

import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


import Desktop.mode_functions as status

class VoskModel:
    def __init__(self, conf):
        self.model = Model(MODEL_PATH)
        self.tmp_cmd_list = None
        self.conf = conf
        self.cmd_list = self.base_command_mode_command_list()

    def run_inference(self, mode, audio_path=AUDIO_PATH):
        if not os.path.exists(MODEL_PATH):
            print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            exit (1)

        wf = wave.open(audio_path, "rb")
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            print ("Audio file must be WAV format mono PCM.")
            exit (1)

        if mode == status.mode.COMMAND:
            self.tmp_cmd_list = self.cmd_list + self.tmp_command_mode_list(self.conf)
            # You can also specify the possible word or phrase list as JSON list, the order doesn't have to be strict
            rec = KaldiRecognizer(self.model, wf.getframerate(), self.tmp_cmd_list)
        else:
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
        # TODO check
        output.strip()
        return output

# Vosk Model  only accepts a list of strings within another string so
#  the code isn't particularly pretty with the string manipulation

    def base_command_mode_command_list(self):
        modes="\"command sleep dictation shell mode\""

        letters = "\"one two three four five six seven eight nine zero\""
        modifiers = "\"shift alt control super enter win\""

        alphabet = self.conf.get_alphabet()
        res = ' '.join(key for key, _ in alphabet.items())
        res = "\"" + res + "\""

        window_actions = '\"focus start close maximize minimize\"'
        apps = '\"editor terminal browser this\"'
        return "[{},{},{},{}, {},".format(letters, modifiers, res, window_actions, modes)

    def tmp_command_mode_list(self, conf):
        import Desktop.xdotool_wrappers as xdotool
    
        context = xdotool.get_focused_window_name()
        context_cmds = conf.get_context_cmds(context)
        res = ' '.join(key for key, _ in context_cmds.items())
        return '\"'+ res + '\"]'

    

if __name__ == "__main__":
    mode=None
    conf = None
    v = VoskModel()
    p =v.run_inference(mode,conf)
    print(p)