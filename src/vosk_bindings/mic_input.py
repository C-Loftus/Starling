# most up to date
# Default for vosk bindings
import os
import queue
import sounddevice as sd
import vosk
import sys

import os, sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


import Desktop.mode_functions as status

class VoskModel:
    def __init__(self, conf):
        ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        self.MODEL_PATH=os.path.join(ROOT_DIR,"vosk_bindings", "model")
    
        vosk.SetLogLevel(-1)
        self.model = vosk.Model(self.MODEL_PATH)
        self.tmp_cmd_list = None
        self.conf = conf
        self.cmd_list = self.base_command_mode_command_list()

        self.q = queue.Queue()

    def callback(self,indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def record_and_infer(self, mode, device=sd.default.device, samplerate=16000):
        try:
        
            if not os.path.exists(self.MODEL_PATH):
                print ("Please download a model for your language from https://alphacephei.com/vosk/models")
                print ("and unpack as 'model' in folder: {}".format(self.MODEL_PATH))
                exit(0)
            device_info = sd.query_devices(device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            samplerate = int(device_info['default_samplerate'])
        
        
            with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=device, dtype='int16',
                                    channels=1, callback=self.callback):
                                    

                    if mode == status.mode.COMMAND:
                        self.tmp_cmd_list = self.cmd_list + self.tmp_command_mode_list(self.conf)
                        # You can also specify the possible word or phrase list as JSON list, the order doesn't have to be strict
                        rec = vosk.KaldiRecognizer(self.model, samplerate, self.tmp_cmd_list)
                    else:
                        rec = vosk.KaldiRecognizer(self.model, samplerate)

                    while True:
                        data = self.q.get()
                        if rec.AcceptWaveform(data):
                            try:
                                return rec.Result().split("\"")[3]
                            except:
                                return ""
                        # TODO pass partial to decoder
                        # else:
                        #     print(rec.PartialResult())

        except Exception as e:
            sys.exit(type(e).__name__ + ': ' + str(e))

# Vosk Model  only accepts a list of strings within another string so
#  the code isn't particularly pretty with the string manipulation

    def base_command_mode_command_list(self):
        modes="\"command sleep dictation shell mode\""

        numbers = "\"one two three four five six seven eight nine zero\""
        modifiers = "\"shift alt control super enter win sentence\""


        alphabet = self.conf.get_alphabet()
        alphabet = ' '.join(key for key, _ in alphabet.items())
        alphabet = "\"" + alphabet + "\""

        aliases = self.conf.get_config()
        aliases = ' '.join(key.lower() for key in aliases if "_" not in key)
        aliases = "\"" + aliases + "\""

        window_actions = '\"focus start close maximize minimize\"'
        apps = '\"editor terminal browser this\"'

        indicator = '\"quit application timer start stop\"'

        return "[{},{},{},{},{},{},{},{},".\
            format(numbers, modifiers, alphabet, window_actions, modes, apps, indicator, aliases)

    def tmp_command_mode_list(self, conf):
        import Desktop.xdotool_wrappers as xdotool
    
        context = xdotool.get_focused_window_name()
        context_cmds = conf.get_context_cmds(context)
        res = ' '.join(key for key, _ in context_cmds.items() if key != "exe_path")
        return '\"'+ res + '\"]'
