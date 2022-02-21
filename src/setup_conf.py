import yaml
try:
    from nvidia.transcribe_speech import *
except:
    # don't need to print an error message since you already
    # did in main.py
    pass
from collections import ChainMap
import os

class application_config:

    def __init__(self):
        ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
        config_path = os.path.join(ROOT_DIR, "config.yaml")
        
        self.config_path = config_path
        self._load_config()
        self._load_transcription_config()

    def _load_config(self):
        with open(self.config_path) as file:
            try:
                self.config = yaml.safe_load(file)

                alpha = {}
                for dictionary in self.config['alphabet']:
                    alpha.update(dictionary)

                self.alphabet = alpha
                self.time_before_break = self.config['time_before_break']
                self.safety_time = self.config['shell_safety_duration']

                self.browser = self.config['browser']

                web = {}
                for dictionary in self.config[self.browser]:
                    web.update(dictionary)

                self.browser_cmds = web

                self.editor = self.config['editor']
                self.terminal = self.config['terminal']

            except yaml.YAMLError as exc:
                raise Exception("Error loading config file at {}".format(self.config_path))

    def get_config(self):
        return self.config

    def get_time_before_break(self):
        return self.time_before_break

    def get_alphabet(self):
        return self.alphabet

    def get_safety_time(self):
        return self.safety_time

    def get_browser_cmds(self):
        return self.browser_cmds

    def get_context_cmds(self, context: str):
        try:
            ctx_cmds = self.config[context] 
            return dict(ChainMap(*ctx_cmds))
        except:
            return {}
        
    def get_path(self, application: str):
        try:
            path = self.config[application] 
            all = dict(ChainMap(*path))
            return all["exe_path"]
        except:
            return application

    def get_default_model(self):
        for i in self.config['models']:
            if list(i.keys()) == ["default"]:
                return i["default"]

    #  user shouldn't need to change this. all is handled automatically
    def _load_transcription_config(self):
        try:
            TranscriptionConfig.model_path = "src/nvidia/stt_en_conformer_ctc_medium.nemo"
            TranscriptionConfig.pretrained_name = "stt_en_conformer_ctc_medium"
            TranscriptionConfig.cuda = -1
            TranscriptionConfig.audio_dir = "src/Assets/"
            TranscriptionConfig.audio_type = "wav"
            TranscriptionConfig.batch_size=32
        except:
            # this means that the nvidia toolkit is not installed
            pass
