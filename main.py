from Desktop.generic_linux import screen_print
from Desktop.gnome import *
from multiprocessing import Lock
import model
from Audio.recording import *
from nvidia.transcribe_speech import *

def init():
    env.set_vol(initialize=True)
    TranscriptionConfig.model_path = "nvidia/stt_en_conformer_ctc_medium.nemo"
    TranscriptionConfig.pretrained_name = "stt_en_conformer_ctc_medium"
    TranscriptionConfig.cuda = -1
    TranscriptionConfig.audio_dir = "Assets/"
    TranscriptionConfig.audio_type = "wav"
    TranscriptionConfig.batch_size=32
    init_transcribe_conf(TranscriptionConfig)

def main():
    init()

    while True:
        print("mainthread")
        record_one_phrase()

        out = init_transcribe_conf(TranscriptionConfig)  
        transcriptions = run_inference(out[0], out[1], out[2], out[3])
        screen_print(transcriptions)
        playsound("Assets/recorded.wav")
        os.remove('Assets/recorded.wav')
        if 'time' in transcriptions:
            default_timer_conf()





if __name__ == '__main__':
    main()

