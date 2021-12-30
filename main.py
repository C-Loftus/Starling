from Desktop.generic_linux import screen_print
from Desktop.gnome import *
from Audio.recording import *
from nvidia.transcribe_speech import *
from setup import application_config


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





if __name__ == '__main__':
    main()

