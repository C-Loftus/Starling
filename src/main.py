from AppIndicator.gtk_indicator import ProgramIndicator
from Desktop.generic_linux import screen_print
from Desktop.gnome import *
from Desktop.mode_functions import handle_transcription, mode
from Audio.recording import *
from nvidia.transcribe_speech import *
from setup_conf import application_config
from AppIndicator.socket_fns import *

CONFIG_PATH = "config.yaml"

# Parses the config and  normalizes audio to the ambient env volume
def init_conf_and_env():
    screen_print("Initializing...", delay=6)
    
    # Get the config From the user supplied file
    app_conf = application_config(CONFIG_PATH)
    
    # Initialize the app indicator on the dock
    p = Process(target=ProgramIndicator, args=(app_conf,))
    p.start()

    # Get the ambient volumeAnd open microphone stream
    env.set_vol(initialize=True)

    # Initialized the model
    nemo = init_transcribe_conf(TranscriptionConfig)

    screen_print("Initialization complete")
    return nemo[0], nemo[1], nemo[2], nemo[3], app_conf, p
    
def main():

    TORCH_CAST, ASR_MODEL, FILEPATHS, BATCH_SIZE, CONF, _ = init_conf_and_env()
    APPINDICATOR_SOCKET = ClientSocket()

    previous_mode, current_mode = mode.COMMAND, mode.COMMAND

    while True:
        # Stores directly to .wav file
        record_one_phrase()
        transcriptions = run_inference(TORCH_CAST, ASR_MODEL, FILEPATHS, BATCH_SIZE)
        
        print(transcriptions)
        if current_mode is not mode.SLEEP:
            screen_print(transcriptions)

        # all mode switching, gui, and keyboard automation code is handlded here
        current_mode = handle_transcription(transcriptions, current_mode, CONF)

        # tentatively checks if the user wants to quit the app or sent a command
        # to the appindicator
        APPINDICATOR_SOCKET.check_to_send(previous_mode, current_mode, transcriptions)

        previous_mode = current_mode

if __name__ == '__main__':
    main()