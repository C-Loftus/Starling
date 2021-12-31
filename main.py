from torch.cuda import init
from Desktop.generic_linux import screen_print, handle_transcription, run_command, run_dictation, run_shell
from Desktop.gnome import *
from Audio.recording import *
from nvidia.transcribe_speech import *
from setup_conf import application_config


import enum

class mode(enum.Enum):
    COMMAND = 1
    DICTATION = 2
    SHELL = 3

# Parses the config and  normalizes audio to the ambient env volume
def init_conf_and_env():
    screen_print("Initializing...", delay=6)
    env.set_vol(initialize=True)
    config_path = "config.yaml"
    application_config(config_path)
    nemo = init_transcribe_conf(TranscriptionConfig)
    screen_print("Initialization complete")
    return nemo[0], nemo[1], nemo[2], nemo[3]
    

def main():

    TORCH_CAST, ASR_MODEL, FILEPATHS, BATCH_SIZE = init_conf_and_env()

    status = mode.COMMAND

    while True:
        print("mainthread")
        record_one_phrase()
        transcriptions = run_inference(TORCH_CAST, ASR_MODEL, FILEPATHS, BATCH_SIZE)
        print(transcriptions)
        screen_print(transcriptions)
        # playsound("Assets/recorded.wav")
        handle_transcription(transcriptions, status)



if __name__ == '__main__':
    main()

# [NeMo E 2021-12-30 16:57:18 segment:155] Loading Assets/recorded.wav via SoundFile raised RuntimeError: `Error opening 'Assets/recorded.wav': System error.`. NeMo will fallback to loading via pydub.