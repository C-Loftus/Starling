from Desktop.generic_linux import screen_print
from Desktop.gnome import *
from Audio.recording import *
from nvidia.transcribe_speech import *
from setup_conf import application_config
from threading import Thread

def init_conf_and_env():
    env.set_vol(initialize=True)
    config_path = "config.yaml"
    application_config(config_path)
    return init_transcribe_conf(TranscriptionConfig)
    
def get_and_handle_inference(TORCH_CAST, ASR_MODEL, FILEPATHS, BATCH_SIZE):
    print("get_and_handle_inference")
    record_one_phrase()
    transcriptions = run_inference(TORCH_CAST, ASR_MODEL, FILEPATHS, BATCH_SIZE)
    print(transcriptions)
    screen_print(transcriptions)
    playsound("Assets/recorded.wav")
    if 'time' in transcriptions:
        default_timer_conf()
    os.remove("Assets/recorded.wav")


def main():
    model = init_conf_and_env()

    TORCH_CAST = model[0]
    ASR_MODEL = model[1]
    FILEPATHS = model[2]
    BATCH_SIZE = model[3]

    current_thread = Thread(target=get_and_handle_inference, args=(TORCH_CAST, ASR_MODEL, FILEPATHS, BATCH_SIZE))
    while True:
        print("mainthread")
        record_one_phrase()

        if current_thread.is_alive():
            current_thread.join()
        current_thread = Thread(target=get_and_handle_inference, args=(TORCH_CAST, ASR_MODEL, FILEPATHS, BATCH_SIZE))
        current_thread.start()

if __name__ == '__main__':
    main()

# [NeMo E 2021-12-30 16:57:18 segment:155] Loading Assets/recorded.wav via SoundFile raised RuntimeError: `Error opening 'Assets/recorded.wav': System error.`. NeMo will fallback to loading via pydub.