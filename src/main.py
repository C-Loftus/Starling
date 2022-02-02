from AppIndicator.gtk_indicator import APPINDICATOR_ID, ProgramIndicator
from Desktop.generic_linux import screen_print
from Desktop.gnome import *
from Desktop.mode_functions import handle_transcription, mode
from Audio.recording import *
from nvidia.transcribe_speech import *
from setup_conf import application_config
from AppIndicator.socket_fns import *
from vosk_bindings.mic_input import VoskModel

CONFIG_PATH = "config.yaml"

# Parses the config and  normalizes audio to the ambient env volume
def init_conf_and_env():
    screen_print("Initializing...", delay=4)
    
    # Get the config From the user supplied file
    app_conf = application_config(CONFIG_PATH)
    
    # Initialize the app indicator on the dock
    p = Process(target=ProgramIndicator, args=(app_conf,))
    p.start()

    # Get the ambient volumeAnd open microphone stream
    env.set_vol(initialize=True)

    if app_conf.get_default_model() == "nvidia_nemo":
        # Initialized the model
        nemo = init_transcribe_conf(TranscriptionConfig)
        default = "nemo"
        model = (nemo[0], nemo[1], nemo[2], nemo[3])

    elif app_conf.get_default_model() == "vosk":
        default="vosk"
        model = VoskModel(app_conf)
    
    screen_print("Initialization complete")
    return model, default, app_conf
            
def main():
    model, default, CONF= init_conf_and_env()
    APPINDICATOR_SOCKET = ClientSocket()
    previous_mode, current_mode = mode.COMMAND, mode.COMMAND

    try:
        while True:

            '''
            There are two different interfaces for drawing inferences from the models
             since the nvidia nemo toolkit conformer model uses a batch API
              whereas the vosk model uses a stream API
            '''
            
            if default == "nemo":
                # Stores directly to .wav file
                record_one_phrase()
                transcriptions = run_inference(*model)
            elif default == "vosk":
                transcriptions = model.record_and_infer(current_mode)
            
            print(transcriptions)
            if current_mode is not mode.SLEEP:
                screen_print(transcriptions)

            # all mode switching, gui, and keyboard automation code is handlded here
            current_mode = handle_transcription(transcriptions, current_mode, CONF)

            # tentatively checks if the user sent a command is that would affect
            # the appindicator
            APPINDICATOR_SOCKET.check_to_send(previous_mode, current_mode, transcriptions)

            previous_mode = current_mode

    #  polite cleanup message to socket and ends program
    except KeyboardInterrupt:
        APPINDICATOR_SOCKET.force_quit()
        sys.exit(0)


if __name__ == '__main__':
    main()