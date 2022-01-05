from sounddevice import sleep
from Desktop.generic_linux import screen_print, detect_time_for_break
from Desktop.gnome import *
from Desktop.mode_functions import handle_transcription, mode
from Audio.recording import *
from nvidia.transcribe_speech import *
from setup_conf import application_config

# Parses the config and  normalizes audio to the ambient env volume
def init_conf_and_env():
    screen_print("Initializing...", delay=6)

    env.set_vol(initialize=True)
    
    config_path = "config.yaml"
    app_conf = application_config(config_path)
    detect_time_for_break(app_conf.get_time_before_break())

    nemo = init_transcribe_conf(TranscriptionConfig)

    screen_print("Initialization complete")
    return nemo[0], nemo[1], nemo[2], nemo[3], app_conf
    

def main():

    TORCH_CAST, ASR_MODEL, FILEPATHS, BATCH_SIZE, CONF = init_conf_and_env()

    current_mode = mode.COMMAND

    while True:
        print("mainthread")
        record_one_phrase()
        transcriptions = run_inference(TORCH_CAST, ASR_MODEL, FILEPATHS, BATCH_SIZE)
        print(transcriptions)
        if current_mode is not mode.SLEEP:
            screen_print(transcriptions)
        # playsound("Assets/recorded.wav")

        # all mode switching, gui, and keyboard automation code is handlded here
        current_mode = handle_transcription(transcriptions, current_mode, CONF)


if __name__ == '__main__':
    main()

# [NeMo E 2021-12-30 16:57:18 segment:155] Loading Assets/recorded.wav via SoundFile raised RuntimeError: `Error opening 'Assets/recorded.wav': System error.`. NeMo will fallback to loading via pydub.