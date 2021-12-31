import yaml
from nvidia.transcribe_speech import *

class application_config:
    def __init__(self, config_path):
        self.config_path = config_path
        self._load_config()
        self._load_transcription_config()

    def _load_config(self):
        with open(self.config_path) as file:
            try:
                self.config = yaml.safe_load(file)
                self.alphabet = self.config['Alphabet']
                self.time_before_break = self.config['Time_before_break']
            except yaml.YAMLError as exc:
                print("Error in yaml syntax or naming", exc)
                exit(1)

    def get_config(self):
        return self.config

    def get_time_before_break(self):
        return self.time_before_break

    def get_alphabet(self):
        return self.alphabet

    #  user shouldn't need to change this. all is handled automatically
    def _load_transcription_config(self):
        TranscriptionConfig.model_path = "nvidia/stt_en_conformer_ctc_medium.nemo"
        TranscriptionConfig.pretrained_name = "stt_en_conformer_ctc_medium"
        TranscriptionConfig.cuda = -1
        TranscriptionConfig.audio_dir = "Assets/"
        TranscriptionConfig.audio_type = "wav"
        TranscriptionConfig.batch_size=32
        # TranscriptionConfig.overwrite_transcripts = True



if __name__ == '__main__':
    config_path = "config.yaml"
    conf = application_config(config_path)
    print(conf.get_config()["Alphabet"])