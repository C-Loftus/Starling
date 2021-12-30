from Desktop.generic_linux import screen_print
from Desktop.gnome import *
from Audio.recording import *
from nvidia.transcribe_speech import *
from setup_conf import application_config


def init_conf_and_env():
    env.set_vol(initialize=True)
    config_path = "config.yaml"
    application_config(config_path)
    return init_transcribe_conf(TranscriptionConfig)
    

def main():
    model = init_conf_and_env()

    TORCH_CAST = model[0]
    ASR_MODEL = model[1]
    FILEPATHS = model[2]
    BATCH_SIZE = model[3]

    while True:
        print("mainthread")
        record_one_phrase()

        transcriptions = run_inference(TORCH_CAST, ASR_MODEL, FILEPATHS, BATCH_SIZE)
        print(transcriptions)
        screen_print(transcriptions)
        playsound("Assets/recorded.wav")
        if 'time' in transcriptions:
            default_timer_conf()
        os.remove("Assets/recorded.wav")


if __name__ == '__main__':
    main()

# [NeMo E 2021-12-30 16:57:18 segment:155] Loading Assets/recorded.wav via SoundFile raised RuntimeError: `Error opening 'Assets/recorded.wav': System error.`. NeMo will fallback to loading via pydub.